import cv2

from tkinter import *
from PIL import Image, ImageTk, ImageOps  # 画像データ用
import sys
import tkinter as tk
from tkinter import filedialog
import glob
import pandas as pd
from pathlib import Path


def ts2sec(tstr):
    h = int(tstr[:-6])
    m = int(tstr[-5:-3])
    s = int(tstr[-2:])
    return h*3600+m*60+s
def sec2ts(sec):
    s = sec%60
    m = int(sec/60)%60
    h = int(sec/3600)
    return "{:02d}{:02d}{:02d}".format(h,m,s)

def sec2ts2(sec):
    s = sec%60
    m = int(sec/60)%60
    h = int(sec/3600)
    return "{:02d}:{:02d}:{:02d}".format(h,m,s)

# 時刻の先頭に 0　を追加するだけ。
def add_recog_0(x):
    return ("0"+x)[-8:]

def read_timestamp(fname):
    df = pd.read_csv(fname, usecols=[0,1,2,3,4])
    df['recog']=df['recog'].map(add_recog_0)
    df['sec']= df['recog'].map(ts2sec)
    return df

def check_timestamp(df):
    ldiff = df['sec'][0]
    error_index = []
    for i,row in df.iterrows():
        diff = row['sec']
        if ldiff +1 != diff and ldiff !=diff:
            print(i,"vid",row['vid_idx'],"frm",row['frm_idx'],lstr,ldiff,row['recog'],diff)
            error_index.append(i)
        lstr = row['recog']
        ldiff = diff

    return error_index

class App(tk.Frame):
    def __init__(self,master = None):
        super().__init__(master)

        self.image_frame = tk.Frame(self.master)
        self.scale_frame = tk.Frame(self.master)
        self.button_frame = tk.Frame(self.master)

        self.canvas = tk.Canvas(self.image_frame, width = 960, height = 540)
#        self.canvas.bind('<Button-1>', self.canvas_click)
        self.canvas.pack(expand = True, fill = tk.BOTH, anchor=tk.CENTER, padx=10)

        self.csv_file = tk.Label(self.button_frame, text = "CSV: Not set")
        self.csv_file.pack(expand = True, padx=10, pady=10)

        self.csv_button = tk.Button(self.button_frame, text="Open CSV", command=self.openCSV, width=40)
        self.csv_button.pack(expand = True, fill = tk.X, padx=10, pady=10)

        self.frame_num = tk.Label(self.button_frame,text="<-Frame:_")
        self.frame_num.pack(expand=True, fill= tk.X, padx = 10, pady = 10)

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

    def openCSV(self):
        path = filedialog.askopenfilename(defaultextension=".csv",filetypes=[("CSV","*.csv")],title="Open csv file")
        print(path)
        self.csv_file["text"]="CSV:"+path
        if len(path)>0:
            df = read_timestamp(path)
            check_timestamp(df)


    def next(self):
        frame = int(self.num.get())
#        cap.
#        print("pushed next for ",frame)
        if app.frame != frame:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES,frame)
            app.frame = frame

        # 現在のフレーム番号
        rframe = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        self.frame_num["text"] = "<----  Frame: "+str(rframe)+", try to set: "+str(frame)

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
#        print("Show image",tf)        

    
if __name__ == "__main__":
    root = tk.Tk()
    app = App(master=root)
    app.cap = cv2.VideoCapture(sys.argv[1])
    app.frame =0
    print(app.cap, sys.argv[1])
    app.mainloop()

