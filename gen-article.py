#!/usr/bin/env python3
"""Generate SEO article HTML files from a template."""
import sys, json

def generate(filename, title, meta_desc, h1, breadcrumb_text, body_html, related_html):
    # Read template parts
    with open('tegn-darlig-ventilasjon.html','r') as f:
        tpl = f.read()
    
    main_start = tpl.find('<main class="content">')
    main_end = tpl.find('</main>') + len('</main>')
    header = tpl[:main_start]
    footer = tpl[main_end:]
    
    # Replace title
    import re
    header = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', header)
    header = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{meta_desc}">', header)
    header = re.sub(r'<link rel="canonical" href=".*?">', f'<link rel="canonical" href="https://ventrensberg.no/{filename}.html">', header)
    
    # Replace JSON-LD Article
    header = re.sub(
        r'"headline":\s*".*?"',
        f'"headline": "{h1}"',
        header
    )
    header = re.sub(
        r'("description":\s*)".*?"(,\s*"author")',
        f'\\1"{meta_desc}"\\2',
        header
    )
    
    # Replace breadcrumb name in JSON-LD
    header = re.sub(
        r'("position": 2,\s*"name":\s*)".*?"',
        f'\\1"{breadcrumb_text}"',
        header
    )
    header = re.sub(
        r'("position": 2,[\s\S]*?"item":\s*)".*?"',
        f'\\1"https://ventrensberg.no/{filename}.html"',
        header
    )
    
    # Build main content
    main = f'''    <main class="content">
        <nav class="breadcrumb" aria-label="Brødsmuler"><a href="index.html">Hjem</a> <span>/</span> {breadcrumb_text}</nav>
        <h1>{h1}</h1>
{body_html}

        <div style="margin-top:3rem;padding-top:2rem;border-top:1px solid var(--border);">
            <h2 style="font-size:1.2rem;margin-bottom:1rem;">Relaterte artikler</h2>
            <ul style="list-style:none;padding:0;">
{related_html}
            </ul>
        </div>

        <div style="background:var(--accent-subtle);border-radius:8px;padding:2rem;text-align:center;margin-top:3rem;">
            <h2 style="font-size:1.3rem;color:var(--primary);margin-bottom:.5rem;">Klar for å sammenligne tilbud?</h2>
            <p style="color:var(--text-secondary);margin-bottom:1.25rem;">Få 3 uforpliktende tilbud fra kvalitetssjekkede firmaer i Bergen.</p>
            <a href="index.html#skjema" style="display:inline-block;background:var(--accent);color:var(--white);padding:.85rem 2rem;border-radius:6px;font-weight:600;text-decoration:none;">Sammenlign tilbud nå</a>
        </div>
    </main>
'''
    
    with open(f'{filename}.html', 'w') as f:
        f.write(header + main + footer)
    print(f'Created {filename}.html')

if __name__ == '__main__':
    # Usage: python3 gen-article.py config.json
    with open(sys.argv[1]) as f:
        articles = json.load(f)
    for a in articles:
        generate(a['filename'], a['title'], a['meta'], a['h1'], a['breadcrumb'], a['body'], a['related'])
