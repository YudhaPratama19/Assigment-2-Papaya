import network
import machine as m
import socket
import time
import requests
import dht
from machine import Pin

# Konfigurasi WiFi
SSID = "Wanipiro"
PASSWORD = "bayardulu"
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(SSID, PASSWORD)

def checkwifi():
    while not sta_if.isconnected():
        time.sleep(1)
        print("Menunggu koneksi WiFi...")
        sta_if.connect(SSID, PASSWORD)

# Konfigurasi Ubidots
TOKEN = "BBUS-jtXyYjozgXzoz94xrcQNo81v6A9R6J"
DEVICE_LABEL = "esp-papaya"
VARIABLE_LABEL_TEMP = "temperature"
VARIABLE_LABEL_HUM = "humidity"

# Inisialisasi sensor DHT11
sensor = dht.DHT11(Pin(27))

def send_data(temp, hum):
    url = "http://industrial.api.ubidots.com/api/v1.6/devices/{}".format(DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
    payload = {
        VARIABLE_LABEL_TEMP: temp,
        VARIABLE_LABEL_HUM: hum
    }
    
    try:
        req = requests.post(url, headers=headers, json=payload)
        print("Status Code:", req.status_code)
        print("Response:", req.json())
    except Exception as e:
        print("[ERROR] Gagal mengirim data:", e)

def main():
    checkwifi()
    while True:
        try:
            sensor.measure()
            temp = sensor.temperature()
            hum = sensor.humidity()
            print(f"Temperature: {temp} C")
            print(f"Humidity: {hum} %")
            send_data(temp, hum)
        except OSError as e:
            print("[ERROR] Gagal membaca sensor.")
        time.sleep(2)  # Kirim data setiap 5 detik

if __name__ == '__main__':
    main()
