from PIL import Image
from rembg import remove
import numpy as np
import io
import os

def extract_frames(gif_path):
    """Tách các khung hình từ file GIF."""
    gif = Image.open(gif_path)
    frames = []
    try:
        while True:
            frame = gif.copy()
            frames.append(frame.convert("RGBA"))
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass
    return frames, gif.info.get('duration', 100)

def remove_background_from_frame(frame):
    """Xóa nền của một khung hình."""
    img_array = np.array(frame)
    img_no_bg = remove(img_array)
    return Image.fromarray(img_no_bg)

def create_gif(frames, output_path, duration):
    """Tạo GIF từ danh sách các khung hình."""
    if frames:
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=0,
            transparency=0,
            disposal=2
        )

def remove_gif_background(input_path, output_path):
    """Xử lý GIF: tách nền và lưu kết quả."""
    # Tách khung hình
    frames, duration = extract_frames(input_path)
    
    # Xóa nền cho từng khung hình
    processed_frames = []
    for frame in frames:
        frame_no_bg = remove_background_from_frame(frame)
        processed_frames.append(frame_no_bg)
    
    # Tạo GIF mới
    create_gif(processed_frames, output_path, duration)
    print(f"Đã lưu GIF với nền trong suốt tại: {output_path}")

# Sử dụng công cụ
input_gif = "uia.gif"  # Thay bằng đường dẫn tới file GIF của bạn
output_gif = "output_no_bg.gif"  # Đường dẫn lưu file GIF đầu ra
remove_gif_background(input_gif, output_gif)