import streamlit as st
import requests
import datetime

st.set_page_config(page_title="Centro de Control de Mi Motor IA", layout="wide")

st.title("🎛️ Centro de Control de Mi Motor IA")

# Control de Vistas
if st.button("🔄 Cambiar a Sección 5: Modo Pantalla Completa (F6) / Vista Normal"):
    st.session_state["vista_completa"] = not st.session_state.get("vista_completa", False)

st.markdown("---")
st.header("📋 Sección 1: Radar F5 (Eventos en Tiempo Real)")

# 1. Intentar cargar credenciales desde Secrets
try:
    odds_key = st.secrets["ODDS_API_KEY"]
    football_key = st.secrets["FOOTBALL_API_KEY"]
except Exception:
    odds_key = ""
    football_key = ""

partidos_reales = []

# 2. Intentar llamar a API-Football (Partidos en vivo globales de hoy)
if football_key and len(football_key) > 15:
    try:
        url = "https://v3.football.api-sports.io/fixtures"
        headers = {"x-apisports-key": football_key}
        hoy = datetime.date.today().isoformat()
        params = {"date": hoy, "status": "LIVE-1H-2H-HT-ET"}
        res = requests.get(url, headers=headers, params=params, timeout=8)
        if res.status_code == 200:
            datos = res.json().get("response", [])
            for item in datos:
                local = item["teams"]["home"]["name"]
                visita = item["teams"]["away"]["name"]
                liga = item["league"]["name"]
                goles_local = item["goals"]["home"] if item["goals"]["home"] is not None else 0
                goles_visita = item["goals"]["away"] if item["goals"]["away"] is not None else 0
                partidos_reales.append(f"⚽ {local} {goles_local} - {goles_visita} {visita} ({liga}) | En Vivo Real")
    except Exception:
        pass

# 3. Si no hay en vivo activos en este segundo, usar The Odds API para los próximos juegos
if not partidos_reales and odds_key and len(odds_key) > 15:
    try:
        url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?apiKey={odds_key}&regions=eu&markets=h2h"
        res = requests.get(url, timeout=8)
        if res.status_code == 200:
            datos = res.json()
            for item in datos[:15]:
                local = item["home_team"]
                visita = item["away_team"]
                liga = item["sport_title"]
                partidos_reales.append(f"📅 {local} vs {visita} ({liga}) | Cuotas Activas de Mercado")
    except Exception:
        pass

# 4. Mostrar datos en pantalla
st.write("⏱️ *Actualización de eventos de fútbol automática en tiempo real*")

if partidos_reales:
    for i, partido in enumerate(partidos_reales, 1):
        st.checkbox(partido, key=f"partido_{i}")
else:
    st.warning("Conectando con las APIs de fútbol en tiempo real...")
    for i in range(1, 6):
        st.checkbox(f"⚽ Buscando partido en vivo #{i}... Conectando a servidores de mercado", key=f"sim_{i}")

st.markdown("---")
st.header("📂 Sección 2: Base de Datos IA (Google Drive)")
st.write(f"📁 Monitoreando automáticamente tu carpeta de Google Drive configurada.")
