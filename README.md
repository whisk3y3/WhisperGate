# WhisperGate

<p align="center">
  <img src="static/images/logo.png" alt="WhisperGate" width="400">
</p>

<p align="center">
  <strong>Multi-stage credential harvesting framework for authorized phishing &amp; vishing assessments</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#how-it-works">How It Works</a> •
  <a href="#operator-panel">Operator Panel</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#customization">Customization</a> •
  <a href="#disclaimer">Disclaimer</a>
</p>

---

## Overview

WhisperGate is a credential harvesting tool built for professional penetration testers conducting authorized phishing and vishing engagements. It presents a realistic endpoint compliance scanner that walks targets through a multi-stage flow — device scan, results review, SSO authentication, and an operator-controlled verification hold — giving operators full control over pacing during live phone-based social engineering.

v3 introduces browser fingerprinting, a split SSO login flow mirroring real Microsoft/Entra ID authentication, first-attempt password rejection, a live operator control panel with one-click credential copy, and fully operator-controlled target release.

Built by [@whisk3y3](https://github.com/whisk3y3)

---

## Features

### Core Flow
- **Multi-stage pipeline** — scan → results → SSO email → org lookup → password → verification hold → operator release → M365 redirect
- **Browser fingerprinting** — scan results are dynamically generated from the target's actual user agent, OS, browser version, screen resolution, and timezone
- **Split SSO login** — email and password are collected on separate screens with an "org lookup" loading transition, mirroring real Microsoft/Okta/Entra ID flows
- **First-attempt rejection** — the first password submission is rejected with a realistic error message, prompting the target to re-enter; both passwords are logged (configurable)
- **Operator-controlled release** — the verification screen holds indefinitely until the operator explicitly releases the target from the control panel; no auto-timer

### Operator Tools
- **Live WebSocket control panel** — real-time credential feed with per-credential copy buttons, accessible at `/operator?token=<your_token>`
- **One-click credential copy** — each captured credential has its own Copy Username and Copy Password buttons for fast relay to a real login
- **Manual target release** — the "Next" button only appears on the target's screen when the operator hits Release; the hold is indefinite by default
- **Per-attempt logging** — credentials are logged with attempt number, timestamp, source IP, and user agent

### Realism Details
- **Session awareness** — page state persists across refreshes; targets who reload skip the scan and return to results
- **Randomized scan timing** — each compliance check takes a different amount of time with natural variance
- **OS-aware results** — scan output adapts per platform (BitLocker/FileVault/LUKS, Defender/XProtect/ClamAV, etc.)
- **Contextual MFA notice** — appears only during the MFA verification step with a device approval prompt
- **No "encrypted connection" badge** — replaced with a subtle policy reference number that real enterprise apps would show
- **Favicon** — inline SVG shield icon so the browser tab looks legitimate
- **Per-client branding** — swap logo and primary color via CSS variables

---

## How It Works

WhisperGate walks the target through five stages:

### Stage 1 — Endpoint Compliance Scan

The page fingerprints the target's browser and builds a set of compliance check results using real device data. An animated scanner reveals each check one by one with randomized timing. The scan runs for approximately 12 seconds.

> **Conference demo note:** On a Mac, the scan correctly shows macOS, FileVault, XProtect, and Safari/Chrome. On Windows, it shows Windows 11, BitLocker, Defender, and Edge/Chrome. This is all derived from the browser's own telemetry — no plugins or special access required.

![Stage 1: Scanning](screenshots/stage1_scan.png)

### Stage 2 — Scan Results

Results display in a professional compliance table with pass/fail badges. A "Submit to IT Helpdesk" button sits below the summary. This separation is intentional — it makes the upcoming login feel like a legitimate SSO redirect rather than a form bolted onto the scan page.

![Stage 2: Results](screenshots/stage2_results.png)

### Stage 3 — SSO Authentication (Email → Password)

Clicking "Submit to IT Helpdesk" transitions to a standalone Microsoft-style sign-in page. The target enters their email address first. A "Looking up your organization..." loading screen appears for 1.5–2.5 seconds (randomized), then the password page loads showing the entered email with a back arrow — exactly mirroring the real Microsoft/Entra ID flow.

**First-attempt rejection:** The first password submission returns an error: *"Your account or password is incorrect."* The target re-enters their password, which is accepted on the second attempt. Both passwords are captured and logged with attempt numbers. This technique increases believability (a fake site would accept anything) and frequently captures a second, different password.

<!-- Screenshots needed: stage3_email.png, stage3_org_lookup.png, stage3_password.png, stage3_password_error.png -->

### Stage 4 — Verification Hold & MFA Window

After successful authentication, the page transitions to a staged verification sequence:

1. **Authenticating credentials** (3s)
2. **Verifying MFA** (7s) — a contextual notice appears: *"A verification request has been sent to your registered device. Please approve the prompt to continue."*
3. **Uploading scan results** (14s)
4. **Awaiting confirmation** (20s+) — **holds indefinitely**

The verification screen never auto-completes. The target sees the spinner and "Awaiting confirmation..." for as long as needed. This is the operator's working window:

1. Credentials appear on the operator panel with Copy Username / Copy Password buttons
2. The operator copies the credentials and pastes them into a real M365 login
3. Microsoft sends an MFA push to the target's device
4. The target approves the push (they're already primed by the on-screen MFA notice)
5. Once the operator confirms successful authentication, they hit **Release Target** on the panel
6. The target sees "Verification complete" and the Next button, which redirects to M365

This gives the operator complete control over timing — no guessing, no race conditions, no premature release.

![Stage 4: Verifying](screenshots/stage3_verifying.png)

![Stage 4: Next Button](screenshots/stage3_next.png)

---

## Operator Panel

Access the operator panel at:

```
https://yourdomain.com/operator?token=changeme
```

The panel provides:

- **Live credential feed** — credentials appear in real-time via WebSocket as targets submit them, showing email, password, attempt number, IP, and timestamp
- **Copy Username / Copy Password** — per-credential buttons for instant clipboard copy; buttons flash green with "Copied!" confirmation
- **Capture counter** — running total of harvested credentials
- **Release Target** — the only way the "Next" button appears on the target's screen; verification holds indefinitely until the operator acts
- **Event log** — timestamped log of all operator actions

### Recommended Operator Workflow

1. Open the operator panel in one browser window
2. Open `https://login.microsoftonline.com` in another tab, ready to paste
3. Call the target and direct them to the WhisperGate URL
4. When credentials land in the feed: **Copy Username** → paste into M365 → **Copy Password** → paste → submit
5. MFA push fires on the target's phone; talk them through approving it
6. Once you're authenticated on your end, hit **Release Target**
7. Target clicks "Next" and lands on the real M365 apps page — clean exit

> **Conference tip:** Run the operator panel on a separate screen alongside the target view. The audience sees both perspectives simultaneously — the target's experience and the operator's real-time control surface.

---

## Quick Start

> **Recommended:** Use an AWS EC2 instance (Ubuntu 22.04+, t2.micro) or similar VPS. This keeps phishing infrastructure isolated and gives you a clean public IP for DNS.

### Prerequisites

- Python 3.8+
- A domain with DNS records pointing to your server
- SSL/TLS certificate (Let's Encrypt recommended)

### Installation

```bash
git clone https://github.com/whisk3y3/WhisperGate.git
cd WhisperGate
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Generate SSL Certificate

```bash
sudo apt install certbot
sudo certbot certonly --standalone -d yourdomain.com
```

### Configure

Edit `WhisperGate.py` and update:

```python
# Certificate paths
cert_file = '/etc/letsencrypt/live/yourdomain.com/fullchain.pem'
key_file = '/etc/letsencrypt/live/yourdomain.com/privkey.pem'

# Engagement settings
EMAIL_DOMAIN = '@targetcompany.com'
MIN_PASS_LEN = 1
ADMIN_TOKEN = 'your-secret-token'    # Change this!
REJECT_FIRST_ATTEMPT = True          # Set False to accept first password
```

### Run

```bash
tmux new -s server
sudo python3 WhisperGate.py
```

The operator panel is available at `https://yourdomain.com/operator?token=your-secret-token`.

Credentials are logged to `credentials.txt` and printed to the console in real-time. Without SSL certs present, WhisperGate starts in dev mode on port 5000.

---

## Customization

### Branding

1. **Logo** — Replace `static/images/logo.png` with the target organization's logo
2. **Primary color** — Edit `--color-primary` in `static/css/styles.css`:

```css
:root {
  --color-primary: #0078d4;       /* Swap per engagement */
  --color-primary-hover: #106ebe;
}
```

3. **Brand text** — Update the header in `templates/index.html`:

```html
<span class="brand-text">Endpoint Security</span>
```

4. **Reference number** — Change the policy ref in the top bar to match the target org's naming convention:

```html
<span class="top-bar-ref">Ref: SEC-2024-0847</span>
```

5. **Redirect URL** — Change the final redirect destination in the Next button `onclick` handler

### Scan Results

The scan results are auto-generated from browser fingerprinting, but you can customize the `getFingerprint()` function in `templates/index.html` to add, remove, or modify checks. The two hardcoded failure items (Security Patch Level and Browser Extensions) can be adjusted to match the target environment.

### Timing

| Variable | Location | Default | Description |
|----------|----------|---------|-------------|
| `SCAN_MS` | `index.html` | `12000` | Total scan duration in ms |
| `REJECT_FIRST_ATTEMPT` | `WhisperGate.py` | `True` | Whether to reject the first password |
| `ADMIN_TOKEN` | `WhisperGate.py` | `changeme` | Access token for the operator panel |

> **Note:** There is no hold timer to configure. The verification screen holds indefinitely until the operator releases the target from the control panel.

---

## Project Structure

```
WhisperGate/
├── WhisperGate.py              # Flask + SocketIO backend
├── requirements.txt            # Python dependencies
├── credentials.txt             # Captured credentials (auto-created)
├── LICENSE
├── README.md
├── templates/
│   ├── index.html              # Multi-stage target-facing page
│   └── operator.html           # Real-time operator control panel
├── static/
│   ├── css/
│   │   └── styles.css          # All styling — CSS variables for rebranding
│   └── images/
│       └── logo.png            # Client logo (swap per engagement)
└── screenshots/
```

---

## Credential Log Format

```
[2025-03-01 14:23:17] IP: 192.168.1.50 | Email: john.smith@company.com | Password: Summer2025! | Attempt: 1
[2025-03-01 14:23:38] IP: 192.168.1.50 | Email: john.smith@company.com | Password: Fall2025!! | Attempt: 2
[2025-03-01 14:25:44] IP: 192.168.1.72 | Email: jane.doe@company.com | Password: Welcome123! | Attempt: 1
[2025-03-01 14:26:01] IP: 192.168.1.72 | Email: jane.doe@company.com | Password: Welcome123! | Attempt: 2
```

---

## What's New in v3

| Feature | v2 | v3 |
|---------|----|----|
| Scan results | Hardcoded Windows checks | Browser fingerprint-aware (OS, browser, resolution) |
| Login flow | Single form (email + password together) | Split SSO: email → org lookup → password |
| Password capture | Accept first attempt | Reject first, accept second (both logged) |
| Verification hold | Auto-timer (30s) with manual extend | Indefinite hold — operator-only release |
| Operator controls | Console only | WebSocket panel with live feed + copy buttons |
| MFA messaging | Premature warning in header | Contextual notice during MFA verification step |
| Session handling | Re-scans on every refresh | Remembers state, skips to results on refresh |
| Scan timing | Uniform intervals | Randomized per-check delays |
| Top bar badge | "Encrypted Connection" | Subtle policy reference number |
| Favicon | None | Inline SVG shield |

---

## Disclaimer

WhisperGate is intended **exclusively** for authorized security assessments. Before using this tool:

- Obtain written authorization from the target organization
- Ensure the engagement scope explicitly includes phishing/vishing
- Comply with all applicable laws and regulations
- Handle captured credentials according to your engagement's rules of engagement

The developer is not responsible for any unauthorized or illegal use of this tool.

---

## Contributing

Contributions welcome. Open an issue or submit a PR.

## License

[MIT](LICENSE)
