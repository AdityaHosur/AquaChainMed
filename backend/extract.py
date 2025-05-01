from PIL import Image
import numpy as np

def extract_lsb_watermark(watermarked_image_path):
    watermarked_img = Image.open(watermarked_image_path)
    watermarked_pixels = np.array(watermarked_img)

    # Extract LSB from green channel
    green_channel = watermarked_pixels[:, :, 1]
    lsb_bits = green_channel & 1

    # Convert bits to 0/255 image
    extracted_watermark = (lsb_bits * 255).astype(np.uint8)

    # Save extracted watermark
    extracted_img = Image.fromarray(extracted_watermark)
    extracted_img.save("extracted_watermark.png")

    print("Extracted watermark successfully!")

# Example usage:
extract_lsb_watermark("watermarked_image.png")
