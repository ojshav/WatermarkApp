import tkinter as tk
from tkinter import filedialog , messagebox , simpledialog
from PIL import Image , ImageDraw , ImageFont , ImageTk

class Watermarkapp:
    def __init__(self,root):
        self.root = root
        self.root.title("Watermark App")
        self.root.geometry("800x600")

        self.label = tk.Label(root,text = "Upload an Image to add a Watermark", font=("Helvetica",14))
        self.label.pack(pady=20)

        self.uploadbutton = tk.Button(root, text="Upload Image",command=self.upload_image)
        self.uploadbutton.pack(pady=10)

        self.text_watermark_button = tk.Button(root,text="Add text Watermark",command=self.add_text_watermark,state=tk.DISABLED)
        self.text_watermark_button.pack(pady=10)

        self.logo_watermark_button = tk.Button(root,text="Add Image Watermark", command=self.add_image_watermark,state=tk.DISABLED)
        self.logo_watermark_button.pack(pady=10)

        self.image_path = None

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.image_path = file_path
            self.text_watermark_button.config(state=tk.NORMAL)
            self.logo_watermark_button.config(state=tk.NORMAL)
            messagebox.showinfo("Image Uplaoded","Image Uploaded Successfully!")
    def add_text_watermark(self):
        if not self.image_path:
            messagebox.showwarning("No Image", "Please upload an image first.")
            return

        watermark_text = simpledialog.askstring("Input", "Enter watermark text:")
        if not watermark_text:
            return

        image = Image.open(self.image_path)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", 36)

        # Use textbbox to get the bounding box of the text
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        width, height = image.size
        x = width - text_width - 10
        y = height - text_height - 10

        draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 128))

        watermarked_image_path = self.image_path.replace(".", "_watermarked.")
        image.save(watermarked_image_path)
        messagebox.showinfo("Watermark Added", f"Watermark added successfully! Saved as {watermarked_image_path}")

    def add_image_watermark(self):
        if not self.image_path:
            messagebox.showwarning("No Image", "Please upload an image first.")
            return
        watermark_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if not watermark_path:
            return
        # Load the image
        image = Image.open(self.image_path).convert("RGBA")
        watermark = Image.open(watermark_path).convert("RGBA")

        # Positioning the watermark at the bottom right corner
        width, height = image.size
        watermark.thumbnail((width // 4, height // 4))
        watermark_width, watermark_height = watermark.size
        x = width - watermark_width - 10
        y = height - watermark_height - 10

        # Create an alpha mask
        alpha_mask = watermark.split()[3]

        # Add the watermark
        image.paste(watermark, (x, y), alpha_mask)

        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if save_path:
            image.save(save_path)
            messagebox.showinfo("Watermark Added", f"Watermark added successfully! Saved as {save_path}")
        
if __name__ == "__main__":
    root = tk.Tk()
    app = Watermarkapp(root)
    root.mainloop()
    
