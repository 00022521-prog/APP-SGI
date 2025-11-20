import streamlit as st
from db import run_query, run_query_df

st.set_page_config(page_title="APP-SGI GAPC", layout="wide")

def probar_conexion():
    try:
        resultado = run_query("SELECT 1 AS ok")
        return resultado[0]["ok"] == 1
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return False

def main():
    st.title("APP-SGI - Sistema GAPC SGI (demo conexión)")

    st.subheader("1. Probar conexión a la base de datos")
    if st.button("Probar conexión"):
        if probar_conexion():
            st.success("✅ Conexión correcta a MySQL")
        else:
            st.error("❌ No se pudo conectar a la base de datos")

    st.markdown("---")
    st.subheader("2. Formulario de ejemplo (tabla `prueba`)")

    nombre = st.text_input("Nombre")
    if st.button("Guardar en la tabla prueba"):
        if nombre.strip() == "":
            st.warning("Escribe un nombre primero.")
        else:
            run_query(
                "INSERT INTO prueba (nombre) VALUES (%s)",
                (nombre,),
                fetch=False
            )
            st.success(f"Se guardó '{nombre}' en la base de datos.")

    st.markdown("---")
    st.subheader("3. Registros actuales en `prueba`")

    if st.button("Actualizar listado"):
        df = run_query_df("SELECT id, nombre FROM prueba ORDER BY id DESC")
        if df.empty:
            st.info("No hay registros todavía.")
        else:
            st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()
