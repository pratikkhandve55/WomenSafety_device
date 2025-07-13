import network
import urequests
import machine
import time
import ubinascii

# ----------  Twilio Credentials (Replace before uploading to ESP32) ----------
twilio_sid         = 'your_twilio_sid'
twilio_api_key     = 'your_api_key_sid'
twilio_api_secret  = 'your_api_key_secret'

guardian_number = '+91xxxxxxxxxx'   # Guardian phone number
victim_number   = '+91xxxxxxxxxx'   # Victim phone number 
twilio_number   = '+1xxxxxxxxxx'    # Twilio number

# ---------- Wi-Fi Credentials ----------
WIFI_SSID     = "your_wifi_ssid"
WIFI_PASSWORD = 'your_wifi_password'

# ---------- Setup Pins ----------
button = machine.Pin(26, machine.Pin.IN, machine.Pin.PULL_UP)  # Emergency button
led = machine.Pin(2, machine.Pin.OUT)  # Onboard blue LED (GPIO2)

# ---------- Wi-Fi Connection ----------
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    print(" Connecting to Wi-Fi", end="")
    for _ in range(15):
        if wlan.isconnected():
            break
        print(".", end="")
        time.sleep(1)

    if wlan.isconnected():
        print(f"\n Connected to Wi-Fi: {wlan.ifconfig()[0]}")
    else:
        print("\n Failed to connect to Wi-Fi")

# ---------- Twilio Call ----------
def make_call():
    print(" Making call to guardian...")
    url = f"https://api.twilio.com/2010-04-01/Accounts/{twilio_sid}/Calls.json"
    headers = {
        "Authorization": "Basic " + ubinascii.b2a_base64(f"{twilio_api_key}:{twilio_api_secret}".encode()).decode().strip(),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = f"To={guardian_number}&From={twilio_number}&Twiml=<Response><Say>Emergency! The user is in danger. Please take action.</Say></Response>"

    try:
        res = urequests.post(url, data=data, headers=headers)
        print(" Call placed:", res.status_code)
        res.close()
    except Exception as e:
        print(" Call error:", e)

# ---------- Twilio SMS ----------
def send_sms():
    print(" Sending SMS to victim...")
    url = f"https://api.twilio.com/2010-04-01/Accounts/{twilio_sid}/Messages.json"
    headers = {
        "Authorization": "Basic " + ubinascii.b2a_base64(f"{twilio_api_key}:{twilio_api_secret}".encode()).decode().strip(),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = f"To={victim_number}&From={twilio_number}&Body=Emergency"

    try:
        res = urequests.post(url, data=data, headers=headers)
        print(" SMS sent:", res.status_code)
        res.close()
    except Exception as e:
        print(" SMS error:", e)

# ---------- Main Program ----------
connect_wifi()
print("Waiting for button press...")

while True:
    if button.value() == 0:  # Button pressed (active LOW)
        print(" Button Pressed!")
        led.on()
        time.sleep(0.3)
        led.off()

        make_call()
        send_sms()

        print("Waiting before next trigger...")
        time.sleep(5)  # Delay to avoid multiple triggers
    time.sleep(0.1)  # Debounce
