from flask import Flask, request, jsonify
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
import subprocess
import json

app=Flask(__name__)

@app.route('/', methods=['GET'])
def run_script():
    try:
        result = subprocess.run(['python', 'backend/ml_model/gmailapi.py'], capture_output=True, text=True)
        if result.returncode != 0:
            return jsonify(error=result.stderr), 500
        predictions = json.loads(result.stdout)
        return jsonify(predictions=predictions)
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
    # Uncomment the following lines if you want to use gevent WSGIServer
    # http_server = WSGIServer(('0.0.0.0', 8080), app)
    # http_server.serve_forever()
