import cv2
import numpy as np
from sklearn.cluster import KMeans

def generate_actual_watermark(watermark_path, host_image_shape, num_clusters=8):
    watermark = cv2.imread(watermark_path)
    pixel_data = watermark.reshape((-1, 3))

    kmeans = KMeans(n_clusters=num_clusters, random_state=0)
    kmeans.fit(pixel_data)
    centroids = kmeans.cluster_centers_.astype(np.uint8)
    labels = kmeans.labels_

    clustered_pixels = centroids[labels]
    clustered_image = clustered_pixels.reshape(watermark.shape)

    # Convert cluster centers to binary
    binary_str = ''.join([format(val, '08b') for center in centroids for val in center])
    binary_array = np.array([int(b) for b in binary_str], dtype=np.uint8)

    total_pixels = host_image_shape[0] * host_image_shape[1]
    repeated_bits = np.tile(binary_array, total_pixels // len(binary_array) + 1)[:total_pixels]
    actual_watermark = repeated_bits.reshape(host_image_shape)

    return actual_watermark, clustered_image


def resize_watermark_to_fit(actual_watermark, host_shape):
    max_bits = host_shape[0] * host_shape[1]
    flat_watermark = actual_watermark.flatten()

    if len(flat_watermark) > max_bits:
        scale_factor = (max_bits / len(flat_watermark))**0.5
        new_size = (int(actual_watermark.shape[1] * scale_factor),
                    int(actual_watermark.shape[0] * scale_factor))
        resized = cv2.resize(actual_watermark.astype(np.uint8), new_size, interpolation=cv2.INTER_AREA)

        padded = np.zeros(host_shape, dtype=np.uint8)
        padded[:resized.shape[0], :resized.shape[1]] = resized
        return padded
    else:
        return actual_watermark


def embed_watermark_lsb(host_image_path, actual_watermark):
    host_image = cv2.imread(host_image_path)
    green_channel = host_image[:, :, 1]
    flat_green = green_channel.flatten()
    flat_watermark = actual_watermark.flatten()

    # Resize watermark if needed
    if len(flat_watermark) > len(flat_green):
        print("[INFO] Watermark too large, resizing...")
        actual_watermark = resize_watermark_to_fit(actual_watermark, green_channel.shape)
        flat_watermark = actual_watermark.flatten()

    # Embed using LSB
    for i in range(len(flat_watermark)):
        flat_green[i] = np.uint8((int(flat_green[i]) & ~1) | int(flat_watermark[i]))

    new_green = flat_green.reshape(green_channel.shape)
    watermarked_image = host_image.copy()
    watermarked_image[:, :, 1] = new_green

    return watermarked_image

host_image = cv2.imread(r"D:\coding\AquaChainMed\img\chestxray.png")
host_shape = host_image.shape[:2]

actual_watermark, clustered = generate_actual_watermark(r"D:\coding\AquaChainMed\img\watermark.png", host_shape)
watermarked_image = embed_watermark_lsb(r"D:\coding\AquaChainMed\img\chestxray.png", actual_watermark)

cv2.imwrite("watermarked_image.png", watermarked_image)
cv2.imwrite("actual_watermark.png", actual_watermark * 255)
