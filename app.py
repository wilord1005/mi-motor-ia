import streamlit as st
import datetime
import json
import io
import re
import concurrent.futures
import requests
from docx import Document
from docx.shared import Pt
import google.generativeai as genai
from groq import Groq
from mistralai import Mistral
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
from google.oauth2 import service_account
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup

# ============================================================
# CONFIG
# ============================================================
st.set_page_config(page_title="Motor Alfa Bravo", page_icon="✈️", layout="wide", initial_sidebar_state="collapsed")

FASES = {
    "F0": "00_Identidad_Motor.docx",
    "F1": "F1.docx", "F2": "F2.docx", "F3": "F3.docx",
    "F4": "F4.docx", "F4.1": "F4.1.docx", "F4.2": "F4.2.docx",
    "F4.3": "F4.3.docx", "F4.4": "F4.4.docx", "F4.5": "F4.5.docx",
    "F4.6": "F4.6.docx", "F5": "F5.docx", "F6": "F6.docx"
}
FASE_NOMBRES = {
    "F0":"Identidad","F1":"Recolección","F2":"Estadística","F3":"Comparación",
    "F4":"Simulación","F4.1":"Estrés","F4.2":"Escenarios","F4.3":"Marcadores",
    "F4.4":"Coherencia","F4.5":"Riesgo","F4.6":"Comparativa","F5":"Picks","F6":"Auditoría"
}

# ============================================================
# CSS (Mantenido igual)
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&display=swap');
html,body,[data-testid="stApp"]{background:#060d18;color:#c8d8e8;font-family:'Rajdhani',sans-serif;}
.hdr{background:linear-gradient(90deg,#070e1a,#0d1e35,#070e1a);border-bottom:2px solid #1e90ff;padding:12px 20px;}
.hdr-title{font-family:'Share Tech Mono',monospace;font-size:18px;color:#1e90ff;letter-spacing:4px;}
.hdr-sub{font-size:10px;color:#2a4a6a;letter-spacing:2px;margin-top:2px;}
.fuente-card{border-radius:4px;padding:8px 12px;margin:4px 0;font-size:12px;line-height:1.5;}
.f-python{background:#071207;border-left:3px solid #00ff88;color:#80d880;}
.f-odds{background:#120c07;border-left:3px solid #f4a300;color:#d4a060;}
.f-football{background:#070d12;border-left:3px solid #00bfff;color:#60b8d8;}
.f-sportsdb{background:#0a0712;border-left:3px solid #c060ff;color:#b080d8;}
.f-gemini{background:#07071a;border-left:3px solid #4285f4;color:#8090f0;}
.f-groq{background:#120707;border-left:3px solid #ff6b35;color:#e09070;}
.f-mistral{background:#0d0712;border-left:3px solid #9b59b6;color:#c090d8;}
.f-usuario{background:#07101a;border-left:3px solid #1e90ff;color:#c8d8e8;}
.debate-box{background:#080f1a;border:1px dashed #1a3a5c;border-radius:4px;padding:10px 14px;margin:6px 0;font-size:11px;color:#4a7a9b;font-family:'Share Tech Mono',monospace;}
.consenso-box{background:linear-gradient(135deg,#071207,#07101a);border:2px solid #1e90ff;border-radius:6px;padding:14px 16px;margin:10px 0;}
.consenso-titulo{font-family:'Share Tech Mono',monospace;font-size:11px;color:#1e90ff;letter-spacing:3px;margin-bottom:8px;}
.badge{display:inline-block;border-radius:2px;padding:1px 6px;font-size:10px;font-family:'Share Tech Mono',monospace;margin-right:4px;}
.b-python{background:#071207;color:#00ff88;border:1px solid #00ff88;}
.b-odds{background:#120c07;color:#f4a300;border:1px solid #f4a300;}
.b-football{background:#070d12;color:#00bfff;border:1px solid #00bfff;}
.b-sportsdb{background:#0a0712;color:#c060ff;border:1px solid #c060ff;}
.b-gemini{background:#07071a;color:#4285f4;border:1px solid #4285f4;}
.b-groq{background:#120707;color:#ff6b35;border:1px solid #ff6b35;}
.b-mistral{background:#0d0712;color:#9b59b6;border:1px solid #9b59b6;}
.b-usuario{background:#07101a;color:#1e90ff;border:1px solid #1e90ff;}
.b-consenso{background:#071a07;color:#00ff88;border:1px solid #00ff88;}
.alerta{background:#120707;border:1px solid #ff3333;border-radius:3px;padding:6px 10px;font-size:11px;color:#ff8888;font-family:'Share Tech Mono',monospace;}
.aprendizaje{background:#071207;border:1px dashed #00ff88;border-radius:3px;padding:6px 10px;font-size:11px;color:#60c870;}
.sdot{display:inline-block;width:7px;height:7px;border-radius:50%;margin-right:5px;animation:pulse 2s infinite;}
.don{background:#00ff88;} .doff{background:#333;}
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:.3;}}
.tab-btn{background:#0a1422;border:1px solid #1a3a5c;border-radius:3px;padding:5px 10px;font-size:11px;cursor:pointer;color:#6a9acb;font-family:'Share Tech Mono',monospace;width:100%;text-align:left;margin:1px 0;}
.tab-active{border-color:#1e90ff!important;color:#1e90ff!important;}
.seccion-header{font-family:'Share Tech Mono',monospace;font-size:10px;color:#2a4a6a;letter-spacing:2px;padding:6px 0;border-bottom:1px solid #1a3a5c;margin-bottom:8px;}
.input-area{background:#060d18;border:1px solid #1a3a5c;border-radius:4px;padding:8px;}
.consola-central{background:linear-gradient(135deg,#060d18,#07101a);border:2px solid #1e90ff;border-radius:6px;}
.cc-header{background:#0a1a2a;border-bottom:1px solid #1e90ff;padding:10px 16px;border-radius:6px 6px 0 0;}
.cc-title{font-family:'Share Tech Mono',monospace;font-size:13px;color:#1e90ff;letter-spacing:3px;}
.cc-sub{font-size:10px;color:#2a4a6a;margin-top:2px;}
div[data-testid="stChatInput"] textarea{background:#060d18!important;color:#c8d8e8!important;font-family:'Share Tech Mono',monospace!important;border:1px solid #1a3a5c!important;font-size:13px!important;}
.stButton>button{background:#0a1422!important;border:1px solid #1a3a5c!important;color:#c8d8e8!important;font-family:'Rajdhani',sans-serif!important;border-radius:3px!important;}
.stButton>button:hover{border-color:#1e90ff!important;color:#1e90ff!important;}
hr{border-color:#1a3a5c!important;}
.stTabs [data-baseweb="tab-list"]{background:#060d18;border-bottom:1px solid #1a3a5c;}
.stTabs [data-baseweb="tab"]{background:#060d18;color:#4a7a9b;font-family:'Share Tech Mono',monospace;font-size:11px;}
.stTabs [aria-selected="true"]{background:#0a1422;color:#1e90ff;border-bottom:2px solid #1e90ff;}
</style>
""", unsafe_html=True)

# ============================================================
# ESTADO E INICIALIZACIÓN
# ============================================================
def init():
    d = {
        "drive_service": None,
        "drive_folder_id": None,
        "fases_cache": {},
        "fase_activa": "F0",
        "datos_compartidos": {},
        "num_aprendizaje": 1,
        "picks_emitidos": [],
        "consola_mensajes": [],
        "fase_mensajes": {f: [] for f in FASES},
        "evento_activo": {},
    }
    for k, v in d.items():
        if k not in st.session_state:
            st.session_state[k] = v
init()

# ============================================================
# FUNCIONES DE IA (CORREGIDAS)
# ============================================================
def gemini(prompt):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-1.5-flash")
        return model.generate_content(prompt).text
    except Exception as e:
        return f"[GEMINI ERROR: {e}]"

def groq_ia(prompt):
    try:
        c = Groq(api_key=st.secrets["GROQ_API_KEY"])
        r = c.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role":"user","content":prompt}],
            max_tokens=3000, temperature=0.1
        )
        return r.choices[0].message.content
    except Exception as e:
        return f"[GROQ ERROR: {e}]"

def mistral_ia(prompt):
    try:
        c = Mistral(api_key=st.secrets["MISTRAL_API_KEY"])
        r = c.chat.complete(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": prompt}]
        )
        return r.choices[0].message.content
    except Exception as e:
        return f"[MISTRAL ERROR: {e}]"

# --- (El resto de tus funciones como conectar_drive, leer_docx, etc. permanecen igual) ---
# [Nota: Debes mantener tus funciones originales de Google Drive y lógica de Motor abajo de esto]
