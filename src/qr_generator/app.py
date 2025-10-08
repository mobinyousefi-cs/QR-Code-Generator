#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project: QR Code Generator
File: app.py
Author: Mobin You
Created: 2025-10-08
Updated: 2025-10-08

Description:
Tkinter GUI for the QR Code Generator project.
"""

import logging
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional
from PIL import ImageTk, Image
from .core import generate_qr

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class QRApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("QR Code Generator")
        self.geometry("640x420")
        self.resizable(False, False)
        self._create_widgets()
        self.preview_image = None

    def _create_widgets(self) -> None:
        frame = ttk.Frame(self, padding=12)
        frame.pack(fill=tk.BOTH, expand=True)

        # Input label + entry
        ttk.Label(frame, text="Text / URL:").grid(row=0, column=0, sticky=tk.W, pady=(0, 6))
        self.data_entry = ttk.Entry(frame, width=60)
        self.data_entry.grid(row=0, column=1, columnspan=3, sticky=tk.W, pady=(0, 6))

        # Output path
        ttk.Label(frame, text="Save as:").grid(row=1, column=0, sticky=tk.W)
        self.path_var = tk.StringVar()
        self.path_entry = ttk.Entry(frame, textvariable=self.path_var, width=45)
        self.path_entry.grid(row=1, column=1, sticky=tk.W)
        ttk.Button(frame, text="Browse...", command=self._browse_save).grid(row=1, column=2, padx=(6, 0))

        # Size
        ttk.Label(frame, text="Box size (px):").grid(row=2, column=0, sticky=tk.W, pady=(8, 0))
        self.box_spin = ttk.Spinbox(frame, from_=1, to=40, width=6)
        self.box_spin.set(10)
        self.box_spin.grid(row=2, column=1, sticky=tk.W, pady=(8, 0))

        # Border
        ttk.Label(frame, text="Border (boxes):").grid(row=2, column=2, sticky=tk.W, pady=(8, 0))
        self.border_spin = ttk.Spinbox(frame, from_=0, to=10, width=6)
        self.border_spin.set(4)
        self.border_spin.grid(row=2, column=3, sticky=tk.W, pady=(8, 0))

        # Buttons
        ttk.Button(frame, text="Generate & Save", command=self._on_generate).grid(row=3, column=1, pady=(14, 0))
        ttk.Button(frame, text="Preview", command=self._on_preview).grid(row=3, column=2, pady=(14, 0))
        ttk.Button(frame, text="Clear", command=self._on_clear).grid(row=3, column=3, pady=(14, 0))

        # Preview area
        self.preview_label = ttk.Label(frame, text="Preview will appear here", anchor=tk.CENTER)
        self.preview_label.grid(row=4, column=0, columnspan=4, sticky="nsew", pady=(16, 0))
        frame.rowconfigure(4, weight=1)

    def _browse_save(self) -> None:
        filetypes = [("PNG image", "*.png"), ("JPEG image", "*.jpg;*.jpeg"), ("All files", "*.*")]
        initialfile = "qrcode.png"
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=filetypes, initialfile=initialfile)
        if path:
            self.path_var.set(path)

    def _on_generate(self) -> None:
        data = self.data_entry.get().strip()
        out_path = self.path_var.get().strip()
        try:
            box = int(self.box_spin.get())
            border = int(self.border_spin.get())
        except Exception:
            messagebox.showerror("Invalid input", "Box size and border must be integers.")
            return

        if not data:
            messagebox.showwarning("Missing data", "Please enter the text or URL to convert to a QR code.")
            return

        if not out_path:
            # ask user where to save if not supplied
            self._browse_save()
            out_path = self.path_var.get().strip()
            if not out_path:
                return

        try:
            saved = generate_qr(data=data, output_path=Path(out_path), box_size=box, border=border)
            messagebox.showinfo("Success", f"QR code saved to:\n{saved}")
            logger.info("Generated QR saved to %s", saved)
        except Exception as exc:
            logger.exception("Failed to generate QR")
            messagebox.showerror("Error", f"Failed to generate QR code:\n{exc}")

    def _on_preview(self) -> None:
        data = self.data_entry.get().strip()
        if not data:
            messagebox.showwarning("Missing data", "Please enter the text or URL to preview.")
            return
        # create temporary in-memory image using core with a temp path in memory
        try:
            # create temp file
            import tempfile
            from pathlib import Path

            tmp = Path(tempfile.gettempdir()) / "qr_preview.png"
            generate_qr(data=data, output_path=tmp, box_size=int(self.box_spin.get()), border=int(self.border_spin.get()))
            img = Image.open(tmp)
            # Resize to fit preview area while keeping aspect
            w, h = img.size
            max_w, max_h = 420, 240
            ratio = min(max_w / w, max_h / h, 1.0)
            new_size = (int(w * ratio), int(h * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)

            self.preview_image = ImageTk.PhotoImage(img)
            self.preview_label.configure(image=self.preview_image, text="")
        except Exception as exc:
            logger.exception("Preview failed")
            messagebox.showerror("Preview Error", f"Could not generate preview:\n{exc}")

    def _on_clear(self) -> None:
        self.data_entry.delete(0, tk.END)
        self.path_var.set("")
        self.preview_label.configure(image="", text="Preview will appear here")
        self.preview_image = None


def main() -> None:
    app = QRApp()
    app.mainloop()


if __name__ == "__main__":
    main()
