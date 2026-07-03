import streamlit as st
import requests
import datetime

# 1. INTENTAR CARGAR LIBRERÍAS DE IA OFICIALES
try:
    from openai import OpenAI
    import anthropic
    librerias_instaladas = True
except ImportError:
    librerias_instaladas = False

# Configuración de diseño de la pantalla
st.set_page_config(page_title="Centro de Control de Mi Motor IA", layout="wide")

# Inicializar memoria interna para el chat real si no existe
if "historial_s4" not in st.session_state:
    st.session_state["historial_s4"] = [
        {"rol": "assistant", "avatar": "🤖", "texto": "🤖 **[Mando Central Activo]:** Conexiones seguras inyectadas desde tus Secrets. Wilmer, la mesa de debate real con ChatGPT y Claude está lista y estable. Haz tus consultas continuamente sin bloqueos."}
    ]
if "eventos_seleccionados" not in st.session_state:
    st.session_state["eventos_seleccionados"] = []

# LECTURA AUTOMÁTICA Y SEGURA DESDE TUS SECRETS
OPENAI_KEY = st.secrets.get("OPENAI_API_KEY", "")
CLAUDE_KEY = st.secrets.get("ANTHROPIC_API_KEY", "")
ODDS_KEY = st.secrets.get("ODDS_API_KEY", "")
FOOTBALL_KEY = st.secrets.get("FOOTBALL_API_KEY", "")
DRIVE_URL = st.secrets.get("GOOGLE_DRIVE_FOLDER_URL", "")

st.title("🎛️ Centro de Control de Mi Motor IA (Conexión Real)")
st.markdown("---")

# Verificación visual rápida del estado del sistema en tu pantalla
st.subheader("🔑 Estado de Conexión Neural")
c_api1, c_api2, c_api3 = st.columns(3)
with c_api1:
    if OPENAI_KEY and CLAUDE_KEY:
        st.success("🟢 IA: LLAVES INYECTADAS DESDE SECRETS")
    else:
        st.error("🔴 IA: REVISA LOS NOMBRES EN SECRETS")
with c_api2:
    if ODDS_KEY and FOOTBALL_KEY:
        st.success("🟢 CUOTAS: PROVEEDORES DUALES ACTIVOS")
    else:
        st.warning("⚠️ CUOTAS: Falta alguna llave de deportes")
with c_api3:
    if librerias_instaladas:
        st.success("🟢 SISTEMA: LIBRERÍAS IA LISTAS")
    else:
        st.error("🔴 REQUISITOS: Agrega openai y anthropic a requirements.txt")

st.markdown("---")

# =========================================================
# SECCIÓN 1, 2 y 3: RADAR Y TABLA F5
# =========================================================
st.header("📋 Sección 1: Radar Global (Ligas Mundiales)")
st.write(f"📂 Conectado al repositorio Drive: [Abrir Carpeta de Trabajo]({DRIVE_URL})")

partidos_respaldo = [
    {"id": "RM_FCB", "titulo": "⚽ Real Madrid vs Barcelona", "liga": "La Liga", "minutos": 15, "cantidad_datos": 1450, "picks": [{"nombre": "Gana Local", "cuota": 1.85, "prob": 74.2}]},
    {"id": "MC_LIV", "titulo": "⚽ Manchester City vs Liverpool", "liga": "Premier League", "minutos": 35, "datos": 1380, "picks": [{"nombre": "Más de 1.5 Goles", "cuota": 1.28, "prob": 69.1}]}
]

tab1, tab2 = st.tabs(["🎯 Top 10", "🗂️ Lista Completa"])
with tab1:
    for i, ev in enumerate(partidos_respaldo, 1):
        with st.expander(f"⭐ [TOP {i}] {ev['titulo']}"):
            st.write(f"👉 Pick: {ev['picks'][0]['nombre']} | Probabilidad: {ev['picks'][0]['prob']}%")
with tab2:
    seleccionados = []
    for ev in partidos_respaldo:
        if st.checkbox(f"Seleccionar {ev['titulo']}", key=f"chk_{ev['id']}"):
            seleccionados.append(ev)
    st.session_state["eventos_seleccionados"] = seleccionados

st.markdown("---")

# =========================================================
# 💬 SECCIÓN 4: CONSOLA DE CONTROL MAESTRO INTERACTIVA REAL
# =========================================================
st.header("💬 Sección 4: Consola de Control Maestro")
st.write("🎛️ *Tu chat directo con los modelos originales conectados a tus APIs.*")

# Renderizar la conversación real acumulada
for msg in st.session_state["historial_s4"]:
    with st.chat_message(msg["rol"], avatar=msg["avatar"]):
        st.write(msg["texto"])

# Entrada de texto nativa del chat
orden_maestra = st.chat_input("Escribe tu pregunta o aclaración para ChatGPT y Claude aquí...")

if orden_maestra:
    # Guardar la pregunta de Wilmer en el historial de inmediato
    st.session_state["historial_s4"].append({"rol": "user", "avatar": "👤", "texto": orden_maestra})
    
    if not OPENAI_KEY or not CLAUDE_KEY:
        respuesta_final = "❌ **[Error]:** No puedo leer las llaves de acceso. Verifica que en tus Secrets de Streamlit estén escritas exactamente como `OPENAI_API_KEY` y `ANTHROPIC_API_KEY`."
    elif not librerias_instaladas:
        respuesta_final = "⚠️ **[Error local]:** Las librerías de comunicación de IA no están listas en el servidor. Asegúrate de haber completado el archivo `requirements.txt`."
    else:
        with st.spinner("⚡ Conectando con los servidores de OpenAI y Anthropic en vivo..."):
            try:
                # CONSULTA REAL A CHATGPT (OpenAI)
                client_openai = OpenAI(api_key=OPENAI_KEY)
                completion = client_openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Eres ChatGPT. Estás en el panel de control de Wilmer para auditar su motor deportivo. Habla de forma natural, fluida, inteligente y en español, analizando el contexto de lo que te pida."},
                        {"role": "user", "content": orden_maestra}
                    ]
                )
                res_chatgpt = completion.choices[0].message.content
                
                # CONSULTA REAL A CLAUDE (Anthropic)
                client_claude = anthropic.Anthropic(api_key=CLAUDE_KEY)
                message = client_claude.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1024,
                    system="Eres Claude. Haces equipo con ChatGPT en el motor deportivo de Wilmer. Lee la consulta de Wilmer y lo que respondió ChatGPT, y genera un debate complementario fluido en español.",
                    messages=[
                        {"role": "user", "content": f"Pregunta de Wilmer: {orden_maestra}\n\nRespuesta de ChatGPT: {res_chatgpt}"}
                    ]
                )
                res_claude = message.content[0].text
                
                respuesta_final = f"🤖 **[ChatGPT Real]:** {res_chatgpt}\n\n🧠 **[Claude Real]:** {res_claude}"
                
            except Exception as e:
                respuesta_final = f"🔴 **[Fallo en Servidores de IA]:** La conexión falló. Verifica si las llaves tienen saldo o si el formato en Secrets tiene algún error.\n\n*Detalle técnico: {str(e)}*"

    # Guardar respuesta y recargar aplicación para mostrarla limpia
    st.session_state["historial_s4"].append({"rol": "assistant", "avatar": "🤖", "texto": respuesta_final})
    st.rerun()
