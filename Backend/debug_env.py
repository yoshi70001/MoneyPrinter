import os
from dotenv import load_dotenv
 
# Construye la ruta absoluta al archivo .env
backend_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(backend_dir, os.pardir))
dotenv_path = os.path.join(project_root, ".env")
print(f"Buscando el archivo .env en: {dotenv_path}")
# Carga el archivo .env
load_ok = load_dotenv(dotenv_path=dotenv_path)
    
if os.path.exists(dotenv_path):
    print("-> El archivo .env FUE ENCONTRADO.")
    if load_ok:
        print("-> El archivo .env se cargó correctamente.")
    else:
        print("-> ERROR: El archivo .env fue encontrado, pero no se pudo cargar. Revisa su contenido.")
else:
    print("-> ERROR: El archivo .env NO FUE ENCONTRADO en la ruta especificada.")
# Lee las variables de entorno específicas
pexels_api_key = os.getenv("PEXELS_API_KEY")
tiktok_session_id = os.getenv("TIKTOK_SESSION_ID")
imagemagick_binary = os.getenv("IMAGEMAGICK_BINARY")
# Imprime los resultados
print("\n--- Valores de las Variables de Entorno ---")
print(f"PEXELS_API_KEY: {pexels_api_key}")
print(f"TIKTOK_SESSION_ID: {tiktok_session_id}")
print(f"IMAGEMAGICK_BINARY: {imagemagick_binary}")
print("-----------------------------------------")
if not all([pexels_api_key, tiktok_session_id, imagemagick_binary]):
    print("\n[!] Una o más variables requeridas faltan. Por favor, revisa el contenido y el nombre de tu archivo .env.")
else:
    print("\n[+] Todas las variables requeridas parecen estar cargadas correctamente.")