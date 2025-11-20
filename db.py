import os
import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd

def _get_mysql_config():
    """
    Devuelve un diccionario con los parámetros de conexión.
    - Si estamos en Clever Cloud: usa variables de entorno del add-on MySQL.
    - Si estamos en local: usa st.secrets["mysql"] (definido en .streamlit/secrets.toml).
    """
    # 1. Ejecutando en Clever Cloud (add-on MySQL)
    if "MYSQL_ADDON_HOST" in os.environ:
        return {
            "host": os.environ["MYSQL_ADDON_HOST"],
            "port": int(os.environ.get("MYSQL_ADDON_PORT", 3306)),
            "database": os.environ["MYSQL_ADDON_DB"],
            "user": os.environ["MYSQL_ADDON_USER"],
            "password": os.environ["MYSQL_ADDON_PASSWORD"],
        }

    # 2. Ejecutando en local con secrets.toml
    cfg = st.secrets["mysql"]
    return {
        "host": cfg["host"],
        "port": int(cfg.get("port", 3306)),
        "database": cfg["database"],
        "user": cfg["user"],
        "password": cfg["password"],
    }

@st.cache_resource
def get_connection():
    config = _get_mysql_config()
    conn = mysql.connector.connect(
        host=config["host"],
        port=config["port"],
        database=config["database"],
        user=config["user"],
        password=config["password"],
    )
    return conn

def run_query(query, params=None, fetch=True, many=False):
    """
    Helper general:
      - fetch=True: devuelve resultados (lista de dicts)
      - fetch=False: solo ejecuta (INSERT/UPDATE/DELETE)
    """
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    if many and isinstance(params, list):
        cur.executemany(query, params)
    else:
        cur.execute(query, params or ())
    if fetch:
        data = cur.fetchall()
        cur.close()
        return data
    else:
        conn.commit()
        cur.close()

def run_query_df(query, params=None):
    data = run_query(query, params=params, fetch=True)
    return pd.DataFrame(data)
