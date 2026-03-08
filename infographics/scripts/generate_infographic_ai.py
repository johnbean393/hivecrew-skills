#!/usr/bin/env python3
"""
Deprecated compatibility wrapper.

In this environment, infographic generation should be performed with the native
`generate_image` tool rather than external API calls. This script preserves the
old filename while redirecting users to the new prompt-preparation workflow.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Prepare an infographic prompt for the environment generate_image tool"
    )
    parser.add_argument("prompt", help="Description of the infographic content")
    parser.add_argument("-o", "--output", required=True, help="Where to save the prompt/spec")
    parser.add_argument("--type", "-t")
    parser.add_argument("--style", "-s")
    parser.add_argument("--palette", "-p")
    parser.add_argument("--background", "-b", default="white")
    parser.add_argument("--doc-type", default="default")
    parser.add_argument("--aspect-ratio", default="3:4")
    parser.add_argument("--research", "-r", action="store_true",
                        help="Informational only: perform research via environment tools before generation")
    parser.add_argument("--iterations", type=int, default=1,
                        help="Unused in tool-native workflow; retained for compatibility")
    parser.add_argument("--api-key", help="Deprecated and ignored")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    helper = Path(__file__).with_name('generate_infographic.py')
    cmd = [sys.executable, str(helper), args.prompt, '-o', args.output,
           '--background', args.background, '--doc-type', args.doc_type,
           '--aspect-ratio', args.aspect_ratio]
    if args.type:
        cmd += ['--type', args.type]
    if args.style:
        cmd += ['--style', args.style]
    if args.palette:
        cmd += ['--palette', args.palette]

    if args.verbose:
        print('Info: external API-based generation is deprecated in this environment.')
        print('Info: preparing a prompt/spec for the native generate_image tool instead.')
        if args.research:
            print('Info: use web_search/read_webpage_content to gather facts before calling generate_image.')

    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == '__main__':
    main()
