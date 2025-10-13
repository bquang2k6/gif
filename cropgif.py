from PIL import Image, ImageDraw, ImageSequence
import os

def round_corners_gif_folder(input_folder, output_folder="output_gif", radius=30, bg_color=(0,0,0,0)):
    """
    Bo cong góc tất cả file GIF trong một thư mục và lưu vào thư mục output.
    """
    if not os.path.exists(input_folder):
        print(f"❌ Thư mục không tồn tại: {input_folder}")
        return
    os.makedirs(output_folder, exist_ok=True)

    gif_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".gif")]
    if not gif_files:
        print("⚠️ Không tìm thấy file GIF nào trong thư mục.")
        return

    for gif_name in gif_files:
        input_path = os.path.join(input_folder, gif_name)
        output_path = os.path.join(output_folder, f"rounded_{gif_name}")

        im = Image.open(input_path)
        w, h = im.size
        frames = []
        durations = []

        # Tạo mask bo góc
        mask = Image.new("L", (w, h), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), (w, h)], radius=radius, fill=255)

        for frame in ImageSequence.Iterator(im):
            duration = frame.info.get("duration", 100)
            durations.append(duration)
            frame_rgba = frame.convert("RGBA")
            bg = Image.new("RGBA", (w, h), bg_color)
            rounded = Image.composite(frame_rgba, bg, mask)
            frames.append(rounded)

        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            loop=0,
            duration=durations,
            disposal=2
        )
        print(f"✅ Đã bo góc và lưu: {output_path}")

    print("\n🎉 Hoàn tất! Tất cả GIF đã được lưu trong thư mục:", os.path.abspath(output_folder))


if __name__ == "__main__":
    print("=== Bo cong ảnh GIF tự động ===")
    input_folder = input("📁 Nhập đường dẫn thư mục chứa các file GIF: ").strip('"')
    radius_str = input("🔵 Nhập độ bo góc (px, ví dụ 40): ")
    try:
        radius = int(radius_str)
    except ValueError:
        radius = 30
    round_corners_gif_folder(input_folder, radius=radius)
