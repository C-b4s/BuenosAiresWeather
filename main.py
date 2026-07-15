import os
import requests
import pandas as pd
from datetime import datetime

# FUENTES CONSULTADAS:
# - OpenWeatherMap Current Weather: https://openweathermap.org/current
# - Pandas json_normalize: https://pandas.pydata.org/docs/reference/api/pandas.json_normalize.html
# - Pandas concat: https://pandas.pydata.org/docs/reference/api/pandas.concat.html

# Configuración (Buenos Aires)
API_KEY = "62d2107136670bd7f62c2c23cea30130"
LAT = -34.6037
LON = -58.3816

# Unidades métricas (C° y m/s)
URL = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"

try:
    # Petición al API
    response = requests.get(URL)
    response.raise_for_status()
    data = response.json()

    # Procesamiento dinámico
    df_new = pd.json_normalize(data)

    # Guardar la fecha y hora de la consulta de forma legible
    df_new['dt'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Ruta dinámica para evitar conflictos entre mis compañeros de grupo
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'clima-buenosaires-hoy.csv')

    # Guardado "inteligente" (evita KeyErrors por columnas vacías como rain)
    if os.path.exists(csv_path):
        df_existing = pd.read_csv(csv_path)
        df_all = pd.concat([df_existing, df_new], ignore_index=True)
        df_all.to_csv(csv_path, index=False)
    else:
        df_new.to_csv(csv_path, index=False)

    print("Datos meteorológicos de Buenos Aires agregados con éxito")

except Exception as e:
    print(f"Error en la ejecución: {e}")
