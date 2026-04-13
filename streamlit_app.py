import streamlit as st

import streamlit as st

import streamlit as st

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Calculadora politica de precios",
    page_icon="💊",
    layout="centered"
)

# ---------------- FUNCION ----------------
def precios_de_venta(precios, iva, margen):
    resultado = []
    for a in precios:
        precio = a * (1 + iva/100) * (1 + margen/100)
        resultado.append(round(precio, 2))
    return resultado

# ---------------- UI ----------------
st.title("💊 Calculadora de Precios")
st.caption("Cálculo automático según política institucional. Carga cada valor separados por una coma")

st.divider()

# Inputs principales
entrada = st.text_area(
    "Precios sin IVA",
    placeholder="Ej: 100, 250.5, 300"
)

col1, col2 = st.columns(2)

with col1:
    iva = st.number_input("IVA (%)", value=10.5, step=0.1)

with col2:
    margen = st.number_input("Margen (%)", value=30.0, step=0.1)

st.divider()

# Botón de cálculo
if st.button("Calcular precios", use_container_width=True):

    if not entrada.strip():
        st.warning("Ingresá al menos un precio")
    else:
        try:
            lista_texto = entrada.split(",")
            precios = [float(a.strip()) for a in lista_texto]

            resultado = precios_de_venta(precios, iva, margen)

            st.success("Resultados")

            for i, (base, final) in enumerate(zip(precios, resultado), start=1):
                st.text(f"Producto {i}: ${base} → ${final}")

        except ValueError:
            st.error("Error: asegurate de ingresar solo números separados por coma")

st.divider()

st.caption("Herramienta interna - uso profesional")
