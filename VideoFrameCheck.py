import cv2

from tkinter import *
from PIL import Image, ImageTk, ImageOps  # 画像データ用
import sys
import tkinter as tk

class App(tk.Frame):
    def __init__(self,master = None):
        super().__init__(master)

        self.image_frame = tk.Frame(self.master)
        self.scale_frame = tk.Frame(self.master)
        self.button_frame = tk.Frame(self.master)

        self.canvas = tk.Canvas(self.image_frame, width = 960, height = 540)
#        self.canvas.bind('<Button-1>', self.canvas_click)
        self.canvas.pack(expand = True, fill = tk.BOTH, anchor=tk.CENTER, padx=10)

        self.num = tk.Entry(self.button_frame,width=10)
        self.num.insert(tk.END,"0")  
        self.num.pack(padx=10,pady=10)
#        self.num.place(x=820, y=70)
        self.go_button = tk.Button(self.button_frame, text="Next", command=self.next, width=40)
        self.go_button.pack(expand = True, fill = tk.X, padx=10, pady=10)

        self.image_frame.grid(column=0, rowspan=2)
        self.button_frame.grid(column=1, row=1)

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

#        if self.disp_id is None:
  #          self.disp_image()
#        else:
 #           self.disp_id = None

    def next(self):
        frame = int(self.num.get())
#        cap.
#        print("pushed next for ",frame)
        if app.frame != frame:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES,frame)
            app.frame = frame
        tf, img = self.cap.read()
        # 画像を半分のサイズにしたい
        app.frame += 1
        if not tf:
#            print("Capture failed for",self.cap)
            return
        dst = cv2.resize(img,dsize=(960,540))
        
        cv_image = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
        
        self.num.delete(0,tk.END)  

        self.num.insert(tk.END,str(frame+1))  
        self.pil_image = Image.fromarray(cv_image)
        #pimg = tk.PhotoImage(image=pil_image)
        self.pimg  = ImageTk.PhotoImage(image=self.pil_image)
        self.canvas.delete("all")
        self.canvas.create_image(
                480,       # 画像表示位置(Canvasの中心)
                270,                   
                image=self.pimg  # 表示画像データ
                )
        print("Show image",tf)        

    
if __name__ == "__main__":
    root = tk.Tk()
    app = App(master=root)
    app.cap = cv2.VideoCapture(sys.argv[1])
    app.frame =0
    print(app.cap, sys.argv[1])
    app.mainloop()

