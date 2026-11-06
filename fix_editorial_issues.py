import os
import re

base_dir = "/Users/devonshigaki/Developer/trust-stack-research-collection"

def fix_file(filepath, fixes):
    if not os.path.exists(filepath): return
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    for old, new in fixes:
        if callable(old):
            content = old(content)
        else:
            content = content.replace(old, new)
            
    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Fixed {filepath}")

# 1. Replace [insert] with TBD DOIs
def fix_dois(content):
    return content.replace("[insert]", "10.17605/OSF.IO/TBD").replace("\\[insert\\]", "10.17605/OSF.IO/TBD")

for root, _, files in os.walk(os.path.join(base_dir, "papers")):
    for file in files:
        if file.endswith(".md") or file.endswith(".tex"):
            filepath = os.path.join(root, file)
            fix_file(filepath, [(fix_dois, None)])

# 2. Fix dangling punctuation in the_value_of_trust.md
vot_md = os.path.join(base_dir, "papers/markdown/the_value_of_trust.md")
fix_file(vot_md, [
    ("\xa0.", "."),
    ("\xa0 (a working paper);", " (a working paper);"),
    ("\xa0;", ";"),
])
vot_tex = os.path.join(base_dir, "papers/source/value_of_trust.tex")
fix_file(vot_tex, [
    ("~.", "."),
    ("~ (a working paper);", " (a working paper);"),
    ("~;", ";"),
])

# 3. Fix cross-references in docas.md
docas_md = os.path.join(base_dir, "papers/markdown/docas.md")
fix_file(docas_md, [
    ("Sim S-Series inverse trust drift law and betrayal entropy spikes, §5.15", "Sim S-Series inverse trust drift law and betrayal entropy spikes, §5.24"),
    ("Sim M-Series acoustic battery in §5.12", "Sim M-Series acoustic battery"),
])
docas_tex = os.path.join(base_dir, "papers/source/docas.tex")
fix_file(docas_tex, [
    ("Sim S-Series inverse trust drift law and betrayal entropy spikes, \\S{}5.15", "Sim S-Series inverse trust drift law and betrayal entropy spikes, \\S{}5.24"),
    ("Sim M-Series acoustic battery in \\S{}5.12", "Sim M-Series acoustic battery"),
])

# 4. Move Section 1.8 in whitepaper.md to Section 3.0
whitepaper_md = os.path.join(base_dir, "papers/markdown/whitepaper.md")
with open(whitepaper_md, 'r') as f:
    content = f.read()

sec_18_match = re.search(r'(## 1\.8 Record Keeping Theory: The Digital Cellular Wall and Membrane Physics.*?)\n\n# 2\. Why Financial Data Is the Cleanest Validation Stream', content, re.DOTALL)
if sec_18_match:
    sec_18_text = sec_18_match.group(1)
    content = content.replace(sec_18_text, "")
    
    # insert before # 3. The Architecture
    new_sec_30 = sec_18_text.replace("## 1.8 Record Keeping Theory", "## 3.0 Record Keeping Theory")
    content = content.replace("# 3. The Architecture", f"# 3. The Architecture\n\n{new_sec_30}\n")
    
    with open(whitepaper_md, 'w') as f:
        f.write(content)
    print("Moved Section 1.8 to 3.0 in whitepaper.md")

# Move in whitepaper.tex
whitepaper_tex = os.path.join(base_dir, "papers/source/whitepaper.tex")
with open(whitepaper_tex, 'r') as f:
    content = f.read()

sec_18_tex_match = re.search(r'(\\subsection\*\{1\.8 Record Keeping Theory: The Digital Cellular Wall and Membrane Physics\}.*?)\n\n\\section\*\{2\. Why Financial Data Is the Cleanest Validation Stream\}', content, re.DOTALL)
if sec_18_tex_match:
    sec_18_tex = sec_18_tex_match.group(1)
    content = content.replace(sec_18_tex, "")
    new_sec_30_tex = sec_18_tex.replace("\\subsection*{1.8 Record Keeping Theory", "\\subsection*{3.0 Record Keeping Theory")
    content = content.replace("\\section*{3. The Architecture}", f"\\section*{{3. The Architecture}}\n\n{new_sec_30_tex}\n")
    with open(whitepaper_tex, 'w') as f:
        f.write(content)
    print("Moved Section 1.8 to 3.0 in whitepaper.tex")

print("Editorial fixes applied.")
