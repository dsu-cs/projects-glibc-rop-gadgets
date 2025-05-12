#!/usr/bin/env python3
import os
import re

def update_index_html():
    # Find all arch-version.txt files in current directory
    files = [f for f in os.listdir('.') if re.match(r'^[a-zA-Z0-9]+-\d+\.\d+\.txt$', f)]
    
    if not files:
        print("No arch-version.txt files found in current directory")
        return
    
    # Parse versions and architectures
    versions = set()
    architectures = set()
    
    for file in files:
        # Remove .txt extension and split
        base = file[:-4]
        arch, version = base.split('-', 1)
        architectures.add(arch)
        versions.add(version)
    
    # Sort versions numerically and architectures alphabetically
    versions = sorted(versions, key=lambda v: [int(num) for num in v.split('.')])
    architectures = sorted(architectures)
    
    # Read the original index.html
    with open('index.html', 'r') as f:
        content = f.read()
    
    # Generate versions radio buttons HTML
    versions_html = []
    versions_html.append('<div id="versions-div">')
    versions_html.append('<h3>Glibc Version:</h3>')
    for version in versions:
        checked = ' checked' if version == max(versions) else ''
        versions_html.append(f'<label><input type="radio" name="version" value="{version}"{checked}> {version}</label>')
    versions_html.append('</div>')
    versions_html = '\n'.join(versions_html)
    
    # Generate architectures radio buttons HTML
    arch_html = []
    arch_html.append('<div id="arch-div">')
    arch_html.append('<h3>Architecture:</h3>')
    for arch in architectures:
        checked = ' checked' if arch == architectures[0] else ''
        arch_html.append(f'<label><input type="radio" name="arch" value="{arch}"{checked}> {arch}</label>')
    arch_html.append('</div>')
    arch_html = '\n'.join(arch_html)
    
    # Remove ALL existing versions and arch sections
    # First remove the entire versions section
    content = re.sub(
        r'<div id="versions-div">.*?</div>',
        '',
        content,
        flags=re.DOTALL
    )
    # Then remove the entire arch section
    content = re.sub(
        r'<div id="arch-div">.*?</div>',
        '',
        content,
        flags=re.DOTALL
    )
    
    # Remove any loose h3 labels that might remain
    content = re.sub(
        r'<h3>Glibc Version:</h3>',
        '',
        content
    )
    content = re.sub(
        r'<h3>Architecture:</h3>',
        '',
        content
    )
    
    # Find the position to insert the radio buttons (after the h1 tag)
    h1_end = content.find('</h1>')
    if h1_end == -1:
        print("Couldn't find </h1> tag in index.html")
        return
    
    # Insert new divs after the h1 tag
    h1_end += len('</h1>')
    content = content[:h1_end] + '\n' + versions_html + '\n' + arch_html + '\n' + content[h1_end:]
    
    # Write the updated file
    with open('index.html', 'w') as f:
        f.write(content)
    
    print(f"Updated index.html with {len(versions)} versions and {len(architectures)} architectures")

if __name__ == '__main__':
    update_index_html()
