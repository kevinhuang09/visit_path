from PIL import Image, ImageDraw, ImageFont
import os

def draw_paths(workers, filename = "path.png", img_size = 600, margin = 60, dot_r = 8):
    all_points = []
    for w in workers:
        all_points.extend(w.path)
    xs = [p[0] for p in all_points]
    ys = [p[1] for p in all_points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    # or with 1 avoid divide by 0
    span_x = max_x - min_x or 1
    span_y = max_y - min_y or 1

    def to_pixel(pt):
        x, y = pt
        px = margin + (x - min_x) / span_x * (img_size - 2 * margin)
        py = margin + (max_y - y) / span_y * (img_size - 2 * margin)
        return (px, py)
    img = Image.new("RGB", (img_size, img_size), "white")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except Exception:
        font = ImageFont.load_default()
    
    colors = ["#e63946", "#1d7874", "#f4a261", "#457b9d"]
    for idx, w in enumerate(workers):
        color = colors[idx % len(colors)]
        pix = [to_pixel(p) for p in w.path]

        if len(pix) >= 2:
            draw.line(pix, fill = color, width = 3)
        
        for order, (px, py) in enumerate(pix):
            draw.ellipse([px - dot_r, py - dot_r,
                          px + dot_r, py + dot_r],
                         fill=color, outline="black")
            
            draw.text((px + dot_r + 2, py - dot_r),
                      str(order), fill="black", font=font)

    dirname = os.path.dirname(filename)
    if dirname:
        os.makedirs(dirname, exist_ok = True)

    # store picture
    img.save(filename)
    print(f"the picture already store with {filename}")