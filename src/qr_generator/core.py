#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project: QR Code Generator
File: core.py
Author: Mobin You
Created: 2025-10-08
Updated: 2025-10-08

Description:
Core QR generation utilities. Provides a generate_qr function used by both GUI and tests/CLI.
"""

from typing import Optional
from pathlib import Path
import qrcode
from qrcode.constants import ERROR_CORRECT_M
from PIL import Image
import logging

logger = logging.getLogger(__name__)


def generate_qr(
    data: str,
    output_path: Path,
    box_size: int = 10,
    border: int = 4,
    error_correction: int = ERROR_CORRECT_M,
    fill_color: str = "black",
    back_color: str = "white",
) -> Path:
    """
    Generate a QR code image for `data` and save it at `output_path`.

    Args:
        data: text or URL to encode.
        output_path: Path to save the resulting image (should include extension .png/.jpg).
        box_size: size of each QR code box in pixels.
        border: width of border (boxes).
        error_correction: qrcode error correction constant.
        fill_color: color of the QR dots.
        back_color: color of the background.

    Returns:
        Path pointing to the saved file.

    Raises:
        ValueError: if `data` is empty or output_path has no parent directory available.
    """
    if not data or not data.strip():
        logger.error("Empty data provided to generate_qr")
        raise ValueError("Data to encode must be a non-empty string.")

    output_path = Path(output_path)
    if not output_path.suffix:
        logger.info("No suffix found for output; defaulting to .png")
        output_path = output_path.with_suffix(".png")

    out_dir = output_path.parent
    if out_dir and not out_dir.exists():
        logger.debug("Creating output directory: %s", out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

    qr = qrcode.QRCode(
        version=None,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )

    qr.add_data(data)
    qr.make(fit=True)

    img: Image.Image = qr.make_image(fill_color=fill_color, back_color=back_color)
    img.save(output_path)
    logger.info("Saved QR to %s", output_path)
    return output_path
