import tkinter as tk
import tkinter.messagebox as tkm

def button_click(event):
    btn = event.widget
    txt = btn["text"]
    tkm.showinfo(txt, f"f[{txt}]ボタンが押されました")

root = tk.Tk()
root.title("おためしか")
root.geometry("500x200")

label = tk.Label(root, 
                text="らべるを書いてみた件", 
                font=("", 20)
                )
label.pack()

button = tk.Button(root, text="押すな")
button.bind("<1>", button_click)
button.pack()

entry = tk.Entry(root, width=30)
entry.insert(tk.END, "fugapiyo")
entry.pack()

def button_click():
    tkm.showwarning("警告", "ボタン押したらあかん言うたやろ")
button = tk.Button(root, text="押すな", command=button_click)
button.pack()

root.mainloop()
