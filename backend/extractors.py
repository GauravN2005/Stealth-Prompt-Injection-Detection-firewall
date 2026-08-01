import io
import re
from bs4 import BeautifulSoup, Comment
import pdfplumber
from pypdf import PdfReader


def is_white_color(color):
    """Utility to check if PDF character color is white/near-white."""
    if color is None:
        return False
    if isinstance(color, (int, float)):
        return color >= 0.95 or color == 255
    if isinstance(color, (list, tuple)):
        if len(color) == 1:
            return color[0] >= 0.95 or color[0] == 255
        if len(color) == 3: # RGB
            return all(c >= 0.95 or c == 255 for c in color)
        if len(color) == 4: # CMYK (0, 0, 0, 0 is white)
            return all(c <= 0.05 or c == 0 for c in color)
    return False


def extract_pdf_layers(file_bytes: bytes):
    """
    Extracts text from PDF documents, separating visible text from hidden layers
    such as white-on-white text, microscopic fonts, annotations, and metadata.
    """
    segments = []
    
    # 1. Inspect Metadata using PyPDF
    try:
        pdf_reader = PdfReader(io.BytesIO(file_bytes))
        metadata = pdf_reader.metadata
        if metadata:
            meta_strings = []
            for key, val in metadata.items():
                if val and isinstance(val, str) and len(val.strip()) > 2:
                    meta_strings.append(f"{key}: {val.strip()}")
            if meta_strings:
                segments.append({
                    "source": "PDF Document Metadata",
                    "text": " | ".join(meta_strings),
                    "is_hidden": True,
                    "reason": "Embedded inside PDF Header/Metadata attributes"
                })
    except Exception as e:
        print(f"Error reading PDF metadata: {e}")

    # 2. Page & Font Attribute Inspection using pdfplumber
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page_idx, page in enumerate(pdf.pages, start=1):
                visible_chars = []
                white_chars = []
                tiny_chars = []

                chars = page.chars
                for char in chars:
                    text_str = char.get("text", "")
                    font_size = char.get("size", 10)
                    color = char.get("non_stroking_color") or char.get("stroking_color")

                    # Check for microscopic font
                    if font_size <= 1.5:
                        tiny_chars.append(text_str)
                    # Check for white / transparent text
                    elif is_white_color(color):
                        white_chars.append(text_str)
                    else:
                        visible_chars.append(text_str)

                # Assemble page text segments
                visible_text = "".join(visible_chars).strip()
                if visible_text:
                    segments.append({
                        "source": f"PDF Page {page_idx} (Visible Body)",
                        "text": visible_text,
                        "is_hidden": False,
                        "reason": None
                    })

                white_text = "".join(white_chars).strip()
                if white_text:
                    segments.append({
                        "source": f"PDF Page {page_idx} (White-on-White Layer)",
                        "text": white_text,
                        "is_hidden": True,
                        "reason": "Invisible text color matching white background"
                    })

                tiny_text = "".join(tiny_chars).strip()
                if tiny_text:
                    segments.append({
                        "source": f"PDF Page {page_idx} (Microscopic Font Layer)",
                        "text": tiny_text,
                        "is_hidden": True,
                        "reason": "Font size <= 1.5pt (Invisible to humans)"
                    })

    except Exception as e:
        print(f"Error parsing PDF layout: {e}")

    return segments


def extract_html_layers(html_content: str):
    """
    Extracts text from HTML documents, isolating visible rendered text from
    hidden CSS elements, comments, meta tags, and alt attributes.
    """
    segments = []
    soup = BeautifulSoup(html_content, "html.parser")

    # 1. Extract HTML Comments
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    comment_texts = [c.strip() for c in comments if len(c.strip()) > 3]
    if comment_texts:
        segments.append({
            "source": "HTML Comments Layer",
            "text": " \n ".join(comment_texts),
            "is_hidden": True,
            "reason": "Hidden inside HTML <!-- comment --> tags"
        })

    # 2. Extract Meta & Alt Attributes
    meta_texts = []
    for meta in soup.find_all("meta"):
        content = meta.get("content")
        if content and len(content.strip()) > 3:
            meta_texts.append(f"{meta.get('name') or meta.get('property') or 'meta'}: {content.strip()}")

    for img in soup.find_all(["img", "svg"]):
        alt = img.get("alt") or img.get("title")
        if alt and len(alt.strip()) > 3:
            meta_texts.append(f"Image Alt: {alt.strip()}")

    if meta_texts:
        segments.append({
            "source": "HTML Meta & Attribute Layer",
            "text": " | ".join(meta_texts),
            "is_hidden": True,
            "reason": "Hidden inside HTML <meta> tags or img attributes"
        })

    # 3. Identify Hidden CSS Elements (display:none, visibility:hidden, opacity:0, font-size:0)
    hidden_css_elements = []
    hidden_selectors = soup.find_all(
        lambda tag: tag.has_attr("style") or tag.has_attr("hidden") or tag.get("aria-hidden") == "true"
    )

    for tag in hidden_selectors:
        style = (tag.get("style") or "").lower().replace(" ", "")
        is_hidden_css = (
            tag.has_attr("hidden") or
            tag.get("aria-hidden") == "true" or
            "display:none" in style or
            "visibility:hidden" in style or
            "opacity:0" in style or
            "font-size:0" in style or
            "color:white" in style or
            "color:#fff" in style or
            "color:transparent" in style
        )
        if is_hidden_css:
            text = tag.get_text(strip=True)
            if len(text) > 2:
                hidden_css_elements.append(text)
                # Remove tag so it doesn't duplicate in visible text extraction
                tag.decompose()

    if hidden_css_elements:
        segments.append({
            "source": "HTML Hidden CSS Element",
            "text": " \n ".join(hidden_css_elements),
            "is_hidden": True,
            "reason": "Hidden via CSS (display:none / opacity:0 / color:transparent)"
        })

    # 4. Extract Visible Rendered Body Text
    # Remove script and style tags first
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()

    visible_body = soup.get_text(separator=" ", strip=True)
    if visible_body:
        segments.append({
            "source": "HTML Rendered Body (Visible)",
            "text": visible_body,
            "is_hidden": False,
            "reason": None
        })

    return segments


def extract_text_layers(text_content: str):
    """
    Extracts text from plain text or markdown files.
    """
    return [{
        "source": "Text Document Body",
        "text": text_content.strip(),
        "is_hidden": False,
        "reason": None
    }]
