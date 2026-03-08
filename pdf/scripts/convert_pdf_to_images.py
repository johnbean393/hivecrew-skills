import glob
import os
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image


# Converts each page of a PDF to a PNG image.
# Default rendering method prefers native Poppler tools available on macOS:
#   1. pdftocairo (best quality/alpha handling)
#   2. pdftoppm
#   3. pdf2image (legacy fallback, if installed)


def _resize_if_needed(image_path, max_dim):
    with Image.open(image_path) as image:
        width, height = image.size
        if width <= max_dim and height <= max_dim:
            return image.size
        scale_factor = min(max_dim / width, max_dim / height)
        new_width = max(1, int(width * scale_factor))
        new_height = max(1, int(height * scale_factor))
        resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        resized.save(image_path)
        return resized.size


def _render_with_pdftocairo(pdf_path, output_dir, dpi):
    exe = shutil.which('pdftocairo')
    if not exe:
        return False
    prefix = os.path.join(output_dir, 'page')
    subprocess.run([exe, '-png', '-r', str(dpi), pdf_path, prefix], check=True)
    return True


def _render_with_pdftoppm(pdf_path, output_dir, dpi):
    exe = shutil.which('pdftoppm')
    if not exe:
        return False
    prefix = os.path.join(output_dir, 'page')
    subprocess.run([exe, '-png', '-r', str(dpi), pdf_path, prefix], check=True)
    return True


def _render_with_pdf2image(pdf_path, output_dir, dpi):
    try:
        from pdf2image import convert_from_path
    except Exception:
        return False
    images = convert_from_path(pdf_path, dpi=dpi)
    for i, image in enumerate(images, start=1):
        image.save(os.path.join(output_dir, f'page-{i}.png'))
    return True


def _normalize_filenames(output_dir):
    candidates = sorted(glob.glob(os.path.join(output_dir, 'page-*.png')))
    if not candidates:
        candidates = sorted(glob.glob(os.path.join(output_dir, 'page*.png')))
    if not candidates:
        raise RuntimeError('Rendering produced no PNG files')

    normalized = []
    for idx, src in enumerate(candidates, start=1):
        dst = os.path.join(output_dir, f'page_{idx}.png')
        if os.path.abspath(src) != os.path.abspath(dst):
            os.replace(src, dst)
        normalized.append(dst)
    return normalized


def convert(pdf_path, output_dir, max_dim=1000, dpi=200):
    pdf_path = os.path.abspath(pdf_path)
    output_dir = os.path.abspath(output_dir)
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Clean prior PNGs from this output directory to avoid stale files.
    for old in glob.glob(os.path.join(output_dir, '*.png')):
        os.remove(old)

    rendered = (
        _render_with_pdftocairo(pdf_path, output_dir, dpi)
        or _render_with_pdftoppm(pdf_path, output_dir, dpi)
        or _render_with_pdf2image(pdf_path, output_dir, dpi)
    )
    if not rendered:
        raise RuntimeError(
            'No supported PDF renderer available. Install pdftocairo, pdftoppm, or pdf2image.'
        )

    image_paths = _normalize_filenames(output_dir)
    for image_path in image_paths:
        final_size = _resize_if_needed(image_path, max_dim)
        print(f'Saved {image_path} (size: {final_size})')

    print(f'Converted {len(image_paths)} pages to PNG images')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: convert_pdf_to_images.py [input pdf] [output directory]')
        sys.exit(1)
    pdf_path = sys.argv[1]
    output_directory = sys.argv[2]
    convert(pdf_path, output_directory)
