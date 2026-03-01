import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client, Client
import subprocess # ⚙️ NUEVO: El motor para ejecutar comandos desde la web

# 1. Configuración de la página
st.set_page_config(page_title="Terminal RWA", page_icon="🏦", layout="wide")

# --- ⚡ NUEVO: PANEL LATERAL DE ACCIÓN ---
with st.sidebar:
    st.header("⚡ Comandos Tácticos")
    st.markdown("Fuerza una auditoría manual en tiempo real si detectas volatilidad.")
    st.markdown("---")
    
    if st.button("🥇 Auditar PAX Gold Ahora"):
        with st.spinner("Conectando a la red Ethereum..."):
            subprocess.run(["python", "auditoria_oro.py"])
        st.success("¡Bóveda de oro auditada e inyectada!")
        st.rerun() # 🔄 Recarga la web automáticamente para mostrar el nuevo dato
        
    if st.button("🇺🇸 Auditar BUIDL Ahora"):
        with st.spinner("Cruzando datos con Wall Street..."):
            subprocess.run(["python", "auditoria_buidl.py"])
        st.success("¡Bonos del tesoro inyectados!")
        st.rerun()

# 2. Conexión a tu bóveda
SUPABASE_URL = "https://cxydeqwjpbeueezsunpm.supabase.co"
SUPABASE_KEY = "sb_publishable_IqyYnVgSLraKOdowjreh0Q_L1kpRvUr"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("🏦 Centro de Mando Forense: Wall Street & Oro")

# 3. Extracción de ambos activos
res_paxg = supabase.table('auditorias_paxg').select("*").execute()
res_buidl = supabase.table('auditorias_buidl').select("*").execute()

datos_paxg = res_paxg.data
datos_buidl = res_buidl.data

if datos_paxg and datos_buidl:
    # Preparar datos de Oro
    df_paxg = pd.DataFrame(datos_paxg)
    df_paxg['fecha'] = pd.to_datetime(df_paxg['fecha'])
    df_paxg = df_paxg.sort_values('fecha')

    # Preparar datos de Bonos
    df_buidl = pd.DataFrame(datos_buidl)
    df_buidl['fecha'] = pd.to_datetime(df_buidl['fecha'])
    df_buidl = df_buidl.sort_values('fecha')

    # --- PANEL 1: PAX GOLD ---
    st.markdown("### 🥇 Bóveda de PAX Gold (Oro Físico)")
    col1, col2, col3 = st.columns(3)
    ultimo_paxg = df_paxg.iloc[-1]
    col1.metric("Valor Total (USD)", f"${ultimo_paxg['valor_total_boveda']:,.2f}")
    col2.metric("Precio del Oro", f"${ultimo_paxg['precio_usd']:,.2f}")
    col3.metric("Onzas Respaldadas", f"{ultimo_paxg['onzas_totales']:,.2f}")

    st.markdown("---")

    # --- PANEL 2: BUIDL BLACKROCK ---
    st.markdown("### 🇺🇸 Fondo BUIDL (Bonos del Tesoro)")
    col4, col5, col6 = st.columns(3)
    ultimo_buidl = df_buidl.iloc[-1]
    col4.metric("Valor Institucional (USD)", f"${ultimo_buidl['valor_total_usd']:,.2f}")
    col5.metric("Tokens BUIDL Emitidos", f"{ultimo_buidl['tokens_buidl']:,.2f}")
    col6.metric("Anclaje al Dólar", "$1.00 USD")

    st.markdown("---")

    # --- GRÁFICAS COMPARATIVAS ---
    st.markdown("### Evolución del Valor Histórico")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        fig_paxg = px.line(df_paxg, x='fecha', y='valor_total_boveda', markers=True, title="Reserva de PAX Gold (USD)")
        fig_paxg.update_layout(template="plotly_dark")
        st.plotly_chart(fig_paxg, use_container_width=True)

    with chart_col2:
        fig_buidl = px.line(df_buidl, x='fecha', y='valor_total_usd', markers=True, title="Reserva Institucional BUIDL (USD)")
        fig_buidl.update_layout(template="plotly_dark")
        fig_buidl.update_traces(line_color="#00FFAA") 
        st.plotly_chart(fig_buidl, use_container_width=True)

else:
    st.warning("Faltan datos en alguna de las bóvedas. Usa el menú lateral para extraerlos.")