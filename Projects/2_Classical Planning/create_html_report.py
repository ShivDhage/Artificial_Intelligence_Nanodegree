#!/usr/bin/env python3
"""
Convert markdown report to HTML that can be printed to PDF
"""

import re

def markdown_to_html(md_file, html_file):
    """Convert markdown to HTML"""
    
    with open(md_file, 'r') as f:
        content = f.read()
    
    # Convert markdown to HTML
    html_lines = [
        '<!DOCTYPE html>',
        '<html>',
        '<head>',
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '<title>Classical Planning Project Report</title>',
        '<style>',
        'body { font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; line-height: 1.6; color: #333; }',
        'h1 { color: #003366; text-align: center; border-bottom: 3px solid #003366; padding-bottom: 10px; }',
        'h2 { color: #003366; margin-top: 30px; border-left: 4px solid #0055AA; padding-left: 10px; }',
        'h3 { color: #0055AA; margin-top: 15px; }',
        'code { background-color: #f5f5f5; padding: 2px 6px; border-radius: 3px; font-family: "Courier New"; }',
        'pre { background-color: #f5f5f5; padding: 12px; border-left: 4px solid #0055AA; overflow-x: auto; }',
        'table { border-collapse: collapse; width: 100%; margin: 15px 0; }',
        'table th { background-color: #003366; color: white; padding: 10px; text-align: left; }',
        'table td { border: 1px solid #ddd; padding: 8px; }',
        'table tr:nth-child(even) { background-color: #f9f9f9; }',
        'ul, ol { margin: 10px 0; padding-left: 30px; }',
        'li { margin: 5px 0; }',
        'blockquote { border-left: 4px solid #ddd; margin: 15px 0; padding-left: 15px; color: #666; font-style: italic; }',
        '.toc { background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0; }',
        '.toc h3 { margin-top: 0; }',
        '@media print { body { max-width: 100%; } h2 { page-break-after: avoid; } table { page-break-inside: avoid; } }',
        '</style>',
        '</head>',
        '<body>',
    ]
    
    lines = content.split('\n')
    i = 0
    in_code = False
    
    while i < len(lines):
        line = lines[i].rstrip()
        
        # Code blocks
        if line.strip().startswith('```'):
            if in_code:
                html_lines.append('</pre>')
                in_code = False
            else:
                html_lines.append('<pre><code>')
                in_code = True
            i += 1
            continue
        
        if in_code:
            html_lines.append(line.replace('<', '&lt;').replace('>', '&gt;'))
            i += 1
            continue
        
        # Titles and headings
        if line.startswith('# ') and i == 0:
            title = line[2:].strip()
            html_lines.append(f'<h1>{title}</h1>')
            i += 1
            continue
        
        if line.startswith('# '):
            heading = line[2:].strip()
            html_lines.append(f'<h2>{heading}</h2>')
            i += 1
            continue
        
        if line.startswith('## '):
            heading = line[3:].strip()
            html_lines.append(f'<h2>{heading}</h2>')
            i += 1
            continue
        
        if line.startswith('### '):
            heading = line[4:].strip()
            html_lines.append(f'<h3>{heading}</h3>')
            i += 1
            continue
        
        # Tables
        if line.startswith('|'):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                row = [cell.strip() for cell in lines[i].split('|')[1:-1]]
                table_lines.append(row)
                i += 1
            
            # Skip separator
            if len(table_lines) > 1:
                if all('---' in cell or '-' in cell for cell in table_lines[1]):
                    table_lines.pop(1)
            
            if table_lines:
                html_lines.append('<table>')
                # Header
                html_lines.append('<tr>')
                for cell in table_lines[0]:
                    html_lines.append(f'<th>{cell}</th>')
                html_lines.append('</tr>')
                # Body
                for row in table_lines[1:]:
                    html_lines.append('<tr>')
                    for cell in row:
                        html_lines.append(f'<td>{cell}</td>')
                    html_lines.append('</tr>')
                html_lines.append('</table>')
            continue
        
        # Bullet points
        if line.startswith('- '):
            bullet_text = line[2:].strip()
            html_lines.append(f'<li>{bullet_text}</li>')
            i += 1
            continue
        
        # Horizontal rules
        if line.strip().startswith('---'):
            html_lines.append('<hr>')
            i += 1
            continue
        
        # Regular paragraphs
        if line.strip():
            # Format inline code and bold
            line = re.sub(r'`([^`]+)`', r'<code>\1</code>', line)
            line = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', line)
            line = re.sub(r'_([^_]+)_', r'<em>\1</em>', line)
            
            html_lines.append(f'<p>{line}</p>')
            i += 1
        else:
            i += 1
    
    html_lines.extend([
        '</body>',
        '</html>'
    ])
    
    # Write HTML file
    with open(html_file, 'w') as f:
        f.write('\n'.join(html_lines))
    
    print(f"✓ HTML report created: {html_file}")
    print(f"  To convert to PDF, open in a browser and use Print > Save as PDF")

if __name__ == '__main__':
    markdown_to_html('report.md', 'report.html')
