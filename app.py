from flask import Flask, request, jsonify, send_from_directory
from konversi import to_decimal, from_decimal

app = Flask(__name__)

@app.route('/api/convert', methods=['POST'])
def api_convert():
    data = request.get_json()
    value = data.get('value', '').strip()
    base_from = data.get('base_from')
    base_to = data.get('base_to')
    try:
        # Konversi ke desimal dulu
        decimal = to_decimal(value, base_from)
        # Lalu konversi ke basis tujuan
        result = from_decimal(decimal, base_to)
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# Route untuk file statis (html)
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)