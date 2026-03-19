"""
Genera el ícono para la aplicación Control de Bajadas de Simplify RRHH.
Diseño: Escudo con avión estilizado + calendario sobre fondo azul corporativo.
Salida: icon.ico (multi-resolución) y icon.png (256x256)
"""
from PIL import Image, ImageDraw, ImageFont
import math, os

SIZE = 256
img = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# === FONDO: Círculo con degradado azul corporativo ===
cx, cy = SIZE // 2, SIZE // 2
radius = 120

for r in range(radius, 0, -1):
    ratio = r / radius
    # Degradado de azul oscuro (#142132) a azul medio (#1e3a5f)
    red = int(20 + (30 - 20) * (1 - ratio))
    green = int(33 + (58 - 33) * (1 - ratio))
    blue = int(50 + (95 - 50) * (1 - ratio))
    draw.ellipse(
        [cx - r, cy - r, cx + r, cy + r],
        fill=(red, green, blue, 255)
    )

# Borde exterior con glow sutil
for i in range(3):
    offset = i + 1
    alpha = 100 - i * 30
    draw.ellipse(
        [cx - radius - offset, cy - radius - offset,
         cx + radius + offset, cy + radius + offset],
        outline=(40, 169, 224, alpha), width=1
    )

# === AVIÓN ESTILIZADO (triángulo + alas) ===
# Posición centrada, ligeramente arriba
plane_cx, plane_cy = cx, cy - 15

# Fuselaje del avión (forma simplificada apuntando arriba-derecha)
# Triángulo principal
plane_color = (255, 255, 255, 240)
accent_color = (40, 169, 224, 255)  # Cyan corporativo

# Avión simplificado - cuerpo
body_points = [
    (plane_cx + 45, plane_cy - 40),   # Punta (nariz)
    (plane_cx + 10, plane_cy - 10),    # Centro superior
    (plane_cx - 35, plane_cy + 30),    # Cola
    (plane_cx - 25, plane_cy + 35),    # Cola inferior
    (plane_cx + 5, plane_cy + 5),      # Centro inferior
]
draw.polygon(body_points, fill=plane_color)

# Ala superior
wing_top = [
    (plane_cx + 10, plane_cy - 10),
    (plane_cx - 30, plane_cy - 40),
    (plane_cx - 40, plane_cy - 35),
    (plane_cx - 5, plane_cy + 0),
]
draw.polygon(wing_top, fill=(200, 220, 255, 220))

# Ala inferior
wing_bot = [
    (plane_cx + 5, plane_cy + 5),
    (plane_cx - 20, plane_cy + 35),
    (plane_cx - 30, plane_cy + 30),
    (plane_cx - 5, plane_cy + 0),
]
draw.polygon(wing_bot, fill=(200, 220, 255, 220))

# Estela del avión (líneas curvas)
for i in range(3):
    y_off = -15 + i * 12
    start_x = plane_cx - 35 + i * 5
    draw.arc(
        [start_x - 40, plane_cy + y_off + 20, start_x, plane_cy + y_off + 40],
        start=160, end=220,
        fill=(40, 169, 224, 120 - i * 30), width=2
    )

# === CALENDARIO (esquina inferior derecha) ===
cal_x, cal_y = cx + 25, cy + 30
cal_w, cal_h = 50, 45

# Sombra
draw.rounded_rectangle(
    [cal_x + 2, cal_y + 2, cal_x + cal_w + 2, cal_y + cal_h + 2],
    radius=6, fill=(0, 0, 0, 60)
)

# Cuerpo del calendario
draw.rounded_rectangle(
    [cal_x, cal_y, cal_x + cal_w, cal_y + cal_h],
    radius=6, fill=(255, 255, 255, 240)
)

# Header del calendario (rojo)
draw.rounded_rectangle(
    [cal_x, cal_y, cal_x + cal_w, cal_y + 14],
    radius=6, fill=(220, 53, 69, 255)
)
# Tapar los bordes redondeados inferiores del header
draw.rectangle(
    [cal_x, cal_y + 8, cal_x + cal_w, cal_y + 14],
    fill=(220, 53, 69, 255)
)

# Checkmark en el calendario (indica "aprobado/completado")
check_color = (34, 197, 94, 255)  # Verde
check_points = [
    (cal_x + 12, cal_y + 28),
    (cal_x + 20, cal_y + 36),
    (cal_x + 38, cal_y + 22),
]
draw.line(check_points, fill=check_color, width=4)

# Puntos del calendario (días)
dot_color = (150, 160, 180, 180)
for row in range(2):
    for col in range(4):
        dx = cal_x + 10 + col * 10
        dy = cal_y + 20 + row * 10
        if not (row == 0 and col >= 1 and col <= 3) and not (row == 1 and col >= 0 and col <= 2):
            draw.ellipse([dx - 1, dy - 1, dx + 1, dy + 1], fill=dot_color)

# === BADGE "S" (Simplify) esquina superior izquierda ===
badge_cx, badge_cy = cx - 70, cy - 70
badge_r = 18

# Fondo del badge
draw.ellipse(
    [badge_cx - badge_r, badge_cy - badge_r, badge_cx + badge_r, badge_cy + badge_r],
    fill=(40, 169, 224, 255)
)

# Letra "S"
try:
    font_s = ImageFont.truetype("arial.ttf", 22)
except:
    font_s = ImageFont.load_default()

draw.text((badge_cx - 7, badge_cy - 13), "S", fill=(255, 255, 255, 255), font=font_s)

# === TEXTO INFERIOR "BAJADAS" ===
try:
    font_label = ImageFont.truetype("arial.ttf", 16)
except:
    font_label = ImageFont.load_default()

text = "BAJADAS"
bbox = draw.textbbox((0, 0), text, font=font_label)
tw = bbox[2] - bbox[0]
text_x = cx - tw // 2
text_y = cy + 75

# Fondo semi-transparente para el texto
draw.rounded_rectangle(
    [text_x - 10, text_y - 4, text_x + tw + 10, text_y + 20],
    radius=4, fill=(0, 0, 0, 80)
)
draw.text((text_x, text_y - 2), text, fill=(255, 255, 255, 240), font=font_label)

# === GUARDAR ===
out_dir = os.path.dirname(os.path.abspath(__file__))

# PNG 256x256
png_path = os.path.join(out_dir, "icon.png")
img.save(png_path, "PNG")
print(f"PNG guardado: {png_path}")

# ICO multi-resolución
ico_path = os.path.join(out_dir, "icon.ico")
sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
ico_images = [img.resize(s, Image.LANCZOS) for s in sizes]
ico_images[0].save(ico_path, format='ICO', sizes=sizes, append_images=ico_images[1:])
print(f"ICO guardado: {ico_path}")
print("¡Ícono generado exitosamente!")
