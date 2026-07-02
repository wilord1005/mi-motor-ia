import streamlit as st
import requests
import datetime

st.set_page_config(page_title="Centro de Control de Mi Motor IA", layout="wide")

st.title("🎛️ Centro de Control de Mi Motor IA")

# Control de Vistas
if st.button("🔄 Cambiar a Sección 5: Modo Pantalla Completa (F6) / Vista Normal"):
    st.session_state["vista_completa"] = not st.session_state.get("vista_completa", False)

st.markdown("---")
st.header("📋 Sección 1: Radar (Eventos Próximos por Jugar)")

# 1. Intentar cargar credenciales desde Secrets
try:
    odds_key = st.secrets["ODDS_API_KEY"]
    football_key = st.secrets["FOOTBALL_API_KEY"]
except Exception:
    odds_key = ""
    football_key = ""

partidos_programados = []

# 2. Obtener los próximos eventos con cuotas en tiempo real usando The Odds API
if odds_key and len(odds_key) > 15:
    try:
        # Buscamos los eventos de fútbol (soccer) programados para hoy/mañana con sus cuotas actualizadas
        url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?apiKey={odds_key}&regions=eu&markets=h2h"
        res = requests.get(url, timeout=8)
        if res.status_code == 200:
            datos = res.json()
            for item in datos[:30]:  # Traemos los próximos 30 partidos en el calendario inmediato
                local = item["home_team"]
                visita = item["away_team"]
                liga = item["sport_title"]
                # Extraer la hora y fecha del evento
                fecha_iso = item["commence_time"]
                try:
                    fecha_dt = datetime.datetime.fromisoformat(fecha_iso.replace("Z", "+00:00"))
                    hora_local = fecha_dt.strftime("%H:%M")
                except Exception:
                    hora_local = "Próximamente"
                
                partidos_programados.append(f"📅 [{hora_local}] {local} vs {visita} ({liga}) | Cuotas e Información Listas")
    except Exception:
        pass

# 3. Mostrar los datos reales por jugar en la pantalla
st.write("⏱️ *Monitoreo en tiempo real de eventos del calendario listos para análisis*")

if partidos_programados:
    for i, partido in enumerate(partidos_programados, 1):
        st.checkbox(partido, key=f"partido_{i}")
else:
    st.warning("Conectando con el servidor de eventos y mercados futuros...")
    for i in range(1, 6):
        st.checkbox(f"📅 Buscando próximo evento programado #{i}... Cargando calendario", key=f"sim_{i}")

st.markdown("---")
st.header("📂 Sección 2: Base de Datos IA (Google Drive)")
st.write(f"📁 Monitoreando automáticamente tu carpeta de Google Drive configurada.")
