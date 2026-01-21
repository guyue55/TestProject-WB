import os
import html
import sys

from flask import Flask, jsonify
import flask as flask_pkg
import google.auth
from google.auth.transport.requests import Request
import urllib.request

app = Flask(__name__)

def _metadata_sa_email():
    try:
        req = urllib.request.Request(
            "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/email",
            headers={"Metadata-Flavor": "Google"},
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.read().decode().strip()
    except Exception:
        return None


@app.route('/whoami')
def who_am_i():
    try:
        credentials, project = google.auth.default()
        try:
            credentials.refresh(Request())
        except Exception:
            pass
        sa_email_adc = getattr(credentials, "service_account_email", None)
        sa_email_meta = _metadata_sa_email()
        identity = {
            "status": "Success - Running on Cloud",
            "project_id": project,
            "identity_type": "Service Account",
            "sa_email_from_adc": sa_email_adc,
            "sa_email_from_metadata": sa_email_meta,
            "is_credentials_valid": getattr(credentials, "valid", False)
        }
    except Exception as e:
        identity = {
            "status": "Failure - Credentials or SDK Issue",
            "error_detail": str(e)
        }

    return jsonify(identity)


@app.route("/")
def hello_world():
    """Example Hello World route."""
    name = os.environ.get("NAME", "World")
    safe_name = html.escape(name)
    py_ver = sys.version.split(' ')[0]
    flask_ver = flask_pkg.__version__
    sa_meta = _metadata_sa_email() or "-"
    service = os.environ.get("K_SERVICE") or "-"
    revision = os.environ.get("K_REVISION") or "-"
    server = "cloud" if os.environ.get("K_SERVICE") else "dev"
    try:
        credentials, project = google.auth.default()
        try:
            credentials.refresh(Request())
        except Exception:
            pass
        project_id = project or (os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT") or "-")
        sa_adc = getattr(credentials, "service_account_email", None) or "-"
        cred_valid = getattr(credentials, "valid", False)
    except Exception:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT") or "-"
        sa_adc = "-"
        cred_valid = False
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Hello {safe_name}</title>
  <style>
    :root {{
      --bg: #f6f8fa;
      --card: #ffffff;
      --text: #24292f;
      --muted: #57606a;
      --accent: #2da44e;
      --border: rgba(27,31,36,0.15);
      --grid: rgba(27,31,36,0.06);
      --shadow: rgba(0,0,0,0.08);
    }}
    @media (prefers-color-scheme: dark) {{
      :root {{
        --bg: #0b0f14;
        --card: #11161d;
        --text: #e6edf3;
        --muted: #8b949e;
        --accent: #3fb950;
        --border: rgba(99,110,123,0.25);
        --grid: rgba(99,110,123,0.15);
        --shadow: rgba(0,0,0,0.35);
      }}
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      background:
        radial-gradient(1200px 600px at 10% 10%, rgba(45,164,78,0.06), transparent 60%),
        radial-gradient(1000px 500px at 90% 15%, rgba(99,110,123,0.08), transparent 60%),
        linear-gradient(to right, var(--grid) 1px, transparent 1px),
        linear-gradient(to bottom, var(--grid) 1px, transparent 1px);
      background-size: auto, auto, 24px 24px, 24px 24px;
      background-color: var(--bg);
      color: var(--text);
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas,
                   "Liberation Mono", "Courier New", monospace;
    }}
    .container {{
      width: min(960px, 94vw);
      margin: 20px auto;
      padding: 0 8px 28px;
    }}
    header {{
      position: sticky;
      top: 0;
      backdrop-filter: saturate(1.2) blur(6px);
      background: color-mix(in srgb, var(--bg) 80%, transparent);
      border-bottom: 1px solid var(--border);
    }}
    .bar {{
      width: min(960px, 94vw);
      margin: 0 auto;
      padding: 12px 8px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .brand {{
      font-weight: 600;
      letter-spacing: 0.3px;
    }}
    .brand .dot {{
      color: var(--accent);
    }}
    .tag {{
      padding: 2px 8px;
      border: 1px solid var(--border);
      border-radius: 999px;
      font-size: 12px;
      color: var(--muted);
    }}
    .hero {{
      margin-top: 24px;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 24px;
      box-shadow: 0 10px 28px var(--shadow);
    }}
    h1 {{
      margin: 0 0 10px;
      font-size: 30px;
      letter-spacing: 0.2px;
    }}
    .badge {{
      display: inline-block;
      margin-left: 10px;
      padding: 2px 8px;
      border-radius: 999px;
      background: rgba(63,185,80,0.12);
      border: 1px solid rgba(63,185,80,0.35);
      color: var(--accent);
      font-size: 12px;
    }}
    .sub {{
      margin: 0;
      color: var(--muted);
      font-size: 14px;
    }}
    .grid {{
      margin-top: 16px;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 16px;
    }}
    .card {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 16px;
      box-shadow: 0 6px 18px var(--shadow);
    }}
    pre {{
      margin: 0;
      padding: 12px 14px;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: rgba(0,0,0,0.06);
      overflow: auto;
    }}
    .footer {{
      margin-top: 14px;
      font-size: 12px;
      color: var(--muted);
    }}
    a {{ color: var(--accent); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
  </style>
</head>
<body>
  <header>
    <div class="bar">
      <div class="brand">helloworld<span class="dot">.</span>app</div>
      <div class="tag">monospace · clean · dev</div>
    </div>
  </header>
  <div class="container">
    <section class="hero">
      <h1>Hello, {safe_name}! <span class="badge">Flask</span></h1>
      <p class="sub">简洁但不单调</p>
      <div class="grid">
        <div class="card">
          <div class="sub">Request</div>
          <pre>GET /
200 OK
Name: {safe_name}</pre>
        </div>
        <div class="card">
          <div class="sub">Environment</div>
          <pre>Python: {py_ver}
Flask: {flask_ver}
Server: {server}
Service: {service}
Revision: {revision}</pre>
        </div>
        <div class="card">
          <div class="sub">Identity</div>
          <pre>Project: {project_id}
SA(meta): {sa_meta}
SA(ADC): {sa_adc}
Creds Valid: {str(cred_valid)}</pre>
        </div>
        <div class="card">
          <div class="sub">Quick Links</div>
          <pre>Docs: https://flask.palletsprojects.com/
Gunicorn: https://gunicorn.org/
Werkzeug: https://werkzeug.palletsprojects.com/</pre>
        </div>
      </div>
      <p class="footer">Powered by Flask · Python</p>
    </section>
  </div>
</body>
</html>"""


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
