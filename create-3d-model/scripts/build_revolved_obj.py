#!/usr/bin/env python3
"""Build a simple textured revolved OBJ model and a dimensioned drawing.

Best for bottles, jars, cans, cups, vases, candles, and similar axisymmetric objects.
Outputs OBJ + MTL + texture + profile CSV + analysis JSON + drawing PNG.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument('--image', help='Reference image path')
    p.add_argument('--generic', choices=['bottle', 'can', 'cup', 'jar', 'vase', 'thermos'], help='Built-in fallback profile when no image exists')
    p.add_argument('--name', required=True, help='Base filename for outputs')
    p.add_argument('--outdir', required=True, help='Output directory')
    p.add_argument('--height', type=float, default=100.0, help='Model height in chosen units')
    p.add_argument('--units', default='mm', help='Dimension label units, e.g. mm or cm')
    p.add_argument('--segments', type=int, default=96, help='Radial mesh segments')
    p.add_argument('--texture-width', type=int, default=2048)
    p.add_argument('--texture-height', type=int, default=2048)
    p.add_argument('--bg-threshold', type=float, default=24.0, help='Foreground/background RGB distance threshold when no alpha exists')
    p.add_argument('--smooth-passes', type=int, default=2, help='Radius smoothing passes')
    args = p.parse_args()
    if not args.image and not args.generic:
        p.error('provide --image or --generic')
    return args


def slugify(text: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-') or 'model'


def bilinear_sample_rgba(image_arr: np.ndarray, x: np.ndarray, y: float) -> np.ndarray:
    h, w, _ = image_arr.shape
    x = np.clip(x, 0.0, w - 1.001)
    y = float(np.clip(y, 0.0, h - 1.001))
    x0 = np.floor(x).astype(np.int32)
    y0 = int(math.floor(y))
    x1 = np.clip(x0 + 1, 0, w - 1)
    y1 = min(y0 + 1, h - 1)
    wx = (x - x0).reshape(-1, 1)
    wy = float(y - y0)
    c00 = image_arr[y0, x0]
    c10 = image_arr[y0, x1]
    c01 = image_arr[y1, x0]
    c11 = image_arr[y1, x1]
    top = c00 * (1.0 - wx) + c10 * wx
    bot = c01 * (1.0 - wx) + c11 * wx
    return top * (1.0 - wy) + bot * wy


def smooth_profile(values: np.ndarray, passes: int) -> np.ndarray:
    kernel = np.array([1, 2, 3, 4, 5, 4, 3, 2, 1], dtype=np.float64)
    kernel /= kernel.sum()
    out = values.astype(np.float64)
    for _ in range(max(0, passes)):
        pad = len(kernel) // 2
        padded = np.pad(out, (pad, pad), mode='edge')
        out = np.convolve(padded, kernel, mode='valid')
    return out


def detect_mask_from_image(path: Path, bg_threshold: float):
    img = Image.open(path).convert('RGBA')
    arr = np.array(img)
    alpha = arr[:, :, 3]
    if int(alpha.max()) > 20 and int((alpha > 20).sum()) > 100:
        mask = alpha > 20
        mask_source = 'alpha'
    else:
        rgb = arr[:, :, :3].astype(np.int16)
        border = np.concatenate([rgb[0], rgb[-1], rgb[:, 0], rgb[:, -1]], axis=0)
        bg = np.median(border, axis=0)
        dist = np.sqrt(((rgb - bg) ** 2).sum(axis=2))
        mask = dist > float(bg_threshold)
        row_keep = mask.sum(axis=1) > 2
        col_keep = mask.sum(axis=0) > 2
        mask &= row_keep[:, None]
        mask &= col_keep[None, :]
        mask_source = 'border-threshold'
    ys, xs = np.where(mask)
    if len(xs) == 0:
        raise RuntimeError('Could not detect object silhouette from image')
    return img, arr, mask, mask_source


def extract_profile_from_mask(mask: np.ndarray):
    ys, xs = np.where(mask)
    y_min, y_max = int(ys.min()), int(ys.max())
    x_min, x_max = int(xs.min()), int(xs.max())
    rows = np.arange(y_min, y_max + 1)
    left = np.full(len(rows), np.nan)
    right = np.full(len(rows), np.nan)
    center = np.full(len(rows), np.nan)
    for i, y in enumerate(rows):
        row = np.where(mask[y])[0]
        if len(row):
            left[i] = float(row.min())
            right[i] = float(row.max())
            center[i] = (left[i] + right[i]) / 2.0
    valid = np.isfinite(center)
    idx = np.arange(len(rows))
    left = np.interp(idx, idx[valid], left[valid])
    right = np.interp(idx, idx[valid], right[valid])
    center = np.interp(idx, idx[valid], center[valid])
    axis_x = float(np.median(center))
    radius_px = np.maximum(axis_x - left, right - axis_x)
    bbox = dict(x_min=x_min, y_min=y_min, x_max=x_max, y_max=y_max)
    return rows, left, right, center, axis_x, radius_px, bbox


def generic_profile(kind: str, samples: int = 500):
    y = np.linspace(0.0, 1.0, samples)
    tables = {
        'bottle': [(0.00, 0.10), (0.05, 0.14), (0.12, 0.13), (0.22, 0.24), (0.35, 0.42), (0.78, 0.43), (0.93, 0.35), (0.99, 0.20), (1.00, 0.03)],
        'can':    [(0.00, 0.42), (0.03, 0.45), (0.08, 0.44), (0.92, 0.44), (0.97, 0.45), (1.00, 0.40)],
        'cup':    [(0.00, 0.22), (0.10, 0.22), (0.25, 0.28), (0.55, 0.34), (0.88, 0.39), (1.00, 0.42)],
        'jar':    [(0.00, 0.20), (0.08, 0.24), (0.15, 0.40), (0.82, 0.42), (0.95, 0.28), (1.00, 0.18)],
        'vase':   [(0.00, 0.12), (0.08, 0.15), (0.25, 0.26), (0.50, 0.45), (0.76, 0.32), (0.92, 0.18), (1.00, 0.14)],
        'thermos':[(0.00, 0.18), (0.08, 0.22), (0.14, 0.22), (0.18, 0.28), (0.92, 0.28), (1.00, 0.24)],
    }
    pts = np.array(tables[kind], dtype=float)
    radius = np.interp(y, pts[:, 0], pts[:, 1]) * 100.0
    rows = np.arange(samples)
    left = 150.0 - radius
    right = 150.0 + radius
    center = np.full(samples, 150.0)
    bbox = dict(x_min=int(left.min()), y_min=0, x_max=int(right.max()), y_max=samples - 1)
    return rows, left, right, center, 150.0, radius, bbox


def generic_texture(kind: str, width: int, height: int) -> Image.Image:
    base_colors = {
        'bottle': (205, 230, 245),
        'can': (210, 210, 214),
        'cup': (245, 244, 240),
        'jar': (222, 236, 220),
        'vase': (228, 218, 236),
        'thermos': (210, 225, 205),
    }
    rgb = np.zeros((height, width, 3), dtype=np.uint8)
    base = np.array(base_colors[kind], dtype=np.float32)
    xs = np.linspace(0.0, 1.0, width)
    ys = np.linspace(0.0, 1.0, height)
    stripe = 0.88 + 0.12 * np.cos(xs * 2.0 * np.pi)
    vertical = 0.92 + 0.08 * np.cos((ys - 0.3) * np.pi)
    for j, fy in enumerate(vertical):
        row = np.clip(base * fy * stripe[:, None], 0, 255)
        rgb[j] = row.astype(np.uint8)
    img = Image.fromarray(rgb).convert('RGBA')
    d = ImageDraw.Draw(img)
    band_y0 = int(height * 0.42)
    band_y1 = int(height * 0.58)
    d.rounded_rectangle((int(width * 0.18), band_y0, int(width * 0.82), band_y1), radius=18, outline=(50, 50, 50, 255), width=6, fill=(255, 255, 255, 180))
    d.text((int(width * 0.34), int(height * 0.47)), kind.upper(), fill=(40, 40, 40, 255))
    return img


def build_texture_from_image(arr: np.ndarray, rows: np.ndarray, axis_x: float, radius_px: np.ndarray, tex_w: int, tex_h: int) -> Image.Image:
    src = arr.astype(np.float32)
    y_min = int(rows[0])
    y_max = int(rows[-1])
    source_y = np.linspace(y_min, y_max, tex_h)
    radius_interp = np.interp(source_y, rows, radius_px)
    sin_theta = np.sin((np.arange(tex_w) + 0.5) / tex_w * 2.0 * np.pi - np.pi)
    out = np.zeros((tex_h, tex_w, 4), dtype=np.uint8)
    for j, yf in enumerate(source_y):
        r = float(radius_interp[j])
        x_sample = axis_x + r * sin_theta
        rgba = bilinear_sample_rgba(src, x_sample, float(yf))
        out[j, :, :3] = np.clip(rgba[:, :3], 0, 255).astype(np.uint8)
        out[j, :, 3] = 255
    return Image.fromarray(out)


def build_mesh(model_height: float, model_radius: np.ndarray, segments: int):
    verts, uvs, faces = [], [], []
    ring_count = len(model_radius)
    for i, r in enumerate(model_radius):
        y = model_height * (1.0 - i / (ring_count - 1))
        v = 1.0 - i / (ring_count - 1)
        for k in range(segments + 1):
            u = k / segments
            theta = 2.0 * math.pi * u - math.pi
            x = float(r) * math.sin(theta)
            z = float(r) * math.cos(theta)
            verts.append((x, y, z))
            uvs.append((u, v))
    verts.append((0.0, model_height, 0.0))
    uvs.append((0.5, 1.0))
    top_idx = len(verts)
    verts.append((0.0, 0.0, 0.0))
    uvs.append((0.5, 0.0))
    bottom_idx = len(verts)

    def vid(i, k):
        return i * (segments + 1) + k + 1

    for i in range(ring_count - 1):
        for k in range(segments):
            a, b, c, d = vid(i, k), vid(i + 1, k), vid(i + 1, k + 1), vid(i, k + 1)
            faces.append((a, b, c))
            faces.append((a, c, d))
    for k in range(segments):
        faces.append((top_idx, vid(0, k + 1), vid(0, k)))
    last = ring_count - 1
    for k in range(segments):
        faces.append((bottom_idx, vid(last, k), vid(last, k + 1)))
    return verts, uvs, faces


def write_obj_bundle(obj_path: Path, mtl_path: Path, texture_name: str, verts, uvs, faces):
    with mtl_path.open('w') as f:
        f.write('newmtl material0\n')
        f.write('Ka 1.000 1.000 1.000\n')
        f.write('Kd 1.000 1.000 1.000\n')
        f.write('Ks 0.180 0.180 0.180\n')
        f.write('Ns 80.000\n')
        f.write('illum 2\n')
        f.write(f'map_Kd {texture_name}\n')
    with obj_path.open('w') as f:
        f.write(f'mtllib {mtl_path.name}\n')
        f.write(f'o {obj_path.stem}\n')
        for x, y, z in verts:
            f.write(f'v {x:.6f} {y:.6f} {z:.6f}\n')
        for u, v in uvs:
            f.write(f'vt {u:.6f} {v:.6f}\n')
        f.write('usemtl material0\n')
        f.write('s 1\n')
        for a, b, c in faces:
            f.write(f'f {a}/{a} {b}/{b} {c}/{c}\n')


def draw_dimension(draw: ImageDraw.ImageDraw, xy0, xy1, label, orientation='h'):
    x0, y0 = xy0
    x1, y1 = xy1
    color = (40, 40, 40)
    draw.line((x0, y0, x1, y1), fill=color, width=2)
    if orientation == 'h':
        draw.line((x0, y0 - 8, x0, y0 + 8), fill=color, width=2)
        draw.line((x1, y1 - 8, x1, y1 + 8), fill=color, width=2)
        draw.text(((x0 + x1) / 2 - 28, y0 - 22), label, fill=color)
    else:
        draw.line((x0 - 8, y0, x0 + 8, y0), fill=color, width=2)
        draw.line((x1 - 8, y1, x1 + 8, y1), fill=color, width=2)
        draw.text((x0 + 10, (y0 + y1) / 2 - 8), label, fill=color)


def draw_dimension_sheet(path: Path, name: str, model_height: float, max_radius: float, units: str, model_radius: np.ndarray):
    W, H = 1600, 1100
    img = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(img)
    d.text((40, 25), f'{name} - dimensioned drawing', fill=(20, 20, 20))
    d.text((40, 55), f'Units: {units}', fill=(70, 70, 70))

    panel_front = (60, 120, 430, 980)
    panel_side = (470, 120, 840, 980)
    panel_top = (900, 140, 1230, 470)
    panel_iso = (900, 520, 1520, 1000)

    def draw_front(panel, label):
        x0, y0, x1, y1 = panel
        d.rectangle(panel, outline=(180, 180, 180), width=2)
        d.text((x0 + 10, y0 + 10), label, fill=(30, 30, 30))
        margin = 45
        pw = x1 - x0 - margin * 2
        ph = y1 - y0 - 90
        local_max_r = float(model_radius.max())
        sx = (pw / 2.0) / local_max_r
        sy = ph / model_height
        px = x0 + (x1 - x0) / 2.0
        py_top = y0 + 55
        left_pts, right_pts = [], []
        for i, r in enumerate(model_radius):
            y = model_height * (i / (len(model_radius) - 1))
            yy = py_top + y * sy
            left_pts.append((px - r * sx, yy))
            right_pts.append((px + r * sx, yy))
        outline = left_pts + right_pts[::-1]
        d.polygon(outline, outline=(60, 90, 150), fill=(235, 243, 255))
        draw_dimension(d, (x0 + 18, py_top), (x0 + 18, py_top + model_height * sy), f'H={model_height:.1f} {units}', 'v')
        ymid = py_top + (np.argmax(model_radius) / (len(model_radius) - 1)) * model_height * sy
        draw_dimension(d, (px - local_max_r * sx, ymid + 28), (px + local_max_r * sx, ymid + 28), f'Ømax={2 * local_max_r:.1f} {units}', 'h')

    draw_front(panel_front, 'Front')
    draw_front(panel_side, 'Side')

    x0, y0, x1, y1 = panel_top
    d.rectangle(panel_top, outline=(180, 180, 180), width=2)
    d.text((x0 + 10, y0 + 10), 'Top', fill=(30, 30, 30))
    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2 + 20
    radius_px = min((x1 - x0), (y1 - y0)) * 0.32
    d.ellipse((cx - radius_px, cy - radius_px, cx + radius_px, cy + radius_px), outline=(60, 90, 150), width=3, fill=(235, 243, 255))
    draw_dimension(d, (cx - radius_px, cy + radius_px + 30), (cx + radius_px, cy + radius_px + 30), f'Ømax={2 * max_radius:.1f} {units}', 'h')

    x0, y0, x1, y1 = panel_iso
    d.rectangle(panel_iso, outline=(180, 180, 180), width=2)
    d.text((x0 + 10, y0 + 10), 'Isometric', fill=(30, 30, 30))
    sample_rings = np.linspace(0, len(model_radius) - 1, 12).astype(int)
    longitude_thetas = np.linspace(0, 2 * np.pi, 10, endpoint=False)
    ring_thetas = np.linspace(0, 2 * np.pi, 41)

    def iso_raw(x, y, z):
        ay = math.radians(45)
        ax = math.radians(35.264)
        x1r = x * math.cos(ay) + z * math.sin(ay)
        z1r = -x * math.sin(ay) + z * math.cos(ay)
        y2r = y * math.cos(ax) - z1r * math.sin(ax)
        return x1r, -y2r

    all_pts = []
    for idx in sample_rings:
        r = float(model_radius[idx])
        yv = model_height * (1.0 - idx / (len(model_radius) - 1))
        all_pts.extend([iso_raw(r * math.sin(t), yv, r * math.cos(t)) for t in ring_thetas])
    for theta in longitude_thetas:
        for idx in np.linspace(0, len(model_radius) - 1, 60).astype(int):
            r = float(model_radius[idx])
            yv = model_height * (1.0 - idx / (len(model_radius) - 1))
            all_pts.append(iso_raw(r * math.sin(theta), yv, r * math.cos(theta)))

    xs = [p[0] for p in all_pts]
    ys = [p[1] for p in all_pts]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    pad = 32
    avail_w = (x1 - x0) - 2 * pad
    avail_h = (y1 - y0) - 2 * pad - 24
    scale = min(avail_w / max(1e-6, (maxx - minx)), avail_h / max(1e-6, (maxy - miny)))

    def project(x, y, z):
        rx, ry = iso_raw(x, y, z)
        px = x0 + pad + (rx - minx) * scale
        py = y0 + 50 + (ry - miny) * scale
        return (px, py)

    for idx in sample_rings:
        r = float(model_radius[idx])
        yv = model_height * (1.0 - idx / (len(model_radius) - 1))
        pts = [project(r * math.sin(t), yv, r * math.cos(t)) for t in ring_thetas]
        d.line(pts, fill=(150, 170, 205), width=1)
    for theta in longitude_thetas:
        pts = []
        for idx in np.linspace(0, len(model_radius) - 1, 60).astype(int):
            r = float(model_radius[idx])
            yv = model_height * (1.0 - idx / (len(model_radius) - 1))
            pts.append(project(r * math.sin(theta), yv, r * math.cos(theta)))
        d.line(pts, fill=(70, 90, 120), width=2)
    d.text((x0 + 20, y1 - 32), 'Generated from extracted/reconstructed profile', fill=(90, 90, 90))
    img.save(path)


def main():
    args = parse_args()
    outdir = Path(args.outdir).expanduser().resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    base = slugify(args.name)

    if args.image:
        image_path = Path(args.image).expanduser().resolve()
        _img, arr, mask, mask_source = detect_mask_from_image(image_path, args.bg_threshold)
        rows, left, right, center, axis_x, radius_px, bbox = extract_profile_from_mask(mask)
        radius_px = smooth_profile(radius_px, args.smooth_passes)
        texture = build_texture_from_image(arr, rows, axis_x, radius_px, args.texture_width, args.texture_height)
        image_source = str(image_path)
    else:
        rows, left, right, center, axis_x, radius_px, bbox = generic_profile(args.generic)
        radius_px = smooth_profile(radius_px, args.smooth_passes)
        texture = generic_texture(args.generic, args.texture_width, args.texture_height)
        mask_source = f'generic:{args.generic}'
        image_source = None

    model_height = float(args.height)
    pixel_height = max(1.0, float(rows[-1] - rows[0]))
    scale = model_height / pixel_height
    model_radius = radius_px * scale
    max_radius = float(model_radius.max())

    verts, uvs, faces = build_mesh(model_height, model_radius, args.segments)

    obj_path = outdir / f'{base}.obj'
    mtl_path = outdir / f'{base}.mtl'
    tex_path = outdir / f'{base}_texture.png'
    csv_path = outdir / f'{base}_profile.csv'
    json_path = outdir / f'{base}_analysis.json'
    drawing_path = outdir / f'{base}_drawing.png'

    texture.save(tex_path)
    write_obj_bundle(obj_path, mtl_path, tex_path.name, verts, uvs, faces)
    draw_dimension_sheet(drawing_path, args.name, model_height, max_radius, args.units, model_radius)

    with csv_path.open('w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['source_y_px', 'center_x_px', 'left_x_px', 'right_x_px', 'radius_px', 'model_y', 'model_radius'])
        for i, y in enumerate(rows):
            model_y = model_height * (1.0 - i / (len(rows) - 1))
            w.writerow([
                int(y),
                round(float(axis_x), 4),
                round(float(left[i]), 4),
                round(float(right[i]), 4),
                round(float(radius_px[i]), 4),
                round(float(model_y), 6),
                round(float(model_radius[i]), 6),
            ])

    analysis = {
        'name': args.name,
        'source_image': image_source,
        'mask_source': mask_source,
        'bbox_px': bbox,
        'height': model_height,
        'units': args.units,
        'segments': args.segments,
        'rings': len(rows),
        'vertex_count': len(verts),
        'face_count': len(faces),
        'max_radius': max_radius,
        'max_diameter': 2 * max_radius,
        'outputs': {
            'obj': str(obj_path),
            'mtl': str(mtl_path),
            'texture': str(tex_path),
            'profile_csv': str(csv_path),
            'drawing_png': str(drawing_path),
        },
    }
    json_path.write_text(json.dumps(analysis, indent=2))
    print(json.dumps(analysis, indent=2))


if __name__ == '__main__':
    main()
