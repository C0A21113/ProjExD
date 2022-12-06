import tkinter as tk
import maze_maker as mm
import tkinter.messagebox as tkm

def count_up(): #矢印キーを押してから計測開始
    global tmr
    global jid
    label["text"] = tmr
    tmr += 1
    jid = root.after(1000, count_up)

def key_down(event):
    global key
    global jid
    if jid is not None:
        # カウントアップ中にキーが押されたら
        # カウントアップ中でない時は、jid is None
        root.after_cancel(jid)
        jid = None
    else:
        jid = root.after(1000, count_up)
    key = event.keysym

def key_up(event):
    global key
    key = ""

def main_proc():
    global cx, cy, mx, my
    if key == "Up":
        my -= 1
    if key == "Down":
        my += 1
    if key == "Left":
        mx -= 1
    if key == "Right":
        mx += 1
    if maze_list[mx][my] == 1: # 移動先が壁だったら
        if key == "Up":
            my += 1
        if key == "Down":
            my -= 1
        if key == "Left":
            mx += 1
        if key == "Right":
            mx -= 1
    cx, cy = mx*100+50, my*100+50
    canvas.coords("kokaton", cx, cy)
    root.after(100, main_proc)

def button_click():#ボタンを押して
    if maze_list[mx][my] == 1: # 移動先が壁だったら
        tkm.showwarning("警告", "そちらには行けません")#警告表示
    button = tk.Button(root, text="押すな", command=button_click)
    button.pack()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("迷えるこうかとん")
    canvas = tk.Canvas(root, width=1500, height=900, bg="black")
    root = tk.Tk()
    label = tk.Label(root, text="-", font=("", 80))
    label.pack()

    tmr = 0
    jid = None

    maze_list = mm.make_maze(15, 9)
    mm.show_maze(canvas, maze_list)

    mx, my = 1, 1
    cx, cy = mx*100+50, my*100+50
    yakitori = tk.PhotoImage(file="fig/3.png") # 画像の変更
    canvas.create_image(cx, cy, image=yakitori, tag="kokaton")
    canvas.pack()

    key = ""
    root.bind("<KeyPress>", key_down)
    root.bind("<KeyRelease>", key_up)
    main_proc()

    root.mainloop()