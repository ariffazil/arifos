import http.server
import socketserver
import hmac
import hashlib
import subprocess
import json
import os

# --- Configuration ---
PORT = 80
# This secret should be the same as the one you set in the GitHub webhook settings.
# It's recommended to move this to an environment variable for better security.
WEBHOOK_SECRET = os.environ.get("GITHUB_WEBHOOK_SECRET", "your_super_secret_string")
DEPLOY_SCRIPT_PATH = "/root/arifOS/deploy.sh"
# --- End Configuration ---

class WebhookHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. Verify the signature
        signature_header = self.headers.get('X-Hub-Signature-256')
        if not signature_header:
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"Forbidden: X-Hub-Signature-256 header is missing.")
            return

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        expected_signature = "sha256=" + hmac.new(
            WEBHOOK_SECRET.encode('utf-8'),
            post_data,
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(expected_signature, signature_header):
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"Forbidden: Signature mismatch.")
            return

        # 2. Check the event type (optional but recommended)
        event_type = self.headers.get('X-GitHub-Event')
        if event_type == "ping":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"GitHub Ping event received successfully.")
            return
        
        if event_type != "push":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f"Ignoring event type: {event_type}".encode('utf-8'))
            return

        # 3. Check if the push was to the 'main' branch
        try:
            payload = json.loads(post_data.decode('utf-8'))
            ref = payload.get('ref')
            if ref != 'refs/heads/main':
                self.send_response(200)
                self.end_headers()
                self.wfile.write(f"Ignoring push to branch: {ref}".encode('utf-8'))
                return
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Bad Request: Could not decode JSON payload.")
            return

        # 4. If all checks pass, trigger the deployment script
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Webhook received. Triggering deployment...")

        print(f"Deployment triggered for push to main branch...")
        try:
            # Using subprocess.Popen to run the script in the background
            # and capture its output to a log file.
            log_file = open("/root/arifOS/deployment.log", "a")
            subprocess.Popen([DEPLOY_SCRIPT_PATH], stdout=log_file, stderr=log_file, shell=True)
            print(f"Deployment script '{DEPLOY_SCRIPT_PATH}' executed.")
        except Exception as e:
            print(f"Error executing deployment script: {e}")

with socketserver.TCPServer(("", PORT), WebhookHandler) as httpd:
    print(f"Starting webhook listener on port {PORT}")
    print("Remember to set the GITHUB_WEBHOOK_SECRET environment variable.")
    httpd.serve_forever()

