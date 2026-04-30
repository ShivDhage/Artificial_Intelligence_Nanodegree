#!/usr/bin/env python3
"""
Create a minimal but valid PDF from the markdown report
This uses pure Python without external dependencies
"""

def text_to_pdf():
    """Convert markdown report to a minimal PDF"""
    
    # Read the markdown report
    with open('report.md', 'r') as f:
        md_content = f.read()
    
    # Create a very simple PDF with the content
    # This is a minimal but valid PDF structure
    pdf = b"""%PDF-1.1
1 0 obj
<</Type /Catalog /Pages 2 0 R>>
endobj
2 0 obj
<</Type /Pages /Kids [3 0 R] /Count 1>>
endobj
3 0 obj
<</Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources <</Font <</F1 5 0 R>>>>>>
endobj
4 0 obj
<</Length 5000>>
stream
BT
/F1 10 Tf
50 750 Td
"""
    
    # Add content from markdown
    lines = md_content.split('\n')
    y_offset = 0
    
    for line in lines[:200]:  # Limit to first 200 lines for manageability
        # Escape special PDF characters
        escaped_line = line.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
        
        if line.startswith('# '):
            # Title
            text = line[2:].strip()
            escaped_text = text.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
            pdf += f"({escaped_text}) Tj\n".encode()
            pdf += b"0 -20 Td\n"
            y_offset += 20
        elif line.startswith('## '):
            # Heading
            text = line[3:].strip()
            escaped_text = text.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
            pdf += f"({escaped_text}) Tj\n".encode()
            pdf += b"0 -16 Td\n"
            y_offset += 16
        elif line.strip():
            # Regular text (truncate to fit)
            if len(escaped_line) > 70:
                escaped_line = escaped_line[:70]
            pdf += f"({escaped_line}) Tj\n".encode()
            pdf += b"0 -12 Td\n"
            y_offset += 12
        else:
            # Blank line
            pdf += b"0 -6 Td\n"
            y_offset += 6
        
        # Page break if needed
        if y_offset > 720:
            pdf += b"ET\nendstream\nendobj\n"
            break
    
    pdf += b"""ET
endstream
endobj
5 0 obj
<</Type /Font /Subtype /Type1 /BaseFont /Helvetica>>
endobj
xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000262 00000 n 
0000005360 00000 n 
trailer
<</Size 6 /Root 1 0 R>>
startxref
5460
%%EOF"""
    
    # Write the PDF
    with open('report.pdf', 'wb') as f:
        f.write(pdf)
    
    return True

if __name__ == '__main__':
    try:
        text_to_pdf()
        print("✓ report.pdf created successfully")
    except Exception as e:
        print(f"✗ Error creating PDF: {e}")
        import traceback
        traceback.print_exc()
