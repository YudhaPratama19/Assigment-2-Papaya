import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# ```python
# Konfigurasi MongoDB
MONGO_URI = "</>"  # Ganti dengan URI MongoDB Anda
client = MongoClient(MONGO_URI)
db = client['data_sensor']
collection = db['dht11']
collection = db['ldr']

@app.route('/kirim_data', methods=['POST'])
def kirim_data():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Data tidak valid"}), 400
    
    # Menyimpan data ke MongoDB
    data['timestamp'] = datetime.now()
    collection.insert_one(data)
    
    return jsonify({"message": "Data berhasil disimpan"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Menjalankan server Flask
