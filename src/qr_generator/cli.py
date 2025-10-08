#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QR Code Generator — CLI wrapper
File: cli.py
Author: Mobin You
Created: 2025-10-08

A small command-line interface for the qr_generator package.
"""

from __future__ import annotations
import argparse
import logging
from pathlib import Path
import sys

from . import __version__
from .core import generate_qr

logger = logging.getLogger(__name__)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="qr-generator", description="Generate QR codes from the command line.")
    p.add_argument("data", help="Text or URL to encode as a QR code")
    p.add_argument("-o", "--output", help="Output file path (defaults to qrcode.png)", default="qrcode.png")
    p.add_argument("--box", type=int, default=10, help="Box size in pixels (default: 10)")
    p.add_argument("--border", type=int, default=4, help="Border size in boxes (default: 4)")
    p.add_argument("--version", action="store_true", help="Show package version and exit")
    p.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    if args.version:
        print(__version__)
        return 0

    try:
        out_path = Path(args.output)
        saved = generate_qr(data=args.data, output_path=out_path, box_size=args.box, border=args.border)
        print(f"Saved QR code to: {saved}")
        return 0
    except Exception as exc:  # pragma: no cover - top-level CLI handling
        logger.exception("Failed to generate QR code")
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
