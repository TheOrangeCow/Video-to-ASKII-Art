import cv2
import tkinter as tk
from PIL import Image, ImageEnhance, ImageFilter

def enhance(iage):
    iage = iage.filter(ImageFilter.EDGE_ENHANCE)
    iage = ImageEnhance.Contrast(iage).enhance(1.3)
    iage = ImageEnhance.Sharpness(iage).enhance(1.2)
    return iage

def covert(image, width, depth):
    charts = (
        "@$B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft"
        "/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    )
    image = image.convert("L")
    image = enhance(image)

    rat = image.height / image.width
    hight = int(rat * width * 0.55)
    image = image.resize((width, hight), Image.BICUBIC)
    piels = list(image.getdata())

    
    newpiels = []
    for p in piels:
        p = max(0, min(255, p))
        p = 255 * (p / 255) ** depth
        p = 255 - p
        newpiels.append(int(p))

    charslen = len(charts) - 1

    chars = ""

    for p in newpiels:
        index = p * charslen // 255
        char = charts[index]
        chars = chars + char 

    lines = ""

    for i in range(0, len(chars), width):
        line = chars[i:i + width]
        lines = lines + line + "\n"

    return lines.rstrip("\n")



root = tk.Tk()
root.title("Video ASKII")
root.configure(bg="black")

root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda e: root.destroy())

txt = tk.Text(
    root,
    bg="black",
    fg="green",
    insertbackground="black",
    font=("Consolas", 5), # Font size here (4 is the best)
    borderwidth=0,
    highlightthickness=0,
    spacing3=0  
)


txt.pack(fill=tk.BOTH, expand=True)
txt.config(state=tk.DISABLED)

cap = cv2.VideoCapture(r"") # vidow path 


def update():
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap.read()
        if not ret:
            return

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)

    askiitext = covert(img, 300, 1) # change the widh here (500 is best)

    txt.config(state=tk.NORMAL)
    txt.delete("1.0", tk.END)
    txt.insert(tk.END, askiitext)
    txt.config(state=tk.DISABLED)

    root.after(int(1000 / 30), update)

update()
root.mainloop()

cap.release()

