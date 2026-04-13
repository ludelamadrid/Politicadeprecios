import streamlit as st
import pandas as pd

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Calculadora IADT",
    page_icon="💊",
    layout="wide"
)

# ---------------- PARAMETROS ----------------
IVA = 10.5

# ---------------- TABLA INICIAL ----------------
tabla_default = pd.DataFrame({
    "Desde": [0, 11207.45, 37363.25, 149436.48, 224154.25],
    "Hasta": [11207.45, 37363.25, 149436.48, 224154.25, None],
    "Indice": [2, 1.8, 1.6, 1.4, 1.3]
})

# Persistencia en sesión
if "tabla" not in st.session_state:
    st.session_state.tabla = tabla_default

# ---------------- FUNCIONES ----------------
def obtener_indice(precio, tabla):
    for _, fila in tabla.iterrows():
        desde = fila["Desde"]
        hasta = fila["Hasta"]
        indice = fila["Indice"]

        if pd.isna(hasta):
            if precio >= desde:
                return indice
        elif desde <= precio <= hasta:
            return indice

    return None


def calcular_precio(base, tabla):
    indice = obtener_indice(base, tabla)
    final = base * (1 + IVA/100) * indice
    return round(final, 2), indice


def formato_ar(numero):
    return f"{numero:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ---------------- UI ----------------
st.title("💊 Calculadora de Precios IADT")
st.caption("Cálculo automático según política institucional")

col1, col2 = st.columns([1, 1])

# ----------- CALCULADORA -----------
with col1:
    st.subheader("Carga de precios")

    entrada = st.text_area(
        "Precios sin IVA",
        placeholder="Ej: 11200, 20000, 80000"
    )

    if st.button("Calcular precios", use_container_width=True):

        if not entrada.strip():
            st.warning("Ingresá al menos un precio")
        else:
            try:
                lista_texto = entrada.split(",")
                precios = [float(a.strip()) for a in lista_texto]

                resultados_texto = []

                for i, base in enumerate(precios, start=1):
                    final, indice = calcular_precio(base, st.session_state.tabla)

                    base_fmt = formato_ar(base)
                    final_fmt = formato_ar(final)

                    resultados_texto.append(
                        f"Producto {i}: ${base_fmt} → ${final_fmt} (índice {indice})"
                    )

                resultado_final = " ; ".join(resultados_texto)

                st.success("Resultados")
                st.text(resultado_final)
                st.code(resultado_final)

            except ValueError:
                st.error("Error: ingresá solo números separados por coma")


# ----------- TABLA EDITABLE -----------
with col2:
    st.subheader("Bandas de costos (editable)")

    tabla_editada = st.data_editor(
        st.session_state.tabla,
        num_rows="dynamic",
        use_container_width=True
    )

    # Guardar cambios automáticamente
    st.session_state.tabla = tabla_editada

st.divider()

st.caption(f"IVA aplicado automáticamente: {IVA}%")
st.caption("La tabla de bandas es editable y define el cálculo")

st.caption(f"IVA aplicado automáticamente: {IVA}%")
st.caption("Herramienta interna - uso profesional")
