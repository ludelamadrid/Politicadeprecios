import streamlit as st

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Calculadora IADT",
    page_icon="💊",
    layout="centered"
)

# ---------------- PARAMETROS ----------------
IVA = 10.5  # fijo según política

# ---------------- FUNCIONES ----------------
def obtener_indice(precio):
    if precio <= 11207.45:
        return 2
    elif precio <= 37363.25:
        return 1.8
    elif precio <= 149436.48:
        return 1.6
    elif precio <= 224154.25:
        return 1.4
    else:
        return 1.3


def calcular_precio(base):
    indice = obtener_indice(base)
    final = base * (1 + IVA/100) * indice
    return round(final, 2), indice


# ---------------- UI ----------------
st.title("💊 Calculadora de Precios IADT")
st.caption("Cálculo automático según política institucional")

st.divider()

entrada = st.text_area(
    "Precios sin IVA",
    placeholder="Ej: 11200, 20000, 80000"
)

st.divider()

# ---------------- CALCULO AUTOMATICO ----------------
if entrada.strip():
    try:
        lista_texto = entrada.split(",")
        precios = [float(a.strip()) for a in lista_texto]

        st.success("Resultados")

        for i, base in enumerate(precios, start=1):
            final, indice = calcular_precio(base)
            st.text(f"Producto {i}: ${base} → ${final} (índice {indice})")

    except ValueError:
        st.error("Error: ingresá solo números separados por coma")

st.divider()

st.caption(f"IVA aplicado automáticamente: {IVA}%")
st.caption("Herramienta interna - uso profesional")
