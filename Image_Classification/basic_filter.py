from PIL import Image, ImageFilter
import matplotlib.pyplot as plt
import os

def apply_blur_filter(image_path, output_path="blurred_image.png"):
    try:
        img = Image.open(image_path)
        img_blurred = img.filter(ImageFilter.GaussianBlur(radius=2))

        # Save full-resolution image
        img_blurred.save(output_path)

        print(f"Processed image saved as '{output_path}'.")
    except Exception as e:
        print(f"Error processing image: {e}")


def apply_vaporwave_filter(image_path, output_path="vaporwave_image.png"):
    try:
        img = Image.open(image_path).convert("RGB")
        img_resized = img  # keep original resolution

        # --- 1. Strong neon color shift ---
        r, g, b = img_resized.split()

        r = r.point(lambda i: min(255, i + 80))  # boost red
        b = b.point(lambda i: min(255, i + 80))  # boost blue
        g = g.point(lambda i: max(0, i - 40))    # reduce green

        neon_shift = Image.merge("RGB", (r, g, b))

        # --- 2. High saturation (fast, stable) ---
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Color(neon_shift)
        saturated = enhancer.enhance(2.5)

        # --- 3. Strong contrast curve ---
        def contrast_curve(i):
            return int((i / 255) ** 0.7 * 255)
        final = saturated.point(contrast_curve)

        # --- 4. Save full-resolution image ---
        final.save(output_path)

        print(f"Vaporwave image saved as '{output_path}'.")
    except Exception as e:
        print(f"Error processing image: {e}")




if __name__ == "__main__":
    print("Image Filter Processor (type 'exit' to quit)\n")
    while True:
        image_path = input("Enter image filename (or 'exit' to quit): ").strip()

        if image_path.lower() == 'exit':
            print("Goodbye!")
            break

        # Vaporwave command
        if image_path.lower() == "vaporwave":
            target = input("Enter image filename for Vaporwave Filter: ").strip()
            if not os.path.isfile(target):
                print(f"File not found: {target}")
                continue
            base, ext = os.path.splitext(target)
            output_file = f"{base}_vaporwave{ext}"
            apply_vaporwave_filter(target, output_file)
            continue

        # Normal blur filter
        if not os.path.isfile(image_path):
            print(f"File not found: {image_path}")
            continue

        base, ext = os.path.splitext(image_path)
        output_file = f"{base}_blurred{ext}"
        apply_blur_filter(image_path, output_file)