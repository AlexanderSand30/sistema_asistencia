import os
from io import BytesIO
from flask import current_app
from xhtml2pdf import pisa


def link_callback(uri, rel):
    """Convierte rutas /static/... en rutas físicas para que xhtml2pdf
    pueda cargar imágenes (como el logo)."""
    if uri.startswith("/static/"):
        return os.path.join(current_app.root_path, uri.lstrip("/"))
    return uri


def html_a_pdf(html_string):
    buffer = BytesIO()
    pdf = pisa.CreatePDF(src=html_string, dest=buffer, link_callback=link_callback)
    if pdf.err:
        return None
    return buffer.getvalue()