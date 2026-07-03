import streamlit as st
import datetime
import json
import io
import concurrent.futures
import requests
from docx import Document
from google.generativeai import configure, GenerativeModel
from groq import Groq
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from duckduckgo_search import DDGS

# --- CONFIGURACIÓN Y CSS ---
st.set_page_config(page_title="Motor Alfa Bravo", layout="wide")
st.markdown("<style>body {background:#060d18; color:#c8d8e8;}</style>", unsafe_allow_html=True)

# --- FUNCIONES DE IA (CORREGIDAS) ---
def gemini(prompt):
    try:
        configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = GenerativeModel("gemini-1.5-flash")
        return model.generate_content(prompt).text
    except Exception as e:
        return f"[GEMINI ERROR: {e}]"

def groq_ia(prompt):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[GROQ ERROR: {e}]"

def mistral_ia(prompt):
    try:
        client = MistralClient(api_key=st.secrets["MISTRAL_API_KEY"])
        response = client.chat(
            model="mistral-small-latest",
            messages=[ChatMessage(role="user", content=prompt)]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[MISTRAL ERROR: {e}]"

# --- LÓGICA PRINCIPAL ---
st.title("✈ Motor Alfa Bravo - Consola Central")

comando = st.chat_input("Escribe tu análisis o consulta...")

if comando:
    st.write(f"Procesando: {comando}")
    
    # Ejecución paralela
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        f1 = executor.submit(gemini, comando)
        f2 = executor.submit(groq_ia, comando)
        f3 = executor.submit(mistral_ia, comando)
        
        res1 = f1.result()
        res2 = f2.result()
        res3 = f3.result()
        
    st.subheader("Resultados del Equipo:")
    col1, col2, col3 = st.columns(3)
    col1.markdown(f"**Gemini:**\n{res1}")
    col2.markdown(f"**Groq:**\n{res2}")
    col3.markdown(f"**Mistral:**\n{res3}")
