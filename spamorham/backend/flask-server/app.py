from flask import Flask, jsonify
from gevent.pywsgi import WSGIServer

import subprocess
import json
app=Flask(__name__)

@app.route('/', methods=['GET'])
def run_script():
    try:
        result = subprocess.run(['python', 'backend\\ml_model\\gmailapi.py'], capture_output=True, text=True)
        if result.returncode != 0:
            return jsonify(error=result.stderr), 500
        predictions = json.loads(result.stdout)
        return jsonify(predictions=predictions)
    except Exception as e:
        return jsonify(error=str(e)), 500


if(__name__)=="__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)

http_server = WSGIServer(('127.0.0.1', 5000), app)
http_server.serve_forever()