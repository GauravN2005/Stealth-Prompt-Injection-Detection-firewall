import base64
import re
import urllib.parse
import codecs

# Common zero-width and invisible unicode characters
ZERO_WIDTH_CHARS = {
    '\u200B': 'Zero-Width Space',
    '\u200C': 'Zero-Width Non-Joiner',
    '\u200D': 'Zero-Width Joiner',
    '\uFEFF': 'Byte Order Mark',
    '\u00AD': 'Soft Hyphen',
    '\u202E': 'Right-to-Left Override',
    '\u202B': 'Right-to-Left Embedding',
    '\u200E': 'Left-to-Right Mark',
    '\u200F': 'Right-to-Left Mark',
    '\u2060': 'Word Joiner',
}

# Cyrillic & Greek homoglyphs commonly used to replace Latin letters
HOMOGLYPH_MAP = {
    'а': 'a', 'е': 'e', 'о': 'o', 'р': 'p', 'с': 'c', 'у': 'y', 'х': 'x',
    'А': 'A', 'В': 'B', 'Е': 'E', 'К': 'K', 'М': 'M', 'Н': 'H', 'О': 'O',
    'Р': 'P', 'С': 'C', 'Т': 'T', 'Х': 'X', 'α': 'a', 'ο': 'o', 'ρ': 'p'
}


def detect_and_clean_zero_width(text: str):
    """
    Detects zero-width and invisible characters, returns count details
    and a cleaned version of the text.
    """
    found_types = {}
    cleaned_chars = []

    for char in text:
        if char in ZERO_WIDTH_CHARS:
            name = ZERO_WIDTH_CHARS[char]
            found_types[name] = found_types.get(name, 0) + 1
        else:
            cleaned_chars.append(char)

    cleaned_text = "".join(cleaned_chars)
    total_found = sum(found_types.values())

    warnings = []
    if total_found > 0:
        details = ", ".join([f"{count} {name}(s)" for name, count in found_types.items()])
        warnings.append(f"Zero-width unicode stealth detected: {details}")

    return cleaned_text, total_found, warnings


def normalize_homoglyphs(text: str):
    """
    Detects Cyrillic/Greek homoglyphs mixed into Latin text and converts them.
    """
    homoglyph_count = 0
    normalized_chars = []

    for char in text:
        if char in HOMOGLYPH_MAP:
            normalized_chars.append(HOMOGLYPH_MAP[char])
            homoglyph_count += 1
        else:
            normalized_chars.append(char)

    normalized_text = "".join(normalized_chars)
    warnings = []
    if homoglyph_count > 0:
        warnings.append(f"Homoglyph spoofing detected: {homoglyph_count} character(s) normalized from Cyrillic/Greek to Latin")

    return normalized_text, homoglyph_count, warnings


def extract_encoded_payloads(text: str):
    """
    Searches text for Base64, Hexadecimal, and URL-encoded strings, decoding them
    to discover hidden prompt injection instructions.
    """
    decoded_segments = []
    warnings = []

    # 1. Base64 Pattern Search (strings >= 12 chars ending in optional padding)
    b64_pattern = r'[A-Za-z0-9+/]{12,}={0,2}'
    matches = re.findall(b64_pattern, text)

    for match in matches:
        # Ignore common non-injection words or hashes
        if len(match) % 4 == 0:
            try:
                decoded_bytes = base64.b64decode(match)
                decoded_str = decoded_bytes.decode('utf-8', errors='ignore').strip()
                # If decoded text looks like printable English text with spaces
                if len(decoded_str) > 6 and any(c == ' ' for c in decoded_str) and decoded_str.isprintable():
                    decoded_segments.append({
                        "source": f"Decoded Base64 Payload ({match[:10]}...)",
                        "text": decoded_str,
                        "is_hidden": True,
                        "reason": f"Decoded from Base64 string '{match[:16]}...'"
                    })
                    warnings.append(f"Base64 encoded payload detected & uncloaked: '{decoded_str[:60]}...'")
            except Exception:
                pass

    # 2. URL Encoding Search (%20, %27, etc.)
    if "%20" in text or "%2f" in text.lower() or "%3c" in text.lower():
        try:
            url_decoded = urllib.parse.unquote(text)
            if url_decoded != text and len(url_decoded) > 5:
                decoded_segments.append({
                    "source": "URL-Decoded Text Layer",
                    "text": url_decoded,
                    "is_hidden": True,
                    "reason": "Unquoted from URL-encoded format"
                })
                warnings.append("URL-encoded payload detected & decoded")
        except Exception:
            pass

    # 3. Hex String Search (e.g., \x49\x67 or 49676e6f7265)
    hex_pattern = r'(?:\\x[0-9a-fA-F]{2}){4,}'
    hex_matches = re.findall(hex_pattern, text)
    for h_match in hex_matches:
        try:
            raw_hex = h_match.replace('\\x', '')
            decoded_hex = bytes.fromhex(raw_hex).decode('utf-8', errors='ignore')
            if len(decoded_hex) > 3 and decoded_hex.isprintable():
                decoded_segments.append({
                    "source": "Hex-Decoded Payload Layer",
                    "text": decoded_hex,
                    "is_hidden": True,
                    "reason": f"Decoded from Hex sequence '{h_match[:16]}...'"
                })
                warnings.append(f"Hex-encoded payload uncloaked: '{decoded_hex}'")
        except Exception:
            pass

    return decoded_segments, warnings


def analyze_obfuscation(text: str):
    """
    Main obfuscation entry point. Cleans zero-width characters, normalizes homoglyphs,
    and extracts decoded payloads.
    """
    warnings = []
    
    # 1. Clean zero-width chars
    clean_text, zw_count, zw_warnings = detect_and_clean_zero_width(text)
    warnings.extend(zw_warnings)

    # 2. Normalize homoglyphs
    normalized_text, h_count, h_warnings = normalize_homoglyphs(clean_text)
    warnings.extend(h_warnings)

    # 3. Decode embedded payloads
    decoded_segments, enc_warnings = extract_encoded_payloads(normalized_text)
    warnings.extend(enc_warnings)

    return {
        "cleaned_text": normalized_text,
        "zero_width_count": zw_count,
        "homoglyph_count": h_count,
        "decoded_segments": decoded_segments,
        "warnings": warnings
    }
