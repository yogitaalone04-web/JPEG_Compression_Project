from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd

# Load the results CSV (it must exist in the same folder)
data = pd.read_csv("results.csv")

# Create a new PDF file
pdf = canvas.Canvas("compression_report.pdf", pagesize=letter)
pdf.setTitle("JPEG Compression Quality Report")

# Title
pdf.setFont("Helvetica-Bold", 18)
pdf.drawString(150, 750, "JPEG Compression Quality Report")

# Table header
pdf.setFont("Helvetica-Bold", 12)
pdf.drawString(50, 700, "Quality")
pdf.drawString(150, 700, "SSIM")
pdf.drawString(250, 700, "PSNR (dB)")
pdf.drawString(350, 700, "File Size (KB)")

# Table rows
pdf.setFont("Helvetica", 12)
y = 680
for _, row in data.iterrows():
    pdf.drawString(50, y, str(row["Quality"]))
    pdf.drawString(150, y, f"{row['SSIM']:.4f}")
    pdf.drawString(250, y, f"{row['PSNR (dB)']:.2f}")
    pdf.drawString(350, y, f"{row['File Size (KB)']:.2f}")
    y -= 20

# Add graph image
pdf.drawImage("compression_graph.png", 100, 350, width=400, height=250)

# Footer
pdf.setFont("Helvetica-Oblique", 10)
pdf.drawString(180, 50, "Generated automatically using Python ")

# Save the PDF
pdf.save()
print(" PDF report created: compression_report.pdf")
