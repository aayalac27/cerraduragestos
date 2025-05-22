import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# ---------- ESTILOS CSS ----------
st.markdown("""
    <style>
        body, .stApp {
            background: linear-gradient(to bottom right, #e0f7fa, #ffffff);
            font-family: 'Segoe UI', sans-serif;
        }

        .main-title {
            font-size: 38px;
            font-weight: bold;
            color: white;
            text-align: center;
            background: linear-gradient(90deg, #0072ff, #00c6ff);
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 30px;
        }

        .info-box {
            background-color: #fefefe;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.08);
            text-align: center;
            margin-bottom: 20px;
            font-size: 18px;
        }

        .stButton>button {
            background-color: #00bcd4;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 14px 28px;
            font-size: 20px;
            font-weight: bold;
            margin: 10px;
            transition: background-color 0.3s ease;
        }

        .stButton>button:hover {
            background-color: #0097a7;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- TÍTULO ----------
st.markdown('<div class="main-title">Control de Iluminación del Hogar 🏠💡</div>', unsafe_allow_html=True)

# ---------- VERSIÓN DE PYTHON ----------
st.markdown(f'<div class="info-box">Controla la luz principal de tu casa en tiempo real.</div>', unsafe_allow_html=True)

# ---------- CONFIGURACIÓN MQTT ----------
def on_publish(client, userdata, result):
    print("Mensaje publicado")

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.info(f"Mensaje recibido: {message_received}")

broker = "broker.hivemq.com"
port = 1883
client1 = paho.Client("AlejoInterfaces")
client1.on_message = on_message

# ---------- BOTONES DE CONTROL ----------
col_left, col_center, col_right = st.columns([1,2,1])


with col_center:
    col_button1, col_button2 = st.columns(2)
    with col_button1:
        if st.button('ENCENDER LUZ 🔆'):
            action = "encender"
            client1 = paho.Client("AlejoInterfaces")
            client1.on_publish = on_publish
            client1.connect(broker, port)
            message = json.dumps({"gesto": action})
            client1.publish("AlejoCerradura", message)
            st.success("Luz encendida. ¡Tu casa está iluminada!")

    with col_button2:
        if st.button('APAGAR LUZ 🌙'):
            action = "apagar"
            client1 = paho.Client("AlejoInterfaces")
            client1.on_publish = on_publish
            client1.connect(broker, port)
            message = json.dumps({"gesto": action})
            client1.publish("AlejoCerradura", message)
            st.warning("Luz apagada. Tu casa está en modo descanso.")
