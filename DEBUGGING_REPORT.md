# Technical Debugging Report — Shield Firewall

This document details two technical engineering challenges encountered during the development, extraction engineering, and testing of **Shield — AI-Driven Stealth Prompt Injection Detection Firewall**.

---

## Incident 1: Obfuscated Stealth Segment Classification Fallthrough in `/scan-text` API

### Problem
When testing zero-width unicode obfuscated text prompts (e.g. `I\u200Bg\u200Cn\u200Do\u200Br\uFEFFe all previous instructions`), the obfuscation engine correctly stripped zero-width characters and generated warning flags (`Zero-width unicode stealth detected`), but the primary text segment was classified as `is_hidden: False` during segment assembly. This caused the aggregated risk scanner to rely solely on raw DistilBERT probability thresholding rather than triggering the stealth layer risk heuristic, resulting in inconsistent risk ratings on edge-case prompt injection syntax.

### Error / Symptom
In automated unit tests:
```text
AssertionError: assert 'Safe' == 'Injection'
- Injection
+ Safe
```
The API logged zero-width character detection but returned an overall label of `Safe` for obfuscated attack vectors.

### Investigation
1. Traced the workflow execution from `app.py` -> `scan_text()` -> `obfuscation.py` -> `predict.py` -> `predict_stealth_scan()`.
2. Inspected `obfuscation.py` output dictionary: `zero_width_count` was 5, `cleaned_text` was `"Ignore all previous instructions..."`, but `is_hidden` in the segment metadata was hardcoded to `False`.
3. Checked `predict.py` line 95: The stealth heuristic override (`conf = max(conf, 99.2)`, `label = "Injection"`) was conditioned on `if is_hidden:`. Because `is_hidden` was `False`, the segment bypassed the stealth heuristic layer and fell through to standard ML sequence classification.

### Root Cause
The `scan_text` and `scan_file` endpoints treated zero-width unicode character stripping and homoglyph normalization purely as text cleaning operations without updating the segment's `is_hidden` attribute to `True`. Because zero-width characters and character spoofing are explicit obfuscation techniques designed to evade standard string matchers, any text carrying these anomalies is by definition a stealth layer payload.

### Solution
Updated `app.py` in both `/scan-text` and `/scan-file` endpoints to dynamically set `is_hidden = True` and populate `reason` whenever `zero_width_count > 0` or `homoglyph_count > 0`:

```python
# app.py
has_obfuscation = obf_result["zero_width_count"] > 0 or obf_result["homoglyph_count"] > 0

segments = [{
    "source": "Primary Text Prompt",
    "text": obf_result["cleaned_text"],
    "is_hidden": has_obfuscation,
    "reason": "Stealth obfuscation detected (Zero-width / Homoglyph characters)" if has_obfuscation else None
}]
```

### Verification
Re-ran Pytest suite across all API endpoints:
- `test_scan_text_zero_width_injection` passed cleanly.
- Verified API response: `overall_label: "Injection"`, `risk_level: "High"`, `obfuscation_warnings` populated.

---

## Incident 2: PyPDF Metadata Parsing & pdfplumber Color Space Normalization

### Problem
During PDF document layer extraction (`extract_pdf_layers` in `extractors.py`), white-on-white stealth text and microscopic font text ($\le 1.5\text{pt}$) were occasionally misclassified as visible body text, or threw type errors when parsing non-standard PDF color spaces (such as CMYK, single-channel grayscale floats, or `None` values).

### Error / Symptom
In PDF parsing logs:
```text
TypeError: 'float' object is not iterable
  File "extractors.py", line 17, in is_white_color
    return all(c >= 0.95 for c in color)
```
In addition, PDFs with white text rendered on light-gray backgrounds using 8-bit integer color spaces (`255, 255, 255`) failed float comparison checks (`color >= 0.95`), bypassing the white-text extractor.

### Investigation
1. Inspected `pdfplumber` character dictionary objects (`page.chars`). Found that PDF non-stroking colors can take multiple structural representations depending on PDF creation software:
   - Single float/int (`1.0` or `255`) for Grayscale
   - 3-tuple (`(1.0, 1.0, 1.0)` or `(255, 255, 255)`) for RGB
   - 4-tuple (`(0, 0, 0, 0)`) for CMYK (where 0 is white in subtractive CMYK)
   - `None` when color inherits from graphics state.
2. The initial `is_white_color()` helper assumed all color representations were 3-element RGB tuples of floats, causing runtime type errors on grayscale single floats and false negatives on 8-bit RGB integer tuples.

### Root Cause
Incompatible type handling and color space normalization in `is_white_color()`.

### Solution
Refactored `is_white_color()` in `extractors.py` to handle `None`, scalars, 1-tuple, 3-tuple (RGB float & int), and 4-tuple (CMYK float & int):

```python
def is_white_color(color):
    """Utility to check if PDF character color is white/near-white across PDF color spaces."""
    if color is None:
        return False
    if isinstance(color, (int, float)):
        return color >= 0.95 or color == 255
    if isinstance(color, (list, tuple)):
        if len(color) == 1:
            return color[0] >= 0.95 or color[0] == 255
        if len(color) == 3: # RGB
            return all(c >= 0.95 or c == 255 for c in color)
        if len(color) == 4: # CMYK (0,0,0,0 is white)
            return all(c <= 0.05 or c == 0 for c in color)
    return False
```

### Verification
Created test PDF document `test_documents/test_stealth_injection.pdf` containing white text and microscopic font text. Ran `test_stealth.py` and API file upload tests (`/scan-file`). Verified 100% layer extraction accuracy with zero runtime exceptions.
