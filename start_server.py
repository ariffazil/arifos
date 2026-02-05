from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/health')
def health():
    """Railway healthcheck endpoint"""
    return jsonify({
        'status': 'ok',
        'service': 'arifOS',
        'version': 'v55.4-SEAL'
    }), 200

@app.route('/')
def root():
    """Root endpoint"""
    return jsonify({
        'service': 'arifOS',
        'status': 'running',
        'constitution': '13 Floors',
        'theory': 'Reverse Transformer'
    })

if __name__ == '__main__':
    # Railway provides PORT env var, default to 3000
    port = int(os.environ.get('PORT', 3000))
    # MUST bind to 0.0.0.0 for Railway
    app.run(host='0.0.0.0', port=port, debug=False)
