import os
import cv2
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim, peak_signal_noise_ratio as psnr
import matplotlib.pyplot as plt
import pandas as pd

# Paths
original_path = "original_images/Flower.jpg"
compressed_folder = "compressed_images"

# Ensure folders exist
if not os.path.exists(original_path):
    raise FileNotFoundError(f" Original image not found at: {original_path}")

os.makedirs(compressed_folder, exist_ok=True)

# JPEG quality levels to test
qualities = [90, 70, 50, 30, 10]

# Read original image
original = cv2.imread(original_path)
original = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)

ssim_values = []
psnr_values = []
file_sizes = []

print("\n Starting JPEG compression quality comparison...\n")

try:
    # Compress image at each quality and evaluate
    for q in qualities:
        compressed_path = os.path.join(compressed_folder, f"flower_q{q}.jpg")

        # Compress using Pillow
        Image.fromarray(original).save(compressed_path, "JPEG", quality=q)

        # Read compressed image
        comp = cv2.imread(compressed_path)
        comp = cv2.cvtColor(comp, cv2.COLOR_BGR2RGB)

        # Compute metrics
        s = ssim(original, comp, channel_axis=2)
        p = psnr(original, comp)
        size_kb = os.path.getsize(compressed_path) / 1024

        ssim_values.append(s)
        psnr_values.append(p)
        file_sizes.append(size_kb)

        print(f" Quality {q}: SSIM={s:.4f}, PSNR={p:.2f} dB, Size={size_kb:.2f} KB")

    # Plot results
    plt.figure(figsize=(8, 5))
    plt.plot(qualities, ssim_values, marker='o', label='SSIM')
    plt.plot(qualities, psnr_values, marker='s', label='PSNR (dB)')
    plt.plot(qualities, file_sizes, marker='^', label='File Size (KB)')
    plt.xlabel("JPEG Quality Level")
    plt.ylabel("Value")
    plt.title("JPEG Compression Quality Comparison")
    plt.gca().invert_xaxis()
    plt.legend()
    plt.grid(True)

    # Save and show graph
    plt.savefig("compression_graph.png")
    print("\n Graph saved successfully as: compression_graph.png")
    plt.show()

    # Save all results to CSV
    df = pd.DataFrame({
        "Quality": qualities,
        "SSIM": ssim_values,
        "PSNR (dB)": psnr_values,
        "File Size (KB)": file_sizes
    })
    df.to_csv("results.csv", index=False)
    print(" Results saved to results.csv\n")

    print(" Process completed successfully!")

except Exception as e:
    print(f"\n Error occurred: {e}")
