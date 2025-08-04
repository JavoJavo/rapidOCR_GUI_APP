import tkinter as tk
from PIL import Image, ImageTk, ImageGrab
import tempfile
import os
from rapidocr import RapidOCR

engine = RapidOCR()

def ocr_it(img_path):
    result = engine(img_path)
    return '\n'.join([sentence for sentence in result.txts])

def paste_image():
    try:
        img = ImageGrab.grabclipboard()
        if img:
            temp_path = os.path.join(tempfile.gettempdir(), "pasted_temp.png")
            img.convert("RGB").save(temp_path)
            
            img = Image.open(temp_path)
            img.thumbnail((800, 600), Image.LANCZOS)  # Scales down proportionally
            tk_img = ImageTk.PhotoImage(img)
            label.config(image=tk_img)
            label.image = tk_img
            root.temp_path = temp_path
            
            # OCR and display results
            text = ocr_it(temp_path)
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, text)
    except Exception as e:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Error: {e}")

def copy_to_clipboard():
    text = result_text.get(1.0, tk.END)
    if text.strip():
        root.clipboard_clear()
        root.clipboard_append(text)

def on_close():
    if hasattr(root, 'temp_path') and os.path.exists(root.temp_path):
        os.remove(root.temp_path)
    root.destroy()

root = tk.Tk()
root.title("Image Paster + OCR")
root.geometry("900x700")

# Image display
label = tk.Label(root)
label.pack(pady=10)

# OCR results
result_text = tk.Text(root, height=10, wrap=tk.WORD)
result_text.pack(fill=tk.X, padx=10, pady=5)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="PASTE (Ctrl+V)", command=paste_image, 
         font=("Arial", 12), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)

tk.Button(button_frame, text="COPY TEXT", command=copy_to_clipboard,
         font=("Arial", 12), bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=5)

root.bind('<Control-v>', lambda e: paste_image())
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()