#!/usr/bin/env python3
"""
Generate a professional PDF report from markdown content
Uses reportlab library for better formatting
"""

def generate_professional_pdf():
    """Generate a well-formatted PDF report"""
    
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
        from reportlab.lib import colors
        from reportlab.pdfgen import canvas
    except ImportError:
        print("reportlab not available, trying alternative method...")
        return generate_simple_pdf()
    
    # Read markdown report
    with open('report.md', 'r') as f:
        content = f.read()
    
    # Create PDF
    pdf_file = "report.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=letter,
                           topMargin=0.75*inch, bottomMargin=0.75*inch,
                           leftMargin=0.75*inch, rightMargin=0.75*inch)
    
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        leading=35
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold',
        leading=20
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#2e5c9a'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    
    heading3_style = ParagraphStyle(
        'CustomHeading3',
        parent=styles['Heading3'],
        fontSize=11,
        textColor=colors.HexColor('#2e5c9a'),
        spaceAfter=8,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=10,
        leading=14
    )
    
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontSize=10,
        leftIndent=20,
        spaceAfter=6,
        leading=12
    )
    
    # Parse markdown and add to elements
    lines = content.split('\n')
    i = 0
    in_table = False
    
    while i < len(lines):
        line = lines[i].rstrip()
        
        # Title (first # only)
        if line.startswith('# ') and i < 5:
            title = line[2:].strip()
            elements.append(Paragraph(title, title_style))
            elements.append(Spacer(1, 0.3*inch))
            i += 1
            continue
        
        # Skip title if already added
        if line.startswith('# '):
            i += 1
            continue
        
        # Heading 1
        if line.startswith('## '):
            heading = line[3:].strip()
            elements.append(Spacer(1, 0.2*inch))
            elements.append(Paragraph(heading, heading1_style))
            i += 1
            continue
        
        # Heading 2
        if line.startswith('### '):
            heading = line[4:].strip()
            elements.append(Paragraph(heading, heading2_style))
            i += 1
            continue
        
        # Heading 3
        if line.startswith('#### '):
            heading = line[5:].strip()
            elements.append(Paragraph(f"<b>{heading}</b>", heading3_style))
            i += 1
            continue
        
        # Tables
        if line.strip().startswith('|'):
            table_data = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                row = [cell.strip() for cell in lines[i].split('|')[1:-1]]
                table_data.append(row)
                i += 1
            
            # Remove separator row
            if len(table_data) > 1 and all('---' in cell or '-' in cell for cell in table_data[1]):
                table_data.pop(1)
            
            if table_data:
                # Calculate column widths
                col_count = len(table_data[0])
                col_width = (7.5 * inch) / col_count
                
                # Create table
                table = Table(table_data, colWidths=[col_width] * col_count)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f4f8')),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
                ]))
                
                elements.append(Spacer(1, 0.15*inch))
                elements.append(table)
                elements.append(Spacer(1, 0.2*inch))
            continue
        
        # Bullet points
        if line.strip().startswith('- '):
            bullet_text = line[2:].strip()
            elements.append(Paragraph(f"• {bullet_text}", bullet_style))
            i += 1
            continue
        
        # Numbered lists
        import re
        if re.match(r'^\d+\. ', line.strip()):
            text = re.sub(r'^\d+\. ', '', line.strip())
            elements.append(Paragraph(f"<b>{line.split('.')[0]}.</b> {text}", bullet_style))
            i += 1
            continue
        
        # Horizontal rule
        if line.strip().startswith('---'):
            elements.append(Spacer(1, 0.15*inch))
            elements.append(PageBreak())
            i += 1
            continue
        
        # Code blocks
        if line.strip().startswith('```'):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            if code_lines:
                code_text = '<br/>'.join(code_lines[:20])  # Limit to 20 lines
                code_style = ParagraphStyle(
                    'Code',
                    parent=styles['Normal'],
                    fontSize=8,
                    fontName='Courier',
                    leftIndent=10,
                    rightIndent=10,
                    spaceAfter=10,
                    textColor=colors.HexColor('#333333'),
                    backColor=colors.HexColor('#f5f5f5'),
                    borderPadding=5
                )
                elements.append(Paragraph(code_text, code_style))
                elements.append(Spacer(1, 0.1*inch))
            i += 1
            continue
        
        # Regular paragraphs
        if line.strip() and not line.startswith('---'):
            # Format inline code and emphasis
            line = re.sub(r'`([^`]+)`', r'<code>\1</code>', line)
            line = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', line)
            line = re.sub(r'_([^_]+)_', r'<i>\1</i>', line)
            line = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', line)  # Remove links but keep text
            
            elements.append(Paragraph(line, normal_style))
            i += 1
        else:
            i += 1
    
    # Build PDF
    try:
        doc.build(elements)
        print(f"✓ Professional PDF report created: report.pdf")
        return True
    except Exception as e:
        print(f"✗ Error building PDF: {e}")
        return False

def generate_simple_pdf():
    """Fallback to simple PDF generation if reportlab not available"""
    print("Generating basic PDF...")
    
    with open('report.md', 'r') as f:
        content = f.read()
    
    # Create basic PDF
    pdf_content = b"""%PDF-1.4
1 0 obj
<</Type /Catalog /Pages 2 0 R>>
endobj
2 0 obj
<</Type /Pages /Kids [3 0 R] /Count 1>>
endobj
3 0 obj
<</Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources <</Font <</F1 5 0 R /F2 6 0 R>>>>>>
endobj
4 0 obj
<</Length 10000>>
stream
BT
/F2 14 Tf
50 750 Td
(Classical Planning Project Report) Tj
0 -30 Td
/F1 11 Tf
"""
    
    lines = content.split('\n')[:150]
    for line in lines:
        line = line.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
        if line.strip():
            if len(line) > 85:
                line = line[:85]
            pdf_content += f"({line}) Tj\n".encode()
            pdf_content += b"0 -14 Td\n"
    
    pdf_content += b"""ET
endstream
endobj
5 0 obj
<</Type /Font /Subtype /Type1 /BaseFont /Helvetica>>
endobj
6 0 obj
<</Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold>>
endobj
xref
0 7
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000272 00000 n 
0000010370 00000 n 
0000010468 00000 n 
trailer
<</Size 7 /Root 1 0 R>>
startxref
10567
%%EOF"""
    
    with open('report.pdf', 'wb') as f:
        f.write(pdf_content)
    print("✓ Basic PDF report created: report.pdf")
    return True

if __name__ == '__main__':
    try:
        success = generate_professional_pdf()
        if not success:
            generate_simple_pdf()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
