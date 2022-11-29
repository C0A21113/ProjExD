import tkinter as tk
import tkinter.messagebox as tkm
import math

def button_click(event):
    btn = event.widget
    num = btn["text"]
    if num == "=":
        siki = entry.get()
        res = eval(siki)
        entry.delete(0, tk.END)
        entry.insert(tk.END, res)
    #else:
    #tkm.showinfo("", f"{num}ボタンがクリックされました")
     #   entry.insert(tk.END, num)

    elif num == "AC":
        entry.delete(0, tk.END)
    else:
        entry.insert(tk.END, num)

root = tk.Tk()
root.geometry("300x500")

entry = tk.Entry(root, justify="right", width=10, font=("", 40), bg="black", fg="white") #Entryクラスの色の変更
entry.grid(row=0, column=0, columnspan=3)
entry.delete(tk.END, 0)

r, c = 1, 0
for num in range(9, -1, -1):
    button = tk.Button(root, text=f"{num}", width=4, height=1, font=("", 30), bg="black", fg="white") #ボタンの色の偏向
    button.grid(row=r, column=c)
    button.bind("<1>", button_click)
    c += 1
    if c%3 == 0:
        r += 1
        c = 0

operators = ["+", "=", "-", "*", "/"] #四則演算の追加
for ope in operators:
    button = tk.Button(root, text=f"{ope}", width=4, height=1, font=("", 30), bg="black", fg="white") #ボタンの色の変更
    button.grid(row=r, column=c)
    button.bind("<1>", button_click)
    c += 1
    if c%3 == 0:
        r += 1
        c = 0

ope = ["AC", "√", "."] #削除,ルート,小数点の追加
for op in ope:
    button = tk.Button(root, text=f"{op}", width=4, height=1, font=("", 30), bg="black", fg="white") #ボタンの色の変更
    button.grid(row=r, column=c)
    button.bind("<1>", button_click)
    c += 1
    if c%3 == 0:
        r += 1
        c = 0

root.mainloop()
