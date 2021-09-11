import sys
import pyautogui as pag
import tkinter as tk
import pyperclip as ppc
import time
import ctypes

# Soybeanmanのパソコンに合わせた座標なのでそのままでは多分ヤバいことになる
posi = {
    'firstImage': (1060, 500),  # 最初の画像クリック位置
    'expandedImage': (1280, 800),  # 画像の位置
    'rightClickSave': (10, 50),  # 右クリックメニュー
    'nextImage': (1280, 1200)  # 次の画像
}
fileName = 'test'
clip = ppc.paste()


def process1():
    frm = tk.Tk()
    frm.geometry('300x220')
    frm.title('手順1')

    static1 = tk.Label(frm, text='まず、保存名と画像枚数を決めて、\nOKを押す。')
    static1.pack()

    entryFile = tk.Entry(frm)
    entryFile.insert(tk.END, fileName)
    entryFile.pack()

    entryImageMax = tk.Entry(frm)
    entryImageMax.pack()

    def buttonCommand():
        global fileName
        global imageMax
        fileName = entryFile.get()
        imageMax = int(entryImageMax.get())
        if fileName != '' and imageMax != 0:
            frm.destroy()

    button1 = tk.Button(frm, text='OK', command=buttonCommand)
    button1.pack()

    button2 = tk.Button(frm, text='Close', command=sys.exit)
    button2.pack()

    frm.mainloop()


def process2():
    frm = tk.Tk()
    frm.geometry('300x180')
    frm.title('手順2')

    static1 = tk.Label(frm, text='次に、すべて見るを選択して、\nそのままスクロールせずにOKを押す。')
    static1.pack()

    button1 = tk.Button(frm, text='OK', command=frm.destroy)
    button1.pack()

    button2 = tk.Button(frm, text='Close', command=sys.exit)
    button2.pack()

    frm.mainloop()

    pag.moveTo(*posi['firstImage'])
    pag.click()
    time.sleep(0.05)

    pag.moveTo(*posi['expandedImage'])
    pag.click(button='right')
    time.sleep(0.05)

    pag.move(*posi['rightClickSave'])
    pag.click()
    time.sleep(1)

    ppc.copy(fileName + '_1')
    pag.hotkey('ctrl', 'v')


def process3():
    frm = tk.Tk()
    frm.geometry('300x180')
    frm.title('手順3')

    static1 = tk.Label(
        frm, text='最後に、セーブするファイルを作成して、\n保存してから、OKを押す。')
    static1.pack()

    button1 = tk.Button(frm, text='OK', command=frm.destroy)
    button1.pack()

    button2 = tk.Button(frm, text='Close', command=sys.exit)
    button2.pack()

    frm.mainloop()

    pag.moveTo(*posi['expandedImage'])
    pag.click(button='right')
    time.sleep(0.05)

    for imageNumber in range(2, imageMax + 1):
        pag.moveTo(*posi['nextImage'])
        pag.click()
        time.sleep(0.05)

        pag.moveTo(*posi['expandedImage'])
        pag.click(button='right')
        time.sleep(0.05)

        pag.move(*posi['rightClickSave'])
        pag.click()
        time.sleep(1)

        ppc.copy(fileName + '_' + str(imageNumber))
        pag.hotkey('ctrl', 'v')
        pag.hotkey('enter')
        time.sleep(0.05)


frm = tk.Tk()
frm.geometry('400x180')

frm.title('注意')

static1 = tk.Label(frm, text='Soybeanmanのパソコンに合わせた座標なので、\nソースコード内の座標を変更しないとヤバいことになります。\n終了するにはCloseを押してください。')
static1.pack()

button1 = tk.Button(frm, text='OK', command=frm.destroy)
button1.pack()

button2 = tk.Button(frm, text='Close', command=sys.exit)
button2.pack()

frm.mainloop()
process1()
process2()
process3()

ppc.copy(clip)
