import paho.mqtt.client as paho
import time
import json
import streamlit as st
import numpy as np
from PIL import Image
from keras.models import load_model

# ---------- ESTILOS CSS ----------
st.markdown("""
    <style>
        .main-title {
            font-size: 40px;
            font-weight: bold;
            color: white;
            text-align: center;
            background: linear-gradient(90deg, #0F2027, #203A43, #2C5364);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .intro-text {
            font-size: 18px;
            color: #333;
            text-align: center;
            margin-bottom: 20px;
        }
        .gesture-box {
            border: 2px solid #2C5364;
            border-radius: 10px;
            padding: 15px;
            margin: 10px;
            background-color: #f0f4f8;
            text-align: center;
            font-size: 18px;
        }
        .gesture-emoji {
            font-size: 40px;
        }
        .stButton>button {
            background-color: #2C5364;
            color: white;
            border: None;
            border-radius: 10px;
            padding: 10px 20px;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- TÍTULO Y INTRODUCCIÓN ----------
st.markdown('<div class="main-title">Sistema de Cerradura Inteligente para Hogares</div>', unsafe_allow_html=True)
st.markdown('<div class="intro-text">Este sistema utiliza visión por computadora y aprendizaje automático para abrir o cerrar tu puerta con gestos. ¡Toma una foto para comenzar!</div>', unsafe_allow_html=True)

# ---------- GESTOS EXPLICATIVOS ----------
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="gesture-box"><div class="gesture-emoji">✊</div><br>Gesto para <strong>cerrar</strong> la cerradura</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="gesture-box"><div class="gesture-emoji">🤚</div><br>Gesto para <strong>abrir</strong> la cerradura</div>', unsafe_allow_html=True)

# ---------- MQTT Y MODELO ----------
def on_publish(client, userdata, result):
    print("el dato ha sido publicado \n")

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

broker = "broker.hivemq.com"
port = 1883
client1 = paho.Client("AlejoInterfaces")
client1.on_message = on_message
client1.on_publish = on_publish
client1.connect(broker, port)

model = load_model('keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# ---------- CÁMARA ----------
img_file_buffer = st.camera_input("Toma una Foto")

if img_file_buffer is not None:
    img = Image.open(img_file_buffer)
    img = img.resize((224, 224))
    img_array = np.array(img)

    normalized_image_array = (img_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array

    prediction = model.predict(data)
    print(prediction)
    
    if prediction[0][0] > 0.3:
        st.header("🔓 Abriendo Cerradura")
        client1.publish("AlejoCerradura", json.dumps({"gesto": "Abre"}), qos=0, retain=False)
        time.sleep(0.2)
    elif prediction[0][1] > 0.3:
        st.header("🔒 Cerrando Cerradura")
        client1.publish("AlejoCerradura", json.dumps({"gesto": "Cierra"}), qos=0, retain=False)
        time.sleep(0.2)
    else:
        st.warning("Gesto no reconocido. Intenta nuevamente.")
