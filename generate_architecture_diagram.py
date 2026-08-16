import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

def draw_architecture_diagram(output_path="architecture/architecture_diagram.png"):
    fig, ax = plt.subplots(figsize=(12, 10), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')

    # Color Palette
    PRIMARY = '#0F172A'    # Deep Navy
    SECONDARY = '#1E293B'  # Dark Slate
    BLUE = '#2563EB'       # Primary Accent Blue
    LIGHT_BLUE = '#EFF6FF' # Light Blue BG
    GREEN = '#16A34A'      # Success Green
    RED = '#DC2626'        # Alert Red
    GRAY_BG = '#F1F5F9'    # Box BG
    BORDER_GRAY = '#94A3B8'# Border Gray
    TEXT_COLOR = '#334155' # Dark Text

    # Title
    plt.text(50, 96, "SHIELD // SYSTEM ARCHITECTURE & DATA FLOW PIPELINE",
             ha='center', va='center', fontsize=15, fontweight='bold', color=PRIMARY)
    plt.text(50, 93.5, "AI-Driven Stealth Prompt Injection Firewall — Technical Flow Diagram",
             ha='center', va='center', fontsize=10, color=BLUE)

    def draw_box(x, y, w, h, title, subtitle, items, bg_color=GRAY_BG, border_color=BORDER_GRAY, header_bg=PRIMARY):
        # Draw main box
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.5",
                                     linewidth=1.2, edgecolor=border_color, facecolor=bg_color)
        ax.add_patch(rect)
        
        # Draw Header bar
        header_rect = patches.FancyBboxPatch((x, y + h - 4), w, 4, boxstyle="round,pad=0.1,rounding_size=0.8",
                                            linewidth=0, facecolor=header_bg)
        ax.add_patch(header_rect)
        
        # Header Text
        plt.text(x + w/2, y + h - 2, title, ha='center', va='center', fontsize=9.5, fontweight='bold', color='white')
        
        # Subtitle
        curr_y = y + h - 5.5
        if subtitle:
            plt.text(x + w/2, curr_y, subtitle, ha='center', va='center', fontsize=8, fontweight='bold', color=BLUE)
            curr_y -= 3
            
        # Items list
        for item in items:
            plt.text(x + 2, curr_y, item, ha='left', va='center', fontsize=7.5, color=TEXT_COLOR)
            curr_y -= 2.6

    def draw_arrow(x1, y1, x2, y2, label=""):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2, mutation_scale=15))
        if label:
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            plt.text(mid_x + 1.5, mid_y, label, ha='left', va='center', fontsize=7.5, fontweight='bold', color=BLUE)

    # 1. User & Client Ingestion Layer
    draw_box(5, 76, 90, 13,
             "1. USER & CLIENT INGESTION LAYER",
             "React 19 Security Dashboard & External API Clients",
             ["• Ingests PDF (.pdf), HTML (.html), Text (.txt), and Markdown (.md) documents",
              "• Interactive drag-and-drop file upload & real-time threat scanning UI",
              "• REST API Consumers submitting prompts & multi-part document streams"],
             bg_color='#FFFFFF', border_color=BLUE, header_bg=PRIMARY)

    draw_arrow(50, 76, 50, 69)

    # 2. FastAPI Gateway & Security Perimeter
    draw_box(5, 56, 90, 13,
             "2. FASTAPI PERIMETER GATEWAY & HEALTH MONITOR",
             "FastAPI 0.116 ASGI Router (app.py)",
             ["• Endpoints: GET / (Info), GET /health (Readiness), POST /scan-text, POST /scan-file",
              "• Structured Python logging (shield.api), CORS Middleware & Exception Sanitization",
              "• Health probe checking model load status, version (2.0), and PyTorch runtime"],
             bg_color='#FFFFFF', border_color=BLUE, header_bg=SECONDARY)

    draw_arrow(50, 56, 50, 49)

    # 3. Parallel Processing Modules: Extractor & Uncloaking (Two columns)
    draw_box(5, 30, 43, 19,
             "3A. MULTI-LAYER EXTRACTOR ENGINE",
             "extractors.py",
             ["• PDF Metadata Header Parser (/Author, /Subject)",
              "• PDF Layout Inspection (White text: RGB=255)",
              "• Microscopic Font Extraction (size <= 1.5pt)",
              "• HTML Hidden CSS Parsing (display:none, opacity:0)",
              "• HTML Comments (<!-- -->) & <meta> tags"],
             bg_color='#FFFFFF', border_color=BLUE, header_bg=BLUE)

    draw_box(52, 30, 43, 19,
             "3B. OBFUSCATION UNCLOAKING ENGINE",
             "obfuscation.py",
             ["• Zero-Width Character Stripper (\\u200B, \\uFEFF)",
              "• Cyrillic/Greek Homoglyph Normalizer (а -> a)",
              "• Base64 Payload Decoder ([A-Za-z0-9+/]{12,})",
              "• Hexadecimal String Uncloaker (\\x49\\x67...)",
              "• URL Percent-Decoding Engine"],
             bg_color='#FFFFFF', border_color=BLUE, header_bg=BLUE)

    # Arrows to 4
    draw_arrow(26.5, 30, 35, 23)
    draw_arrow(73.5, 30, 65, 23)

    # 4. Intelligence Layer (DistilBERT Classifier)
    draw_box(15, 10, 70, 13,
             "4. ML INTELLIGENCE LAYER (DistilBERT Classifier)",
             "predict.py & model.py (Fine-Tuned distilbert-base-uncased)",
             ["• DistilBertTokenizerFast (max_length=256 token sequence window)",
              "• Sequence Classification Logit Softmax Probabilities (Safe vs Injection)",
              "• Stealth Layer Priority Heuristics (Flags stealth layers carrying attack tokens)"],
             bg_color='#FFFFFF', border_color=RED, header_bg=PRIMARY)

    draw_arrow(50, 10, 50, 5)

    # 5. Output Threat Report
    draw_box(15, 0, 70, 5,
             "5. DOCUMENT THREAT REPORT & SEGMENT INSPECTOR",
             "",
             ["Overall Label (Safe/Injection) | Confidence % | Risk Hierarchy (High/Med/Low) | Segment Breakdown"],
             bg_color='#EFF6FF', border_color=GREEN, header_bg=GREEN)

    out_file = Path(output_path).resolve()
    out_file.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out_file, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] High-resolution architecture diagram saved: {out_file}")
    return out_file

if __name__ == "__main__":
    draw_architecture_diagram()
