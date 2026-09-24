import os
import math
from PIL import Image, ImageDraw, ImageFont

STATIC_IMAGES = os.path.join(os.path.dirname(__file__), "static", "images")
os.makedirs(STATIC_IMAGES, exist_ok=True)

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def interpolate_color(c1, c2, factor):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * factor) for i in range(len(c1)))

def draw_rounded_rect(draw, bbox, radius, fill=None, outline=None, width=1):
    x0, y0, x1, y1 = bbox
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)

def render_apple_g_mark_image(size=512, background="#0B0F17", transparent_bg=False):
    """
    Renderiza la 'G.' verde estilo Apple en alta resolución con Pillow
    con antialiasing por supermuestreo (supersampling 2x).
    """
    scale = 2
    canvas_size = size * scale
    img = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    margin = int(canvas_size * 0.05)
    corner_r = int(canvas_size * 0.22)

    # Fondo redondeado estilo Squircle Apple
    if not transparent_bg:
        bg_rgb = hex_to_rgb(background)
        draw_rounded_rect(draw, (margin, margin, canvas_size - margin, canvas_size - margin), corner_r, fill=(*bg_rgb, 255))
        draw_rounded_rect(draw, (margin, margin, canvas_size - margin, canvas_size - margin), corner_r, outline=(255, 255, 255, 22), width=scale*2)

    # Curvas de la 'G' verde estilo Apple
    c_green = hex_to_rgb("#10B981")
    c_mint = hex_to_rgb("#34D399")

    # Dimensiones y centro
    cx, cy = int(canvas_size * 0.46), int(canvas_size * 0.50)
    sw = int(canvas_size * 0.09) # grosor del trazo
    r_outer = int(canvas_size * 0.26)

    # Arco exterior de la G (de 45 a 315 grados aproximadamente)
    bbox_arc = [cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer]
    draw.arc(bbox_arc, start=45, end=315, fill=(*c_green, 255), width=sw)

    # Trazo horizontal que entra al centro de la G
    mid_y = cy
    draw.line([cx, mid_y, cx + int(r_outer * 0.88), mid_y], fill=(*c_mint, 255), width=sw)
    # Poste vertical derecho que sube hasta la mitad
    draw.line([cx + int(r_outer * 0.88), mid_y, cx + int(r_outer * 0.88), cy + int(r_outer * 0.70)], fill=(*c_green, 255), width=sw)

    # Punto terminal característico de la "G." (Apple Minimal Dot)
    dot_r = int(canvas_size * 0.045)
    dot_cx = int(canvas_size * 0.76)
    dot_cy = int(canvas_size * 0.73)
    draw.ellipse([dot_cx - dot_r, dot_cy - dot_r, dot_cx + dot_r, dot_cy + dot_r], fill=(*c_mint, 255))

    return img.resize((size, size), Image.Resampling.LANCZOS)


def generate_all_icons():
    print("-> Generando Favicon e Iconos Apple Style (G. verde)...")
    
    icon_512 = render_apple_g_mark_image(512, background="#0B0F17")
    icon_512.save(os.path.join(STATIC_IMAGES, "icon-512.png"), "PNG", optimize=True)

    icon_192 = render_apple_g_mark_image(192, background="#0B0F17")
    icon_192.save(os.path.join(STATIC_IMAGES, "icon-192.png"), "PNG", optimize=True)

    apple_icon = render_apple_g_mark_image(180, background="#0B0F17")
    apple_icon.save(os.path.join(STATIC_IMAGES, "apple-touch-icon.png"), "PNG", optimize=True)

    fav_32 = render_apple_g_mark_image(32, background="#0B0F17")
    fav_32.save(os.path.join(STATIC_IMAGES, "favicon-32x32.png"), "PNG", optimize=True)

    fav_16 = render_apple_g_mark_image(16, background="#0B0F17")
    fav_16.save(os.path.join(STATIC_IMAGES, "favicon-16x16.png"), "PNG", optimize=True)

    # Multi-resolution favicon.ico
    fav_32.save(
        os.path.join(STATIC_IMAGES, "favicon.ico"),
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48)]
    )

    icon_trans = render_apple_g_mark_image(512, transparent_bg=True)
    icon_trans.save(os.path.join(STATIC_IMAGES, "logo-mark-transparent.png"), "PNG", optimize=True)

    print("✓ Iconos generados con éxito.")

def generate_og_image():
    """
    Genera la imagen OpenGraph de 1200x630px para Twitter/LinkedIn/WhatsApp
    con diseño minimalista estilo Apple (G. verde).
    """
    print("-> Generando OpenGraph Banner (1200x630) Apple Style...")
    width, height = 1200, 630
    img = Image.new("RGBA", (width, height), (11, 15, 23, 255)) # Slate Oscuro Mate
    draw = ImageDraw.Draw(img)

    # Resplandor radial verde esmeralda sutil en esquina superior derecha
    glow_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_img)
    glow_draw.ellipse([800, -80, 1300, 420], fill=(16, 185, 129, 25))
    img = Image.alpha_composite(img, glow_img)
    draw = ImageDraw.Draw(img)

    # Insertar Isotipo G. Verde
    mark = render_apple_g_mark_image(140, background="#182234")
    img.paste(mark, (90, 80), mark)

    # Tipografías del sistema macOS (SF Pro / Helvetica / Arial)
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 52)
        font_tagline = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 26)
        font_badge = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 15)
        font_pill = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 18)
    except:
        font_large = ImageFont.load_default()
        font_tagline = font_large
        font_badge = font_large
        font_pill = font_large

    # Badge Minimalista Verde Esmeralda
    draw_rounded_rect(draw, (90, 260, 470, 296), 18, fill=(16, 185, 129, 30), outline=(16, 185, 129, 100), width=1)
    draw.ellipse([106, 274, 114, 282], fill=(52, 211, 153, 255))
    draw.text((126, 271), "ESTUDIO & CONSULTORÍA DE SOFTWARE", font=font_badge, fill=(52, 211, 153, 255))

    # Título Principal Estilo Apple (GG Solutions)
    draw.text((90, 320), "GG Solutions", font=font_large, fill=(255, 255, 255, 255))
    
    # Subtítulo
    draw.text((90, 395), "Software pensado para resolver problemas reales.", font=font_tagline, fill=(241, 245, 249, 255))
    draw.text((90, 435), "Sistemas Internos • Dashboards • Arquitectura de Alto Rendimiento", font=font_tagline, fill=(148, 163, 184, 255))

    # Franja inferior
    draw.line([(90, 520), (1110, 520)], fill=(255, 255, 255, 20))
    draw.text((90, 545), "Córdoba, Argentina  •  ggsolutions.com.ar", font=font_pill, fill=(148, 163, 184, 255))
    draw.text((820, 545), "Menos ruido. Más solución.", font=font_pill, fill=(52, 211, 153, 255))

    img.save(os.path.join(STATIC_IMAGES, "og-image.png"), "PNG", optimize=True)
    print("✓ og-image.png generado con éxito.")

if __name__ == "__main__":
    generate_all_icons()
    generate_og_image()
