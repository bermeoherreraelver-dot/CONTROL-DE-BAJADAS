# PROYECTO: SISTEMA DE VIDEO VIGILANCIA Y SEGURIDAD - HOSPITAL ESSALUD CAJAMARCA

## 1. INTRODUCCIÓN
Este documento resume la ingeniería técnica y el plan de configuración para el sistema de CCTV del Hospital Especializado de Cajamarca. El sistema consta de 302 cámaras IP, 6 NVRs, servidores redundantes y un sistema de videowall de 8 monitores.

---

## 2. PLAN DE DIRECCIONAMIENTO IP (SEGMENTACIÓN POR VLANS)
Para garantizar la seguridad y el rendimiento, se propone la siguiente segmentación de red:

| VLAN | PROPÓSITO | RANGO DE RED | MÁSCARA | GATEWAY |
| :--- | :--- | :--- | :--- | :--- |
| **VLAN 10** | Servidores y Gestión | 10.0.10.0/24 | 255.255.255.0 | 10.0.10.1 |
| **VLAN 20** | Cámaras IP (Video) | 10.0.20.0/23 | 255.255.254.0 | 10.0.20.1 |
| **VLAN 30** | Visualización y Control | 10.0.30.0/24 | 255.255.255.0 | 10.0.30.1 |

### Distribución de IPs Críticas:
- **Servidores Admin (HA):** 10.0.10.10, 10.0.10.11
- **Servidores VMS (HA):** 10.0.10.20, 10.0.10.21
- **NVRs (1 al 6):** 10.0.10.31 - 10.0.10.36
- **Cámaras IP:** 10.0.20.10 en adelante.

---

## 3. CÁLCULO DE ALMACENAMIENTO Y SERVIDORES
Basado en las EETT y MD del proyecto (30 días de grabación mínima):

*   **Demanda Total Aproximada:** ~138.5 TB (con Smart H.265+ y regla 70/30 actividad).
*   **Capacidad por NVR:** 48TB Brutos (8 discos de 6TB SAS).
*   **Configuración RAID 6:** 2 discos de redundancia por NVR -> 36TB Útiles por NVR.
*   **Capacidad Total del Sistema:** 216 TB Útiles (Suficiente para cumplir los 30 días exigidos).

---

## 4. ARQUITECTURA DE REDUNDANCIA Y CENTRO DE CONTROL

### Redundancia 1+1 (Alta Disponibilidad)
- Configuración de clúster **Activo-Pasivo**.
- Uso de **IP Virtual (VIP)** para que las cámaras no pierdan conexión en caso de fallo del servidor principal.
- Sincronización de Base de Datos en tiempo real (Hot Standby).

### Centro de Control (Videowall)
- **Arreglo:** 4x2 (8 monitores de 50").
- **Conexión:** Daisy Chain (Cascada) mediante DisplayPort para optimizar el cableado.
- **Gestión:** Matriz Virtual controlada por estación de trabajo profesional con aceleración GPU.

---

## 5. AUTOMATIZACIÓN (SCRIPT DE CONFIGURACIÓN DAHUA)
He desarrollado un script para que tus técnicos asignen IPs automáticamente evitando el trabajo manual puerto por puerto.

---

## 6. MANUAL DE EJECUCIÓN POR FASES
1. **Fase 1 (Lab):** Configuración de RAID 6 y actualización de Firmwares.
2. **Fase 2 (Infra):** Despliegue de Fibra Óptica y Switches PoE por cada cuarto de comunicaciones.
3. **Fase 3 (Core):** Instalación de Servidores en Clúster (Redundancia 1+1).
4. **Fase 4 (Campo):** Montaje y direccionamiento de cámaras mediante script.
5. **Fase 5 (Control):** Calibración de Videowall y Reglas de Analítica IVS.
