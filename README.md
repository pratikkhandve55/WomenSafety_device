#  Women Safety Device using ESP32 + Twilio

A compact, low-cost, IoT-based emergency alert system built using an **ESP32 DevKit V1**, programmed with **MicroPython**, that automatically sends an **emergency call and SMS** using **Twilio Cloud API** when a button is pressed.

---

## 🔧 Features

-  Automatic **call to guardian** using Twilio Voice API
-  Sends **SMS to victim** instantly
-  Connects to Wi-Fi automatically on power-up
-  Works fully standalone (no laptop, no backend server)
-  Button-activated trigger, ready for wearable design
-  Secure and open-source code (MIT License)

---

##  Circuit Diagram

> Connect a push button between **GPIO26** and **GND**.  
> The onboard blue LED on **GPIO2** is used as an indicator.

![Circuit Diagram](images/circuit_diagram.jpg)

---

##  How It Works

1. ESP32 powers on and connects to Wi-Fi.
2. On button press:
   - A **call** is placed to the guardian with a voice message.
   - An **SMS** is sent to the victim.
3. Victim's smartphone (via Tasker) can auto-send live GPS location to police via SMS when a call is received.

---

##  Technologies Used

- MicroPython on ESP32
- Twilio REST API (SMS & Voice)
- HTTP Requests via `urequests`
- Wi-Fi connection using `network`
- Tasker (optional smartphone automation)

---

