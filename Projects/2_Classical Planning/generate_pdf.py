#!/usr/bin/env python3
"""
Convert markdown report to PDF using reportlab
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib import colors
import re

def create_pdf_report():
    """Create PDF report from markdown content"""
    
    # Read markdown file
    with open('report.md', 'r') as f:
        content = f.read()
    
    # Create PDF
    pdf_filename = "report.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter,
                           topMargin=0.75*inch, bottomMargin=0.75*inch,
                           leftMargin=0.75*inch, rightMargin=0.75*inch)
    
    # Container for PDF elements
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#003366'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Custom heading styles
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#003366'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#0055AA'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=8
    )
    
    code_style = ParagraphStyle(
        'Code',
        parent=styles['Normal'],
        fontSize=8,
        fontName='Courier',
        leftIndent=20,
        spaceAfter=6,
        textColor=colors.HexColor('#333333'),
        backColor=colors.HexColor('#F0F0F0')
    )
    
    # Parse and add content
    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        
        # Title
        if line.startswith('# ') and i == 0:
            title = line[2:].strip()
            elements.append(Paragraph(title, title_style))
            elements.append(Spacer(1, 0.3*inch))
            i += 1
            continue
        
        # Heading 1
        if line.startswith('# '):
            heading = line[2:].strip()
            elements.append(Spacer(1, 0.2*inch))
            elements.append(Paragraph(heading, heading1_style))
            i += 1
            continue
        
        # Heading 2
        if line.startswith('## '):
            heading = line[3:].strip()
            elements.append(Spacer(1, 0.15*inch))
            elements.append(Paragraph(heading, heading2_style))
            i += 1
            continue
        
        # Heading 3
        if line.startswith('### '):
            heading = line[4:].strip()
            elements.append(Paragraph(f"<b>{heading}</b>", normal_style))
            i += 1
            continue
        
        # Table (markdown format)
        if line.startswith('|'):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                row = [cell.strip() for cell in lines[i].split('|')[1:-1]]
                table_lines.append(row)
                i += 1
            
            # Skip separator row
            if len(table_lines) > 1:
                if all('---' in cell or '-' in cell for cell in table_lines[1]):
                    table_lines.pop(1)
            
            if table_lines:
                table = Table(table_lines, colWidths=[2*inch]*len(table_lines[0]))
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F5F5F5')),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9F9F9')])
                ]))
                elements.append(Spacer(1, 0.1*inch))
                elements.append(table)
                elements.append(Spacer(1, 0.2*inch))
            continue
        
        # Code block (```...```)
        if line.strip().startswith('```'):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            if code_lines:
                code_text = '\n'.join(code_lines)
                elements.append(Paragraph(f"<font face='Courier' size='8'>{code_text}</font>", code_style))
                elements.append(Spacer(1, 0.1*inch))
            i += 1
            continue
        
        # Bullet point
        if line.startswith('- '):
            bullet_text = line[2:].strip()
            elements.append(Paragraph(f"• {bullet_text}", normal_style))
            i += 1
            continue
        
        # Numbered list
        if re.match(r'^\d+\. ', line):
            num_text = line.split('. ', 1)[1].strip()
            elements.append(Paragraph(f"{line.split('.')[0]}. {num_text}", normal_style))
            i += 1
            continue
        
        # Regular paragraph
        if line.strip() and not line.startswith('---'):
            elements.append(Paragraph(line.strip(), normal_style))
            i += 1
        elif line.strip() == '':
            elements.append(Spacer(1, 0.1*inch))
            i += 1
        else:
            i += 1
    
    # Build PDF
    try:
        doc.build(elements)
        print(f"✓ PDF report created: {pdf_filename}")
        return True
    except Exception as e:
        print(f"✗ Error creating PDF: {e}")
        return False

if __name__ == '__main__':
    create_pdf_report()
