import streamlit as st
import time

# Configuración de la página para que use todo el ancho del celular o PC
st.set_page_config(page_title="Mi Motor IA - Multimodal", layout="wide")

# Inicializar estados de memoria si no existen
if "eventos_seleccionados" not in st.session_state:
    st.session_state.eventos_seleccionados = []
if "historial_chat" not in st.session_state:
    st.session_state.historial_chat = [
        {"rol": "ChatGPT", "texto": "🤖 [ChatGPT]: Sistema listo. Monitoreando 50 eventos en vivo."},
        {"rol": "Claude", "texto": "🤖 [Claude]: Auditoría activa. Esperando selección de eventos para cruzar con el Word."}
    ]
if "pantalla_completa" not in st.session_state:
    st.session_state.pantalla_completa = False

# --- BOTÓN PARA SECCIÓN 5 (PANTALLA COMPLETA / F6) ---
st.markdown("### 🎛️ Centro de Control de Mi Motor IA")
if st.button("🔄 Cambiar a Sección 5: Modo Pantalla Completa (F6) / Vista Normal"):
    st.session_state.pantalla_completa = not st.session_state.pantalla_completa

st.write("---")

# ==============================================================================
# MODO VISTA NORMAL (SECCIONES 1 A 4)
# ==============================================================================
if not st.session_state.pantalla_completa:
    # Creamos las columnas en la pantalla
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    with col1:
        st.header("📋 Sección 1: Radar F5 (50 Eventos)")
        st.write("⏱️ *Último F5 automático hace 2 minutos*")
        
        # Simulación de eventos
        for i in range(1, 11): # Mostramos 10 por espacio en celular, simula los 50
            nombre_partido = f"Partido En Vivo #{i} - Local vs Visitante"
            cuota = 1.85 + (i * 0.05)
            
            # Checkbox interconectado
            seleccionado = st.checkbox(f"⚽ {nombre_partido} | Cuota: {cuota:.2f}", key=f"chk_{i}")
            if seleccionado and i not in st.session_state.eventos_seleccionados:
                st.session_state.eventos_seleccionados.append(i)
                # Al seleccionar, las IA simulan el inicio del debate en el chat
                st.session_state.historial_chat.append({"rol": "ChatGPT", "texto": f"🤖 [ChatGPT]: Analizando variables F1-F4.6 para el Partido #{i}..."})
                st.session_state.historial_chat.append({"rol": "Claude", "texto": f"🤖 [Claude]: Verificando reglas del Word para el Partido #{i}..."})
            elif not seleccionado and i in st.session_state.eventos_seleccionados:
                st.session_state.eventos_seleccionados.remove(i)

    with col2:
        st.header("📊 Sección 2: Laboratorio Técnico")
        if not st.session_state.eventos_seleccionados:
            st.info("💡 Selecciona eventos en la Sección 1 con el 'Check' para ver las variables F1 a F4.6 aquí.")
        else:
            st.write("### 📈 Variables en Tiempo Real (Excel)")
            for ev in st.session_state.eventos_seleccionados:
                st.success(f"**Partido #{ev}**")
                # Tabla simulada de variables
                st.caption("F1 (Racha): 84% | F2 (Goles): 1.45 | F3 (Cuota Valor): SÍ | F4.6 (Límites): Ajustado")
                st.write("*Debate técnico:* ChatGPT propone sobreapuesta, Claude audita y pide cautela según página 3 del Word.")

    with col3:
        st.header("📢 Sección 3: Veredicto Final")
        if not st.session_state.eventos_seleccionados:
            st.write("Esperando datos digeridos...")
        else:
            st.write("🚨 **Alertas de Confirmación Directa:**")
            for ev in st.session_state.eventos_seleccionados:
                st.warning(f"🎯 [F5 ANÁLISIS] Partido #{ev}: Se cumplen 4 de 5 reglas del Word. Pick Recomendado: Más de 2.5 goles (Cuota Rentable).")

    with col4:
        st.header("💬 Sección 4: Consola Multimodal")
        st.write("Interactúa con el sistema mediante texto, archivos o notas de voz:")
        
        # Mostrar el historial espejo de las IA y tus mensajes
        for msg in st.session_state.historial_chat[-6:]: # Muestra los últimos 6 para no saturar
            st.write(msg["texto"])
            
        # ENTRADAS MULTIMODALES DE LA SECCIÓN 4
        opcion_entrada = st.radio("Elige cómo mandar orden:", ["Texto", "Foto/Archivo", "Nota de Voz"], horizontal=True)
        
        if opcion_entrada == "Texto":
            comando = st.text_input("Escribe tu orden a las IA:", placeholder="Ej: Claude, sube el riesgo a F2...")
            if st.button("Enviar Comando"):
                if comando:
                    st.session_state.historial_chat.append({"rol": "Usuario", "texto": f"👤 [Tú]: {comando}"})
                    st.session_state.historial_chat.append({"rol": "ChatGPT", "texto": "🤖 [ChatGPT]: Orden recibida en tiempo real. Ajustando lógica..."})
                    st.rerun()

        elif opcion_entrada == "Foto/Archivo":
            archivo = st.file_uploader("Sube capturas de cuotas, estadísticas, Excel o PDFs", type=["png", "jpg", "jpeg", "pdf", "xlsx"])
            if archivo:
                st.success(f"¡Archivo '{archivo.name}' cargado con éxito! Las IA lo están leyendo...")

        elif opcion_entrada == "Nota de Voz":
            audio_data = st.audio_input("Toca el micrófono para grabar tu orden por voz")
            if audio_data:
                st.success("🎤 Audio recibido. Transcribiendo y ejecutando con Python en tiempo real...")

# ==============================================================================
# MODO PANTALLA COMPLETA (SECCIONES 5 / F6)
# ==============================================================================
else:
    st.header("🖥️ Sección 5: Editor del Motor (F6) - Modo Pantalla Completa")
    st.info("Estás dentro del código del motor en tiempo real. Las secciones de partidos están ocultas para concentrarte.")
    
    codigo_simulado = """def calcular_motor_apuestas(evento, reglas_word):
    # F1: Análisis de Racha Histórica
    if evento.goles_locales_ultimos_3 > 2:
        F1 = 85  # Regla de la página 2 del Word
    else:
        F1 = 40
    
    # F2: Movimiento de Cuota en vivo (Python F5 en tiempo real)
    F2 = evento.cuota_actual * 1.12
    
    return F1, F2"""
    
    st.text_area("Código Fuente de tu Motor (Modificable por IA o por ti):", value=codigo_simulado, height=250)
    
    st.subheader("🤖 Programación asistida con las IA")
    orden_codigo = st.text_input("Dile a las IA qué cambiar en el código de arriba:", placeholder="Ej: Cambia la regla F1 para que exija 4 goles en vez de 3...")
    if st.button("Reescribir Motor"):
        if orden_codigo:
            st.success("⚡ Python ha modificado el archivo 'app.py' en el servidor en tiempo real basado en tu orden de voz/texto.")
