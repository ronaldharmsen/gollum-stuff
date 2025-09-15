#!/usr/bin/env python3
"""
This script extracts Mermaid code blocks from all .md files in the current directory,
generates SVG images using the Mermaid CLI (mmdc), and replaces the code blocks with image links.
"""
import os
import re
import subprocess

MERMAID_BLOCK_RE = re.compile(r'```mermaid\s*([\s\S]+?)```', re.MULTILINE)

def process_markdown_file(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    matches = list(MERMAID_BLOCK_RE.finditer(content))
    if not matches:
        return False

    new_content = content
    for i, match in enumerate(matches, 1):
        mermaid_code = match.group(1)
        img_filename = f"{os.path.splitext(os.path.basename(md_path))[0]}-mermaid-{i}.svg"
        img_path = os.path.join(os.path.dirname(md_path), img_filename)
        # Write Mermaid code to temp file
        with open('tmp.mmd', 'w', encoding='utf-8') as tmp:
            tmp.write(mermaid_code)
        # Generate SVG with mmdc
    subprocess.run(['mmdc', '-i', 'tmp.mmd', '-o', img_path, '--puppeteerConfigFile', '../main-repo/puppeteer-config.json'], check=True)
    # Replace code block with image link
    new_content = new_content.replace(match.group(0), f'![Mermaid diagram]({img_filename})')
    # Remove temp file
    if os.path.exists('tmp.mmd'):
        os.remove('tmp.mmd')
    # Write updated markdown
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

def main():
    for filename in os.listdir('.'):
        if filename.endswith('.md'):
            process_markdown_file(filename)

if __name__ == '__main__':
    main()
