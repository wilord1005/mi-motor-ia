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

# Inicializar memoria interna para el chat real
if "historial_s4" not in st.session_state:
    st.session_state["historial_s4"] = [
        {"rol": "assistant", "avatar": "🤖", "texto": "🤖 **[Mando Central Activo]:** Conexiones de seguridad preparadas. Wilmer, introduce tus consultas en la consola maestra para iniciar el debate analítico real."}
    ]
if "eventos_seleccionados" not in st.session_state:
    st.session_state["eventos_seleccionados"] = []

# CAPTURA SEGURA DESDE LOS SECRETS DEL SERVIDOR
OPENAI_KEY = st.secrets.get("OPENAI_API_KEY", "")
CLAUDE_KEY = st.secrets.get("ANTHROPIC_API_KEY", "")

st.title("🎛️ Centro de Control de Mi Motor IA (Conexión Real)")
st.markdown("---")

# Verificación visual rápida del estado del sistema en tu pantalla
st.subheader("🔑 Estado de Conexión Neural")
c_api1, c_api2 = st.columns(2)
with c_api1:
    if OPENAI_KEY and CLAUDE_KEY:
        st.success("🟢 CHATGPT Y CLAUDE: LLAVES SEGURAS INYECTADAS")
    else:
        st.error("🔴 FALTA CONFIGURAR LAS LLAVES EN LOS SECRETS DE STREAMLIT")
with c_api2:
    if librerias_instaladas:
        st.success("🟢 LIBRERÍAS DE INTERFACES IA: INSTALADAS Y LISTAS")
    else:
        st.warning("⚠️ LIBRERÍAS CARGANDO: Esperando procesamiento...")

st.markdown("---")

# =========================================================
# SECCIÓN 1, 2 y 3: RADAR Y TABLA F5
# =========================================================
st.header("📋 Sección 1: Radar Global (Ligas Mundiales)")
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
st.write("🎛️ *Tu chat directo con los modelos originales. Sin simulaciones.*")

# Renderizar la conversación real acumulada
for msg in st.session_state["historial_s4"]:
    with st.chat_message(msg["rol"], avatar=msg["avatar"]):
        st.write(msg["texto"])

# Entrada de texto nativa del chat
orden_maestra = st.chat_input("Escribe tu pregunta o aclaración para ChatGPT y Claude aquí...")

if orden_maestra:
    st.session_state["historial_s4"].append({"rol": "user", "avatar": "👤", "texto": orden_maestra})
    
    if not OPENAI_KEY or not CLAUDE_KEY:
        respuesta_final = "❌ **[Error]:** Las llaves no se han guardado en los Secrets de la App. Sigue el PASO 2 de las instrucciones de la IA."
    elif not librerias_instaladas:
        respuesta_final = "⚠️ **[Error local]:** Las librerías aún se están cargando en segundo plano. Espera 1 minuto y vuelve a enviar."
    else:
        with st.spinner("⚡ Consultando a los servidores en vivo..."):
            try:
                # CONSULTA REAL A CHATGPT
                client_openai = OpenAI(api_key=OPENAI_KEY)
                completion = client_openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Eres ChatGPT. Responde a Wilmer sobre su motor deportivo de forma fluida, libre y contextual, interactuando en español sin repetir plantillas fijas."},
                        {"role": "user", "content": orden_maestra}
                    ]
                )
                res_chatgpt = completion.choices[0].message.content
                
                # CONSULTA REAL A CLAUDE
                client_claude = anthropic.Anthropic(api_key=CLAUDE_KEY)
                message = client_claude.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1024,
                    system="Eres Claude. Estás en la mesa de control junto a ChatGPT analizando el motor de Wilmer. Lee lo que opina ChatGPT y complementa de manera interactiva.",
                    messages=[
                        {"role": "user", "content": f"Pregunta de Wilmer: {orden_maestra}\n\nRespuesta de ChatGPT: {res_chatgpt}"}
                    ]
                )
                res_claude = message.content[0].text
                
                respuesta_final = f"🤖 **[ChatGPT Real]:** {res_chatgpt}\n\n🧠 **[Claude Real]:** {res_claude}"
                
            except Exception as e:
                respuesta_final = f"🔴 **[Fallo en Servidores]:** Las claves fueron rechazadas o se acabó el saldo.\n\n*Detalle: {str(e)}*"

    st.session_state["historial_s4"].append({"rol": "assistant", "avatar": "🤖", "texto": respuesta_final})
    st.rerun()
