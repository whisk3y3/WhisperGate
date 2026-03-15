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
  <a href="#social-engineering-psychology">SE Psychology</a> •
  <a href="#operator-panel">Operator Panel</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#customization">Customization</a> •
  <a href="#disclaimer">Disclaimer</a>
</p>

---

## Overview

WhisperGate is a credential harvesting tool built for professional penetration testers conducting authorized phishing and vishing engagements. It presents a realistic endpoint compliance scanner that walks targets through a multi-stage flow — device scan, results review, SSO authentication, and an operator-controlled verification hold — giving operators full control over pacing during live phone-based social engineering.

Every design decision in WhisperGate is rooted in social engineering psychology. This isn't a tool that was built to look pretty — it was built to exploit the way people make trust decisions under pressure. The [SE Psychology](#social-engineering-psychology) section below breaks down the reasoning behind each feature.

The tool supports multiple simultaneous targets with per-target session isolation. Each target gets their own card on the operator panel with independent controls, status tracking, credential copy buttons, and notes. Operators can mark MFA bypass, release individual targets, and export everything to a formatted Excel report.

Built by [@whisk3y3](https://github.com/whisk3y3)

---

## Features

### Core Flow
- **Multi-stage pipeline** — scan → results → SSO email → org lookup → password → verification hold → operator release → completion
- **Browser fingerprinting** — scan results are dynamically generated from the target's actual user agent, OS, browser version, screen resolution, and timezone
- **Split SSO login** — email and password are collected on separate screens with a "Taking you to your organization's sign-in page..." loading transition, mirroring real Microsoft/Okta/Entra ID flows
- **Per-engagement branding** — set `ORG_NAME` once and it flows through the SSO hint, org lookup screen, and completion message
- **First-attempt rejection** — the first password submission is rejected with a realistic error message; both passwords are logged (configurable)
- **Operator-controlled release** — the verification screen holds indefinitely until the operator releases that specific target
- **Clean exit** — after release, the target sees "Submission Complete — You may close this window" instead of a redirect

### Operator Panel
- **Per-target cards** — each target gets their own card showing email, IP, session ID, all captured passwords, and a status badge
- **Status progression** — Scanning → Captured → MFA Pending → Compromised → Released, updated in real-time
- **Per-target isolation** — releasing one target doesn't affect any others; WebSocket rooms are scoped per session
- **One-click credential copy** — Copy Username and Copy Latest Password buttons on each card, plus individual Copy buttons on every password entry
- **Mark Compromised** — appears when a target is in MFA Pending status; tags the target as MFA bypassed before release
- **Per-target notes** — textarea on every card for documenting outcomes; auto-saves and exports with the report
- **Engagement timer** — running clock from first credential capture, plus per-target timers showing elapsed time since each target's first submission
- **Stats dashboard** — Total Targets, Creds Captured, MFA Bypassed, and Released at a glance
- **Excel export** — one-click download with two sheets: Captured Credentials (full details per attempt) and Engagement Summary
- **State persistence** — refreshing the operator panel reloads all existing target data from the server

### Realism Details
- **Session awareness** — page state persists across refreshes; targets who reload skip the scan and return to results
- **Randomized scan timing** — each compliance check takes a different amount of time with natural variance
- **OS-aware results** — scan output adapts per platform (BitLocker/FileVault/LUKS, Defender/XProtect/ClamAV, etc.)
- **Contextual MFA notice** — appears only during the MFA verification step with a device approval prompt
- **Subtle top bar** — policy reference number instead of an "encrypted connection" badge
- **Favicon** — inline SVG shield icon so the browser tab looks legitimate

---

## How It Works

WhisperGate walks the target through five stages. Each stage is designed around a specific psychological principle — see the callouts below each stage and the full [SE Psychology](#social-engineering-psychology) section for deeper analysis.

### Stage 1 — Endpoint Compliance Scan

The page fingerprints the target's browser and builds compliance check results using real device data. An animated scanner reveals each check with randomized timing over approximately 12 seconds.

> **Conference demo note:** On a Mac, the scan shows macOS, FileVault, XProtect, and Safari/Chrome. On Windows, it shows Windows 11, BitLocker, Defender, and Edge/Chrome. All derived from the browser's own telemetry.

> **🧠 Why this works:** The scan creates a *commitment investment*. The target has now spent 12 seconds watching their device get "scanned" — they've invested time, and the results feel personalized because they reflect their actual system. Walking away now means that investment was wasted. The scan also establishes *authority framing*: the page is telling the target about their own device, which positions it as a system with knowledge and access the target doesn't have. People don't question tools that appear to know more than they do.

![Stage 1: Scanning](screenshots/stage1_scan.png)

### Stage 2 — Scan Results

Results display in a compliance table with pass/fail badges. A "Submit to IT Helpdesk" button sits below the summary with a note: *"You will be prompted to authenticate with your [Org] account."*

> **🧠 Why this works:** The results include deliberate failures — a missing security patch, flagged browser extensions. These create *anxiety and urgency*. The target now believes their device has a compliance problem, and the only path to resolution is the "Submit to IT Helpdesk" button. This is textbook *fear-then-relief*: introduce a threat, then offer a clear action to resolve it. The target isn't just willing to authenticate — they're motivated to. The "Submit" button is also intentionally separated from the login form. It feels like a natural handoff to an SSO provider, not a credential grab bolted onto a scan page.

![Stage 2: Results](screenshots/stage2_results.png)

### Stage 3 — SSO Authentication (Email → Password)

Clicking "Submit to IT Helpdesk" transitions to a standalone sign-in page. The target enters their email first, sees a loading screen (*"Taking you to your organization's sign-in page..."*), then the password page with the hint *"Sign in with your [Org] account."*

The first password is rejected with *"Your account or password is incorrect."* The second attempt succeeds. Both are captured and logged.

> **🧠 Why this works — the split flow:** Every modern identity provider (Microsoft Entra, Okta, Google Workspace) collects email and password on separate screens. Showing both fields on a single page is one of the most common tells of a phishing page — it looks like 2018 because it *is* 2018. The split flow with an org lookup animation in between matches what the target sees every day when they log into real work applications. Muscle memory takes over. They're not evaluating whether the page is real — they're just doing the thing they've done a thousand times.
>
> **🧠 Why this works — first-attempt rejection:** This is counterintuitive, which is why it's effective. Most people assume a fake site would accept any password — so when the page rejects their first attempt, it paradoxically *increases* trust. The target thinks "okay, this is actually checking my credentials against something real." They re-enter their password (often the same one, sometimes a different one), and the second attempt succeeds. The operator now has two captured passwords. A surprising number of people rotate between 2-3 passwords across different systems, so the first attempt might be their email password while the second is their VPN password. Both get logged with attempt numbers and both appear in the Excel export.

<!-- Screenshots needed: stage3_email.png, stage3_org_lookup.png, stage3_password.png, stage3_password_error.png -->

### Stage 4 — Verification Hold & MFA Window

After authentication, the page shows a staged verification sequence:

1. **Authenticating credentials** (3s)
2. **Verifying MFA** (7s) — contextual notice: *"A verification request has been sent to your registered device."*
3. **Uploading scan results** (14s)
4. **Awaiting confirmation** (20s+) — **holds indefinitely**

This is the operator's working window. The target's card appears on the operator panel:

1. **Copy Username** → paste into your M365 login tab
2. **Copy Latest Password** → paste → submit
3. Microsoft sends MFA push → target approves (primed by on-screen notice)
4. **Mark Compromised** on the operator panel (tags MFA bypass)
5. **Release Target** → only that target sees the completion screen

> **🧠 Why this works — the MFA notice:** The notice *"A verification request has been sent to your registered device"* appears exactly when the MFA step activates on screen. Seconds later, the target's phone buzzes with a real MFA push (because the operator just used their credentials to log in). The timing and the on-screen context make the push feel completely expected — the page told them it was coming, and now it arrived. Without the notice, an unexpected MFA prompt might make the target pause and call their real IT department. With the notice, they approve it without a second thought. This is *priming* — setting an expectation so that when the event occurs, the brain categorizes it as "normal" rather than "suspicious."
>
> **🧠 Why this works — indefinite hold:** The verification screen holds forever until the operator releases. There's no auto-timer that might fire too early (before the operator has authenticated) or too late (making the target suspicious). The operator has complete control. During a vishing call, this is critical — the operator can keep the target calm with "it's just verifying, sometimes this takes a minute" while they work through the MFA flow. The target sees animated progress indicators the entire time, which signals that something is happening. People are remarkably patient with loading screens as long as there's visible progress.

![Stage 4: Verifying](screenshots/stage3_verifying.png)

### Stage 5 — Completion

When released, the target sees:

> ✅ **Submission Complete**
>
> Your scan results have been submitted to the [Org] IT Helpdesk. No further action is required.
>
> *You may close this window.*

> **🧠 Why this works — no redirect:** An earlier version of WhisperGate redirected to the Microsoft 365 apps page after release. The problem: if the target is already logged into M365 in another tab, landing on the apps page feels wrong — why would a compliance scan send me to Outlook? The completion screen avoids this entirely. "You may close this window" is exactly what real enterprise tools say after a form submission. It's boring, forgettable, and gives the target no reason to think about what just happened. The interaction ends on a note of closure, not confusion.

---

## Social Engineering Psychology

Every feature in WhisperGate maps to a known social engineering principle. This section explains the psychology behind the design for operators who want to understand the "why" and for defenders who want to know what to train against.

### Commitment & Consistency

Once someone starts a process, they're psychologically inclined to finish it. The 12-second scan is a deliberate investment of the target's time and attention. By the time results appear, they've already committed to the flow. Abandoning it now feels like wasting the effort they've put in. Each stage deepens the commitment: scan → review results → click submit → enter email → enter password. By the time they're typing their password, they've made five consecutive decisions to continue. Backing out at step six feels inconsistent with the five "yes" decisions they've already made.

### Authority & Institutional Trust

The page presents itself as an internal IT compliance tool, not a login page. It uses enterprise visual language — compliance tables, policy reference numbers, status badges, branded headers — that signals institutional authority. People don't scrutinize tools that look like they belong to their employer. The browser fingerprinting amplifies this: when the scan "detects" your actual OS version, your real browser, and your correct screen resolution, it reinforces the belief that this tool has legitimate access to your system. It appears to know things about your device, which positions it as authoritative.

### Fear-Then-Relief

The scan intentionally flags failures — a missing security patch, flagged browser extensions. This creates mild anxiety: *"My device isn't compliant."* The "Submit to IT Helpdesk" button is the relief valve. The target isn't just willing to authenticate — they *want* to, because it resolves the threat. Attackers and marketers have used this pattern for decades: introduce a problem, then offer the solution. The target feels like they're *fixing* something, not giving something away.

### Familiarity & Muscle Memory

The split SSO flow (email → loading → password) isn't just realistic — it's *identical* to what the target does every morning when they log into work. Microsoft Entra ID, Okta, and Google Workspace all use this exact pattern. When the target sees it, their brain doesn't flag it for evaluation. It triggers the same motor routine they've executed hundreds of times: type email, click next, wait, type password, click sign in. You're not phishing their credentials — you're phishing their muscle memory.

### Paradoxical Trust Through Rejection

The first-attempt password rejection is WhisperGate's most counterintuitive feature. Common sense says "accept whatever the user types." But real authentication systems sometimes reject valid credentials on the first try (network timeouts, typos, expired sessions). A page that accepts *anything* on the first attempt is suspicious precisely because it's too easy. By rejecting once and accepting on the second try, WhisperGate mimics the minor friction of real authentication. The target's internal logic: "A fake site would have taken my password the first time. This one didn't. Therefore it's real." The bonus: you frequently capture two different passwords, because people instinctively try a different one when the first "doesn't work."

### Priming & Expectation Setting

The MFA notice (*"A verification request has been sent to your registered device"*) appears on screen seconds before the target's phone actually buzzes with a real MFA push. This is textbook priming. The brain has already categorized the incoming push as expected and legitimate before it even arrives. Without the notice, an unsolicited MFA prompt is suspicious — it's the number one thing security awareness training teaches people to watch for. With the notice, the target has a ready-made explanation: "The compliance tool said it was going to send me a verification request, and it did." The prompt goes from red flag to expected behavior.

### Sunk Cost & Patience

The indefinite verification hold works because the target has already invested significant time and effort: they watched the scan, reviewed results, authenticated, and entered their password twice. Walking away now means all of that was wasted. People will wait a remarkably long time on a loading screen if they've already committed to the process. The animated progress indicators (step-by-step checkmarks, a spinner, status messages) reinforce that something is happening — even though nothing is. As long as the page appears to be working, the target will wait. The operator controls the timing.

### Closure & Forgettability

The completion screen is deliberately boring. "Submission Complete. You may close this window." No redirect to a different site. No unexpected content. No reason to think twice about what just happened. The target's brain files the interaction under "routine IT task" and moves on. This is important for operational security — the longer the target spends thinking about the interaction after it's over, the higher the chance they mention it to a coworker or call IT. A clean, boring exit minimizes post-interaction scrutiny.

### The Absence of Red Flags

Some of WhisperGate's most important design decisions are about what it *doesn't* show. No "Encrypted Connection" badge (real enterprise apps don't advertise TLS). No email and password on the same page (every modern IdP splits them). No generic placeholder logo (you brand it per engagement). No uniform scan timing (real scans have variance). No automatic redirect after completion (avoids confusion). Each of these is a tell that exists in lower-quality phishing toolkits. WhisperGate's realism comes as much from removing red flags as from adding green ones.

---

## Operator Panel

Access the operator panel at:

```
https://yourdomain.com/operator
```

You'll be prompted to enter your access token. The token is set via `ADMIN_TOKEN` in `WhisperGate.py` (default: `changeme`). Authentication is session-based — the token is submitted via a POST form and stored in a server-side session cookie, so it never appears in the URL, browser history, or server access logs. The session persists until you log out or close the browser.

### Dashboard

The top stats bar shows real-time counts: Total Targets, Creds Captured, MFA Bypassed, and Released. An engagement timer starts when the first credential lands.

### Target Cards

Each target gets their own card with:

- **Email and IP** with session ID
- **Status badge** — Scanning → Captured → MFA Pending → Compromised → Released
- **All captured passwords** with attempt numbers, timestamps, and individual Copy buttons
- **Copy Username / Copy Latest Password** — quick-copy for relaying to a real login
- **Mark Compromised** — appears during MFA Pending; tags the target as MFA bypassed
- **Release Target** — sends the completion screen to that specific target only
- **Notes** — textarea for documenting outcomes; auto-saves to the server
- **Per-target timer** — elapsed time since first credential capture

### Excel Export

Click "Download Excel Report" in the sidebar. Generates a formatted `.xlsx` with:

**Sheet 1 — Captured Credentials:**
| Email | Password | Attempt | Timestamp | IP Address | User Agent | Status | MFA Bypassed | Released At | Notes |

**Sheet 2 — Engagement Summary:**
| Field | Value |
|-------|-------|
| Start Time | 2025-03-01 14:23:17 |
| Export Time | 2025-03-01 15:45:02 |
| Total Targets | 12 |
| MFA Bypassed | 8 |
| Organization | Contoso |

Filename format: `WhisperGate_Contoso_20250301_154502.xlsx`

### Recommended Operator Workflow

1. Open the operator panel in one browser window
2. Open `https://login.microsoftonline.com` in another tab
3. Call the target and direct them to the WhisperGate URL
4. Credentials land on the target's card → **Copy Username** → paste → **Copy Latest Password** → paste → submit
5. MFA push fires → talk the target through approving it
6. Hit **Mark Compromised** on their card
7. Hit **Release Target** — only that target sees the completion screen
8. Repeat for additional targets
9. **Download Excel Report** when the engagement wraps

> **Conference tip:** Run the operator panel on a second screen. The audience sees both the target experience and the operator's real-time control surface with status changes, timers, and credential captures.

### Multi-Target Note

Each target operates in their own WebSocket room. Releasing target A has no effect on target B. Multiple operators can have the panel open simultaneously — they all see the same live feed.

---

## Quick Start

> **Recommended:** Use an AWS EC2 instance (Ubuntu 22.04+, t2.micro) or similar VPS.

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
ORG_NAME = 'Contoso'                 # Target org name
```

### Branding Checklist

Before each engagement:

1. Set `ORG_NAME` in `WhisperGate.py`
2. Replace `static/images/logo.png` with the target's logo
3. Update `--color-primary` in `static/css/styles.css` to match the target's brand
4. Update the brand text in `templates/index.html` if needed
5. Update the reference number in the top bar if desired

### Run

```bash
tmux new -s server
sudo python3 WhisperGate.py
```

The operator panel is available at `https://yourdomain.com/operator` (you'll be prompted for the access token on first visit).

Credentials are logged to `credentials.txt` and printed to the console in real-time. Without SSL certs present, WhisperGate starts in dev mode on port 5000.

---

## Customization

### Branding

1. **Organization name** — Set `ORG_NAME` in `WhisperGate.py`. Flows through to:
   - SSO login hint: *"Sign in with your [Org] account"*
   - Org lookup screen: *"Taking you to your organization's sign-in page..."*
   - Completion screen: *"Your scan results have been submitted to the [Org] IT Helpdesk."*
   - Excel export: org name in the Engagement Summary sheet and filename

2. **Logo** — Replace `static/images/logo.png` with the target organization's logo

3. **Primary color** — Edit `--color-primary` in `static/css/styles.css`:

```css
:root {
  --color-primary: #0078d4;       /* Swap per engagement */
  --color-primary-hover: #106ebe;
}
```

4. **Brand text** — Update the header in `templates/index.html`:

```html
<span class="brand-text">Endpoint Security</span>
```

5. **Reference number** — Change the policy ref in the top bar:

```html
<span class="top-bar-ref">Ref: SEC-2024-0847</span>
```

### Scan Results

Scan results are auto-generated from browser fingerprinting. Customize the `getFingerprint()` function in `templates/index.html` to add, remove, or modify checks. The two hardcoded failure items (Security Patch Level and Browser Extensions) can be adjusted to match the target environment.

### Configuration Reference

| Variable | Location | Default | Description |
|----------|----------|---------|-------------|
| `ORG_NAME` | `WhisperGate.py` | `Contoso` | Target org name — used throughout SSO flow, completion, and export |
| `EMAIL_DOMAIN` | `WhisperGate.py` | `@evilphishinc.com` | Target email domain |
| `REJECT_FIRST_ATTEMPT` | `WhisperGate.py` | `True` | Whether to reject the first password |
| `ADMIN_TOKEN` | `WhisperGate.py` | `changeme` | Access token for the operator panel (entered via login form, stored in session) |
| `SCAN_MS` | `index.html` | `12000` | Total scan duration in ms |

> **Note:** There is no hold timer to configure. The verification screen holds indefinitely until the operator releases each target individually from the control panel.

---

## Project Structure

```
WhisperGate/
├── WhisperGate.py              # Flask + SocketIO backend with per-target rooms
├── requirements.txt            # Python dependencies (flask, socketio, openpyxl)
├── credentials.txt             # Captured credentials (auto-created)
├── LICENSE
├── README.md
├── templates/
│   ├── index.html              # Multi-stage target-facing page
│   ├── operator.html           # Real-time operator control panel
│   └── operator_login.html     # Operator authentication page
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

## Changelog

### v3.1
- Session-based operator authentication — token submitted via login form, never exposed in URL
- Per-target WebSocket rooms — releasing one target doesn't affect others
- Operator panel rewritten with per-target cards, status progression, and independent controls
- Mark Compromised button for tagging MFA bypass before release
- Per-target notes with auto-save
- Engagement timer and per-target timers
- Stats dashboard (targets, creds, MFA bypassed, released)
- Excel export with Captured Credentials and Engagement Summary sheets
- Operator panel state persistence across refresh
- `ORG_NAME` config for per-engagement branding
- Completion screen ("You may close this window") replaces M365 redirect
- Social Engineering Psychology section added to README

### v3.0
- Browser fingerprint-aware scan results (OS, browser, resolution)
- Split SSO login: email → org lookup → password
- First-attempt password rejection (both logged)
- Operator-controlled verification hold (no auto-timer)
- Contextual MFA notice during verification step
- Session-aware refresh (skips scan on reload)
- Randomized per-check scan delays
- Policy reference number replaces "Encrypted Connection" badge
- Inline SVG favicon

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
