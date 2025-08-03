from PIL import Image
from rembg import remove
import numpy as np
import os

def crop_to_square(frame):
    """Cắt khung hình thành tỷ lệ 1:1 (hình vuông) từ trung tâm."""
    width, height = frame.size
    target_size = min(width, height)  # Lấy kích thước nhỏ nhất để tạo hình vuông
    left = (width - target_size) // 2
    top = (height - target_size) // 2
    right = left + target_size
    bottom = top + target_size
    return frame.crop((left, top, right, bottom))

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
    """Xử lý GIF: cắt 1:1, tách nền và lưu kết quả."""
    # Tách khung hình
    frames, duration = extract_frames(input_path)
    
    # Cắt và xóa nền cho từng khung hình
    processed_frames = []
    for frame in frames:
        # Cắt khung hình thành tỷ lệ 1:1
        cropped_frame = crop_to_square(frame)
        # Xóa nền của khung hình đã cắt
        frame_no_bg = remove_background_from_frame(cropped_frame)
        processed_frames.append(frame_no_bg)
    
    # Tạo GIF mới
    create_gif(processed_frames, output_path, duration)
    print(f"Đã lưu GIF với nền trong suốt và tỷ lệ 1:1 tại: {output_path}")

# Sử dụng công cụ
input_gif = "0808.gif"  # Thay bằng đường dẫn tới file GIF của bạn
output_gif = "08088.gif"  # Đường dẫn lưu file GIF đầu ra
remove_gif_background(input_gif, output_gif)