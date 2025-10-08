from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from konversi import to_decimal, from_decimal
import os

app = Flask(__name__, static_folder="static")
CORS(app)  # 🔥 Izinkan akses lintas domain (misal dari :5500)

@app.route('/api/convert', methods=['POST'])
def api_convert():
    data = request.get_json()
    value = data.get('value', '').strip()
    base_from = data.get('base_from')
    base_to = data.get('base_to')
    try:
        decimal = to_decimal(value, base_from)
        result = from_decimal(decimal, base_to)
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    # 🔧 Railway menggunakan port dinamis lewat variabel lingkungan
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
