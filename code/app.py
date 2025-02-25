from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Konfigurasi MongoDB
MONGO_URI = "#####"  # Ganti dengan MongoDB URI
client = MongoClient(MONGO_URI)
db = client['data_sensor']
collection_dht11 = db['dht11']
collection_ldr = db['ldr']

@app.route('/kirim_data', methods=['POST'])
def kirim_data():
    try:
        data = request.get_json()
        if not data or not isinstance(data, dict):
            return jsonify({"error": "Data tidak valid"}), 400

        data['timestamp'] = datetime.now()

        if "temperature" in data and "humidity" in data:
            collection_dht11.insert_one(data)
        elif "light" in data:
            collection_ldr.insert_one(data)
        else:
            return jsonify({"error": "Jenis sensor tidak dikenali"}), 400

        return jsonify({"message": "Data berhasil disimpan"}), 200

    except Exception as e:
        return jsonify({"error": f"Gagal menyimpan data: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
