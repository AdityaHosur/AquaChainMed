from PIL import Image
import numpy as np

def verify_watermark(downloaded_path, extracted_path):
    downloaded_img = Image.open(downloaded_path).convert('L')
    extracted_img = Image.open(extracted_path).convert('L')

    downloaded_arr = np.array(downloaded_img)
    extracted_arr = np.array(extracted_img)

    # XOR comparison
    difference = np.bitwise_xor(downloaded_arr, extracted_arr)

    if np.any(difference):
        print("Warning: Watermark integrity check FAILED. Possible tampering detected.")
    else:
        print("Watermark integrity verified. No tampering detected!")

# Example usage:
verify_watermark("downloaded_actual_watermark.png", "extracted_watermark.png")
