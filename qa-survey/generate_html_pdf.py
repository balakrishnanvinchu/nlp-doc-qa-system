#!/usr/bin/env python3
"""
Convert markdown literature review to high-quality PDF using HTML template
This approach preserves tables, diagrams, and formatting properly

Usage:
    python generate_html_pdf.py <input_md_file> [output_html_file] [output_pdf_file]

Examples:
    python generate_html_pdf.py Literature_Review_QA_Systems.md
    python generate_html_pdf.py input.md output.html output.pdf
"""
import os
import re
import sys
from pathlib import Path

def create_html_from_markdown(md_file):
    """Convert markdown to beautifully formatted HTML"""
    
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # HTML template with professional styling
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Literature Review: Extractive and Abstractive Question Answering</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.7;
                color: #2c3e50;
                background-color: #ffffff;
            }}
            
            .container {{
                max-width: 900px;
                margin: 0 auto;
                padding: 40px 30px;
            }}
            
            h1 {{
                color: #1a5c9e;
                font-size: 28px;
                margin: 30px 0 20px 0;
                padding-bottom: 15px;
                border-bottom: 3px solid #1a5c9e;
                page-break-after: avoid;
            }}
            
            h2 {{
                color: #2980b9;
                font-size: 22px;
                margin: 25px 0 15px 0;
                padding-top: 10px;
                page-break-after: avoid;
            }}
            
            h3 {{
                color: #3498db;
                font-size: 18px;
                margin: 18px 0 12px 0;
                page-break-after: avoid;
            }}
            
            h4 {{
                color: #34495e;
                font-size: 15px;
                margin: 12px 0 8px 0;
                page-break-after: avoid;
            }}
            
            p {{
                margin: 12px 0;
                text-align: justify;
            }}
            
            ul, ol {{
                margin: 15px 0 15px 30px;
            }}
            
            li {{
                margin: 8px 0;
            }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                page-break-inside: avoid;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            
            th {{
                background-color: #2980b9;
                color: white;
                padding: 12px;
                text-align: left;
                font-weight: 600;
                border: 1px solid #2c3e50;
            }}
            
            td {{
                padding: 10px 12px;
                border: 1px solid #ecf0f1;
                background-color: #f9f9f9;
            }}
            
            tr:nth-child(even) td {{
                background-color: #f5f5f5;
            }}
            
            tr:hover td {{
                background-color: #f0f7ff;
            }}
            
            code {{
                background-color: #f4f4f4;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
                color: #c7254e;
            }}
            
            pre {{
                background-color: #f4f4f4;
                border-left: 4px solid #2980b9;
                padding: 12px;
                margin: 15px 0;
                border-radius: 4px;
                overflow-x: auto;
                page-break-inside: avoid;
                font-family: 'Courier New', monospace;
                font-size: 12px;
            }}
            
            blockquote {{
                border-left: 4px solid #3498db;
                padding-left: 15px;
                margin: 15px 0;
                color: #555;
                font-style: italic;
            }}
            
            .diagram {{
                background-color: #ecf0f1;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 15px;
                margin: 20px 0;
                page-break-inside: avoid;
                font-family: 'Courier New', monospace;
                font-size: 11px;
                white-space: pre;
                overflow-x: auto;
            }}
            
            .metrics {{
                background-color: #e8f4f8;
                border-left: 4px solid #16a085;
                padding: 15px;
                margin: 15px 0;
                page-break-inside: avoid;
            }}
            
            .highlight {{
                background-color: #fffacd;
                padding: 2px 4px;
                border-radius: 2px;
            }}
            
            strong {{
                color: #2c3e50;
                font-weight: 600;
            }}
            
            em {{
                color: #34495e;
                font-style: italic;
            }}
            
            hr {{
                border: none;
                border-top: 2px solid #ecf0f1;
                margin: 30px 0;
                page-break-after: avoid;
            }}
            
            .section {{
                page-break-inside: avoid;
            }}
            
            .key-result {{
                background-color: #d5f4e6;
                border-left: 4px solid #27ae60;
                padding: 12px;
                margin: 10px 0;
                page-break-inside: avoid;
            }}
            
            .warning {{
                background-color: #fadbd8;
                border-left: 4px solid #e74c3c;
                padding: 12px;
                margin: 10px 0;
            }}
            
            a {{
                color: #2980b9;
                text-decoration: none;
            }}
            
            a:hover {{
                text-decoration: underline;
            }}
            
            @media print {{
                body {{
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    padding: 20px;
                }}
                h1, h2, h3 {{
                    page-break-after: avoid;
                }}
                table, pre, .diagram {{
                    page-break-inside: avoid;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            {content}
        </div>
    </body>
    </html>
    """
    
    # Convert markdown to HTML
    html_content = convert_markdown_to_html(content)
    
    # Combine with template
    final_html = html_template.format(content=html_content)
    
    return final_html

def convert_markdown_to_html(md_text):
    """Convert markdown elements to HTML"""
    
    lines = md_text.split('\n')
    html_lines = []
    in_table = False
    in_code_block = False
    in_list = False
    code_block_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Code blocks (```...```)
        if line.strip().startswith('```'):
            if not in_code_block:
                in_code_block = True
                code_block_lines = []
                i += 1
                continue
            else:
                in_code_block = False
                code_block_content = '\n'.join(code_block_lines)
                code_block_content = escape_html(code_block_content)
                html_lines.append(f'<pre class="diagram">{code_block_content}</pre>')
                code_block_lines = []
                i += 1
                continue
        
        if in_code_block:
            code_block_lines.append(line)
            i += 1
            continue
        
        # Tables
        if '|' in line and not line.strip().startswith('#'):
            if not in_table:
                in_table = True
                html_lines.append('<table>')
            
            # Parse table row
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            
            if i + 1 < len(lines) and '---' in lines[i + 1]:
                # Header row
                html_lines.append('<tr>')
                for cell in cells:
                    cell = cell.replace('**', '<strong>').replace('*', '<em>')
                    html_lines.append(f'<th>{cell}</th>')
                html_lines.append('</tr>')
                i += 2
                continue
            elif in_table:
                html_lines.append('<tr>')
                for cell in cells:
                    cell = cell.replace('**', '<strong>').replace('*', '<em>')
                    html_lines.append(f'<td>{cell}</td>')
                html_lines.append('</tr>')
                i += 1
                continue
        elif in_table:
            in_table = False
            html_lines.append('</table>')
        
        # Headings
        if line.startswith('# '):
            title = line[2:].strip()
            html_lines.append(f'<h1>{escape_html(title)}</h1>')
        elif line.startswith('## '):
            heading = line[3:].strip()
            html_lines.append(f'<h2>{escape_html(heading)}</h2>')
        elif line.startswith('### '):
            heading = line[4:].strip()
            html_lines.append(f'<h3>{escape_html(heading)}</h3>')
        elif line.startswith('#### '):
            heading = line[5:].strip()
            html_lines.append(f'<h4>{escape_html(heading)}</h4>')
        
        # Horizontal rule
        elif line.startswith('---'):
            html_lines.append('<hr>')
        
        # List items
        elif line.strip().startswith('- '):
            if not in_list:
                in_list = True
                html_lines.append('<ul>')
            
            item = line.strip()[2:]
            item = apply_markdown_formatting(item)
            html_lines.append(f'<li>{item}</li>')
        
        elif in_list and line.strip() and not line.strip().startswith('- '):
            in_list = False
            html_lines.append('</ul>')
            
            if line.strip():
                para = apply_markdown_formatting(line)
                html_lines.append(f'<p>{para}</p>')
        
        # Paragraphs
        elif line.strip():
            para = apply_markdown_formatting(line)
            html_lines.append(f'<p>{para}</p>')
        
        # Empty lines
        else:
            html_lines.append('')
        
        i += 1
    
    # Close any open elements
    if in_list:
        html_lines.append('</ul>')
    if in_table:
        html_lines.append('</table>')
    
    return '\n'.join(html_lines)

def apply_markdown_formatting(text):
    """Apply markdown formatting to text"""
    text = escape_html(text)
    # Bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__(.*?)__', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    text = re.sub(r'_(.*?)_', r'<em>\1</em>', text)
    # Code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # Links
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)
    return text

def escape_html(text):
    """Escape HTML special characters"""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#39;'))

if __name__ == '__main__':
    # Parse command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python generate_html_pdf.py <input_md_file> [output_html_file] [output_pdf_file]")
        print("\nExamples:")
        print("  python generate_html_pdf.py Literature_Review_QA_Systems.md")
        print("  python generate_html_pdf.py input.md output.html output.pdf")
        sys.exit(1)
    
    # Get input markdown file
    md_file = sys.argv[1]
    
    # Check if input file exists
    if not os.path.exists(md_file):
        print(f"✗ Error: Input file '{md_file}' not found!")
        sys.exit(1)
    
    # Generate output filenames
    if len(sys.argv) >= 3:
        html_file = sys.argv[2]
    else:
        # If not specified, use same name with .html extension
        base_name = os.path.splitext(md_file)[0]
        html_file = f"{base_name}.html"
    
    if len(sys.argv) >= 4:
        pdf_file = sys.argv[3]
    else:
        # If not specified, use same name with .pdf extension
        base_name = os.path.splitext(md_file)[0]
        pdf_file = f"{base_name}.pdf"
    
    print(f"Converting {md_file} to HTML...")
    print(f"  Input:  {os.path.abspath(md_file)}")
    print(f"  Output: {os.path.abspath(html_file)}")
    
    try:
        html_content = create_html_from_markdown(md_file)
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✓ HTML generated successfully: {html_file}")
        print(f"  File size: {os.path.getsize(html_file) / 1024:.1f} KB")
        
        # Convert HTML to PDF using weasyprint
        print("\nConverting HTML to PDF using weasyprint...")
        
        try:
            from weasyprint import HTML
            
            HTML(string=open(html_file).read()).write_pdf(pdf_file)
            
            pdf_size = os.path.getsize(pdf_file) / 1024 / 1024
            print(f"✓ PDF created successfully: {pdf_file}")
            print(f"  File size: {pdf_size:.2f} MB")
            
        except ImportError:
            print("⚠ weasyprint not available")
            print(f"✓ However, HTML file is ready and can be opened in any browser")
            print(f"  You can print it to PDF from your browser (Ctrl+P or Cmd+P)")
        except Exception as e:
            print(f"⚠ Could not create PDF: {e}")
            print(f"✓ However, HTML file is ready! Open it in your browser and print to PDF")
            
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
