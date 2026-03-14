import requests
from requests.auth import HTTPDigestAuth
import time

# --- CONFIGURACIÓN BASE ---
IP_POR_DEFECTO = "192.168.1.108" # IP de fábrica de Dahua
USUARIO = "admin"
PASSWORD_DEFECTO = "admin123" # CAMBIAR POR LA CONTRASEÑA DEFINIDA PARA EL HOSPITAL

# --- NUEVO PLAN DE DIRECCIONAMIENTO ---
NUEVO_RANGO_BASE = "10.0.20."
NUEVA_MASCARA = "255.255.254.0"
NUEVO_GATEWAY = "10.0.20.1"

# Iniciar contador para la primera cámara (VLAN 20)
contador_ip = 10 

def cambiar_ip_dahua(ip_actual, nueva_ip):
    # Dahua CGI API para configurar red
    url = f"http://{ip_actual}/cgi-bin/configManager.cgi?action=setConfig&Network.eth0.IPAddress={nueva_ip}&Network.eth0.SubnetMask={NUEVA_MASCARA}&Network.eth0.DefaultGateway={NUEVO_GATEWAY}"
    
    print(f"[*] Intentando configurar cámara en {ip_actual}...")
    try:
        response = requests.get(url, auth=HTTPDigestAuth(USUARIO, PASSWORD_DEFECTO), timeout=5)
        
        if response.status_code == 200:
            print(f"[+] ÉXITO: Cámara movida a {nueva_ip}")
            return True
        else:
            print(f"[-] ERROR {response.status_code}: Verifica usuario/password.")
            return False
            
    except Exception as e:
        print(f"[-] ERROR DE CONEXIÓN: {e}")
        return False

print("=== ASIGNADOR DE IPs CCTV HOSPITAL CAJAMARCA ===")
while True:
    input(f"\nConecta la cámara y presiona ENTER para asignarle la IP {NUEVO_RANGO_BASE}{contador_ip}...")
    nueva_ip = f"{NUEVO_RANGO_BASE}{contador_ip}"
    if cambiar_ip_dahua(IP_POR_DEFECTO, nueva_ip):
        contador_ip += 1
        print("Cámara lista. Desconéctala y conecta la siguiente.")
    else:
        print("Reintenta con la misma cámara.")
