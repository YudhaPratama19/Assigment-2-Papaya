import network
import machine as m
import time
import urequests
import dht
from machine import Pin

# Konfigurasi WiFi
SSID = "Wanipiro"
PASSWORD = "12345678"
sta_if = network.WLAN(network.STA_IF)

def connect_wifi():
    if sta_if.isconnected():
        sta_if.disconnect()
        time.sleep(1)
    sta_if.active(True)
    sta_if.connect(SSID, PASSWORD)

def checkwifi():
    connect_wifi()
    timeout = 10  # detik
    start_time = time.time()
    while not sta_if.isconnected():
        if time.time() - start_time > timeout:
            print("[ERROR] Gagal terhubung ke WiFi.")
            return
        time.sleep(1)
        print("Menunggu koneksi WiFi...")
    print("Terhubung ke WiFi:", sta_if.ifconfig())

# API endpoints
API_BASE_URL = "http://192.168.240.206:5000"
DHT11_ENDPOINT = f"{API_BASE_URL}/kirim_data"

# Konfigurasi Ubidots
TOKEN = "BBUS-7dq4SxDOdlh33mMlkhrz4PmQjdTgVU"
DEVICE_LABEL = "esp32"
VARIABLE_LABEL_LDR = "light"
VARIABLE_LABEL_TEMPERATURE = "temperature"
VARIABLE_LABEL_HUMIDITY = "humidity"

# Inisialisasi sensor
DHT_PIN = Pin(21)
dht_sensor = dht.DHT11(DHT_PIN)

LDR_PIN = 34
ldr_sensor = m.ADC(Pin(LDR_PIN))
ldr_sensor.width(m.ADC.WIDTH_12BIT)

def send_dht_data(temperature, humidity):
    payload = {
        'temperature': temperature,
        'humidity': humidity
    }
    
    try:
        req = urequests.post(DHT11_ENDPOINT, json=payload)
        print("DHT Status Code:", req.status_code)
        print("DHT Response:", req.json())
    except Exception as e:
        print("[ERROR] Gagal mengirim data DHT:", e)

def send_ubidots_data(temperature, humidity, ldr_value):
    url = f"http://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}"
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
    payload = {
        VARIABLE_LABEL_TEMPERATURE: temperature,
        VARIABLE_LABEL_HUMIDITY: humidity,
        VARIABLE_LABEL_LDR: ldr_value
    }
    
    try:
        req = urequests.post(url, headers=headers, json=payload)
        print("Ubidots Status Code:", req.status_code)
        print("Ubidots Response:", req.json())
    except Exception as e:
        print("[ERROR] Gagal mengirim data ke Ubidots:", e)

def main():
    checkwifi()
    while True:
        try:
            # Membaca data dari DHT11
            dht_sensor.measure()
            temperature = dht_sensor.temperature()
            humidity = dht_sensor.humidity()
            
            print(f"Suhu: {temperature} C, Kelembapan: {humidity} %")

            # Membaca nilai dari LDR
            ldr_value = ldr_sensor.read()
            ldr_value_scaled = (ldr_value / 4095) * 100  # Normalisasi 0-100%
            print(f"Cahaya: {ldr_value_scaled:.2f}%")
            
            # Mengirim data ke server Flask (MongoDB)
            send_dht_data(temperature, humidity)

            # Mengirim data ke Ubidots
            send_ubidots_data(temperature, humidity, ldr_value_scaled)
            
        except OSError as e:
            print("[ERROR] Gagal membaca sensor.")

        time.sleep(5)  # Kirim data setiap 5 detik

if __name__ == '__main__':
    main()
