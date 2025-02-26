import cv2
import os
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

def hide_msg(img_pth, msg, pwd, out_f="hidden_msg.png"):
    if not os.path.exists(img_pth):
        messagebox.showerror("Error", "Oops! Image not found.")
        return
    img = cv2.imread(img_pth)
    if img is None:
        messagebox.showerror("Error", "Invalid image file.")
        return
    h, w, _ = img.shape
    msg += "<END>"
    msg_b = np.array(list(msg.encode('utf-8')), dtype=np.uint8)
    if len(msg_b) > h * w * 3:
        messagebox.showerror("Error", "Message too long for this image!")
        return
    flat_img = img.flatten()
    flat_img[:len(msg_b)] = msg_b
    mod_img = flat_img.reshape(img.shape)
    cv2.imwrite(out_f, mod_img, [cv2.IMWRITE_PNG_COMPRESSION, 0])
    messagebox.showinfo("Success", "Message hidden successfully!")
    reset_ui()
def reveal_msg(img_pth, pwd):
    if not os.path.exists(img_pth):
        messagebox.showerror("Error", "Encrypted image not found.")
        return
    img = cv2.imread(img_pth)
    if img is None:
        messagebox.showerror("Error", "Invalid image file.")
        return
    flat_img = img.flatten()
    ext_b = bytearray(flat_img[:5000])
    try:
        dec_msg = ext_b.split(b"<END>")[0].decode('utf-8')
        messagebox.showinfo("Decrypted Message", dec_msg)
    except UnicodeDecodeError:
        messagebox.showerror("Error", "Message corrupted.")
def pick_img():
    f_pth = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if f_pth:
        ent_f_pth.delete(0, tk.END)
        ent_f_pth.insert(0, f_pth)
        show_img(f_pth)
def show_img(f_pth):
    # Image preview
    img = Image.open(f_pth).resize((250, 250), Image.LANCZOS)
    img_ph = ImageTk.PhotoImage(img)
    prev_lbl.config(image=img_ph)
    prev_lbl.photo = img_ph
def reset_ui():
    # Resets the user interface
    ent_f_pth.delete(0, tk.END)
    if 'txt_msg' in globals():
        txt_msg.delete("1.0", tk.END)
    ent_pwd.delete(0, tk.END)
    prev_lbl.config(image=None)
    prev_lbl.photo = None
def enc_action():
    # Perform encryption
    img_pth, sec_txt, usr_pwd = ent_f_pth.get(), txt_msg.get("1.0", tk.END).strip(), ent_pwd.get()
    if img_pth and sec_txt and usr_pwd:
        hide_msg(img_pth, sec_txt, usr_pwd)
    else:
        messagebox.showwarning("Warning", "Fill all fields!")
def dec_action():
    # Perform decryption
    img_pth, usr_pwd = ent_f_pth.get(), ent_pwd.get()
    if img_pth and usr_pwd:
        reveal_msg(img_pth, usr_pwd)
    else:
        messagebox.showwarning("Warning", "Fill both fields!")
def exit_app():
    root.destroy()
def open_ui(mode):
    global root, ent_f_pth, txt_msg, ent_pwd, prev_lbl
    ch_win.destroy()
    root = tk.Tk()
    root.title("Stego Tool")
    root.attributes('-fullscreen', True)
    root.configure(bg="#2E3B4E")
    sty = ttk.Style(root)
    sty.theme_use('clam')
    sty.configure('TLabel', background="#2E3B4E", foreground="white", font=('Segoe UI', 10))
    sty.configure('TButton', font=('Segoe UI', 10), padding=6, relief="flat", background="#5DADE2", foreground="black")
    sty.map('TButton', background=[('active', '#85C1E9')])
    sty.configure('TEntry', font=('Segoe UI', 10))
    sty.configure('TFrame', background="#2E3B4E")
    main_fr = ttk.Frame(root, padding="20")
    main_fr.pack(expand=True, anchor=tk.CENTER)
    f_fr = ttk.Frame(main_fr)
    f_fr.grid(column=0, row=0, sticky=(tk.W, tk.E), pady=10)
    ttk.Label(f_fr, text="Select Image:").grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
    ent_f_pth = ttk.Entry(f_fr, width=40)
    ent_f_pth.grid(column=1, row=0, sticky=(tk.W, tk.E), padx=5, pady=5)
    ttk.Button(f_fr, text="Browse", command=pick_img).grid(column=2, row=0, sticky=tk.W, padx=5, pady=5)
    prev_fr = ttk.Frame(main_fr)
    prev_fr.grid(column=0, row=1, pady=10, sticky=(tk.W, tk.E))
    prev_lbl = ttk.Label(prev_fr)
    prev_lbl.grid(column=0, row=0, sticky=tk.N+tk.S+tk.E+tk.W)
    if mode == "encrypt":
        msg_fr = ttk.Frame(main_fr)
        msg_fr.grid(column=0, row=2, sticky=(tk.W, tk.E), pady=10)
        ttk.Label(msg_fr, text="Secret Message:").grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        txt_msg = tk.Text(msg_fr, height=4, width=50, font=('Segoe UI', 10))
        txt_msg.grid(column=0, row=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        pwd_fr = ttk.Frame(main_fr)
        pwd_fr.grid(column=0, row=3, sticky=(tk.W, tk.E), pady=10)
        ttk.Label(pwd_fr, text="Password:").grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        ent_pwd = ttk.Entry(pwd_fr, show="*", width=30)
        ent_pwd.grid(column=1, row=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Button(main_fr, text="Encrypt", command=enc_action).grid(column=0, row=4, pady=20, sticky=(tk.W, tk.E))
    elif mode == "decrypt":
        pwd_fr = ttk.Frame(main_fr)
        pwd_fr.grid(column=0, row=2, sticky=(tk.W, tk.E), pady=10)
        ttk.Label(pwd_fr, text="Enter Password:").grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        ent_pwd = ttk.Entry(pwd_fr, show="*", width=30)
        ent_pwd.grid(column=1, row=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Button(main_fr, text="Decrypt", command=dec_action).grid(column=0, row=3, pady=20, sticky=(tk.W, tk.E))
    ttk.Button(main_fr, text="Exit", command=exit_app).grid(column=0, row=5, pady=10, sticky=(tk.W, tk.E))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    main_fr.columnconfigure(0, weight=1)
    root.mainloop()
ch_win = tk.Tk()
ch_win.title("Choose Action")
ch_win.geometry("350x220")  
ch_win.configure(bg="#2E3B4E")
sty = ttk.Style(ch_win)
sty.theme_use('clam')
sty.configure('ChFrame.TFrame', background="#2E3B4E")
sty.configure('ChLbl.TLabel', background="#2E3B4E", foreground="white", font=('Segoe UI', 12, 'bold'))
sty.configure('ChBtn.TButton', font=('Segoe UI', 10), padding=8, relief="flat", background="#5DADE2", foreground="black")
sty.map('ChBtn.TButton', background=[('active', '#85C1E9')])
ch_fr = ttk.Frame(ch_win, style='ChFrame.TFrame')
ch_fr.pack(expand=True, anchor=tk.CENTER)
ttk.Label(ch_fr, text="CAPSTONE PROJECT", style='ChLbl.TLabel', font=('Segoe UI', 14, 'bold')).pack(pady=5, anchor=tk.CENTER)
ttk.Label(ch_fr, text="SECURE DATA HIDING IN IMAGES USING STEGANOGRAPHY", style='ChLbl.TLabel', font=('Segoe UI', 10, 'bold')).pack(pady=5, anchor=tk.CENTER)
ttk.Label(ch_fr, text="Choose your action:", style='ChLbl.TLabel').pack(pady=10, anchor=tk.CENTER)
ttk.Button(ch_fr, text="Encrypt", command=lambda: open_ui("encrypt"), style='ChBtn.TButton').pack(pady=5, fill=tk.X, padx=20, anchor=tk.CENTER)
ttk.Button(ch_fr, text="Decrypt", command=lambda: open_ui("decrypt"), style='ChBtn.TButton').pack(pady=5, fill=tk.X, padx=20, anchor=tk.CENTER)
ch_win.mainloop()