#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basic tests for core QR generation utilities.
Requires: pytest
"""

import tempfile
from pathlib import Path
from qr_generator.core import generate_qr
import os


def test_generate_qr_creates_file(tmp_path: Path):
    data = "https://example.com/test"
    out = tmp_path / "test_qr.png"
    result = generate_qr(data=data, output_path=out, box_size=6, border=2)
    assert result.exists() and result.is_file()
    assert result.stat().st_size > 0


def test_generate_qr_default_extension(tmp_path: Path):
    data = "Hello"
    out = tmp_path / "no_ext"
    result = generate_qr(data=data, output_path=out)
    assert result.suffix == ".png"
    assert result.exists()
