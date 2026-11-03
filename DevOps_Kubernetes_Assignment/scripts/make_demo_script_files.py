#!/usr/bin/env python3
"""
Generate DEMO_RECORDING_SCRIPT in DOCX and PDF formats
Student: Yash Janardan Sabale | PRN: 202301040087 | MITAOE Pune
"""

import re
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable
from reportlab.pdfgen import canvas

BASE_DIR = Path(__file__).resolve().parent.parent
DOC_MD = BASE_DIR / "docs" / "DEMO_RECORDING_SCRIPT.md"
DOCX_OUT = BASE_DIR / "docs" / "DEMO_RECORDING_SCRIPT.docx"
PDF_OUT = BASE_DIR / "docs" / "DEMO_RECORDING_SCRIPT.pdf"

def md_to_xml(text):
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # Convert back tags we want
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    text = re.sub(r'`(.*?)`', r'<font face="Courier">\1</font>', text)
    return text

def build_docx():
    doc = docx.Document()
    for sec in doc.sections:
        sec.top_margin = Inches(0.8)
        sec.bottom_margin = Inches(0.8)
        sec.left_margin = Inches(0.8)
        sec.right_margin = Inches(0.8)

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = title.add_run("🎬 Video Demonstration Script (5 to 8 Minutes)\n")
    r.bold = True
    r.font.size = Pt(20)
    r.font.color.rgb = RGBColor(15, 23, 42)

    sub = title.add_run("Containerization & Kubernetes Deployment Demonstration\nStudent: Yash Janardan Sabale | PRN: 202301040087 | MITAOE Pune")
    sub.font.size = Pt(11)
    sub.font.color.rgb = RGBColor(71, 85, 105)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    content = DOC_MD.read_text(encoding="utf-8")
    for line in content.splitlines():
        if line.startswith("# ") or line.startswith("## ") or line.startswith("### "):
            text = line.lstrip("#").strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(4)
            r = p.add_run(text)
            r.bold = True
            r.font.size = Pt(13)
            r.font.color.rgb = RGBColor(2, 132, 199)
        elif line.startswith("> "):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.4)
            p.paragraph_format.space_after = Pt(6)
            clean = line.replace("> ", "").replace("**", "")
            r = p.add_run(clean)
            r.font.size = Pt(10.5)
            r.font.color.rgb = RGBColor(15, 23, 42)
        elif line.strip().startswith("- ") or line.strip().startswith("* "):
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_after = Pt(3)
            clean = line.strip().lstrip("-* ").replace("**", "")
            r = p.add_run(clean)
            r.font.size = Pt(10)
        elif line.strip():
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(4)
            clean = line.replace("**", "")
            r = p.add_run(clean)
            r.font.size = Pt(10)

    doc.save(DOCX_OUT)
    print(f"Generated DOCX: {DOCX_OUT}")

def build_pdf():
    class SimpleCanvas(canvas.Canvas):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._saved_page_states = []

        def showPage(self):
            self._saved_page_states.append(dict(self.__dict__))
            self._startPage()

        def save(self):
            num = len(self._saved_page_states)
            for state in self._saved_page_states:
                self.__dict__.update(state)
                self.draw_decorations(num)
                super().showPage()
            super().save()

        def draw_decorations(self, count):
            self.saveState()
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(54, 750, "ShalaConnect Cloud-Native Video Demonstration Script")
            self.drawRightString(558, 750, "Yash Sabale | PRN: 202301040087")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            self.drawString(54, 40, "MIT Academy of Engineering, Pune")
            self.drawRightString(558, 40, f"Page {self._pageNumber} of {count}")
            self.line(54, 50, 558, 50)
            self.restoreState()

    doc = SimpleDocTemplate(str(PDF_OUT), pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
    styles = getSampleStyleSheet()

    body = ParagraphStyle('B', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, textColor=colors.HexColor("#1E293B"), spaceAfter=6)
    head1 = ParagraphStyle('H1', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=13, leading=17, textColor=colors.HexColor("#0284C7"), spaceBefore=12, spaceAfter=6)
    quote = ParagraphStyle('Q', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, textColor=colors.HexColor("#0F172A"), leftIndent=16, spaceAfter=8)

    story = [
        Paragraph("<b>🎬 Video Demonstration Script (5 to 8 Minutes)</b>", head1),
        Paragraph("<b>Containerization &amp; Kubernetes Deployment Demonstration</b>", body),
        Paragraph("Student: Yash Janardan Sabale | PRN: 202301040087 | MITAOE Pune", body),
        HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0284C7"), spaceAfter=10),
    ]

    content = DOC_MD.read_text(encoding="utf-8")
    for line in content.splitlines():
        if line.startswith("# ") or line.startswith("## ") or line.startswith("### "):
            clean = md_to_xml(line.lstrip("#").strip())
            story.append(Paragraph(f"<b>{clean}</b>", head1))
        elif line.startswith("> "):
            clean = md_to_xml(line.replace("> ", ""))
            story.append(Paragraph(clean, quote))
        elif line.strip().startswith("- ") or line.strip().startswith("* "):
            clean = md_to_xml(line.strip().lstrip("-* "))
            story.append(Paragraph(f"• {clean}", body))
        elif line.strip():
            clean = md_to_xml(line)
            story.append(Paragraph(clean, body))

    doc.build(story, canvasmaker=SimpleCanvas)
    print(f"Generated PDF: {PDF_OUT}")

if __name__ == "__main__":
    build_docx()
    build_pdf()
