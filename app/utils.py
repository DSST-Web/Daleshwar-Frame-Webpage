# app/utils.py

from PIL import Image
from io import BytesIO
import uuid
import os

def process_image(user_image_file, frame_path, x=0, y=0, scale=1.0, canvas_width=None, canvas_height=None):
    from PIL import Image
    from io import BytesIO
    import uuid
    import os

    # 🖼 Load frame to get its dimensions first
    frame_img = Image.open(frame_path).convert("RGBA")
    frame_width, frame_height = frame_img.size

    # 🚫 If canvas size not provided, use frame size
    if canvas_width is None or canvas_height is None:
        canvas_width, canvas_height = frame_width, frame_height

    # Resize frame to canvas (in case specified explicitly)
    frame_img = frame_img.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)

    # Load and resize user image
    user_img = Image.open(user_image_file).convert("RGBA")
    user_width, user_height = user_img.size
    new_width = int(user_width * scale)
    new_height = int(user_height * scale)
    user_img = user_img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Create transparent background canvas
    background = Image.new("RGBA", (canvas_width, canvas_height), (0, 0, 0, 0))
    background.paste(user_img, (x, y), user_img)

    # Composite
    combined = Image.alpha_composite(background, frame_img)

    # Save output
    img_bytes = BytesIO()
    combined.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    filename = f"{uuid.uuid4().hex}_framed.png"
    output_path = os.path.join("static", filename)
    with open(output_path, "wb") as f:
        f.write(img_bytes.read())

    return filename