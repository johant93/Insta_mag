import sys
import multiprocessing as mp
import threading
import time
from PIL import ImageTk
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import *
import os


import app as app



class GUI:

    flag = True

    def __init__(self, master):

        frame = Frame(master)
        frame.pack(fill=X, pady=5)

        photo = PhotoImage(file="icon_insta_mag.ico")
        self.labelico = ttk.Label(frame,image=photo)
        self.labelico.photo = photo
        self.labelico.pack()

        frame1 = Frame(master)
        frame1.pack(fill=X, pady=5)

        self.label1 = ttk.Label(frame1, text='Destination folder:')
        self.label1.pack(side=LEFT, padx=5, pady=5)

        self.dst_path_entry = ttk.Entry(frame1, width=17)  # number of characters along the width
        self.dst_path_entry.pack(padx=5, side=tk.LEFT)

        self.btnBrowse = ttk.Button(frame1, text="browse")
        self.btnBrowse.pack(padx=5, side=tk.LEFT)
        self.btnBrowse.bind('<Button-1>', self.btnBrowsefunc)

        frame2 = Frame(master)
        frame2.pack(fill=X,pady=5)

        self.label2 = ttk.Label(frame2, text='Hashtag:#')
        self.label2.pack(side=LEFT, padx=5, pady=5)

        self.htag_entry = ttk.Entry(frame2, width=15)  # number of characters along the width
        self.htag_entry.pack(fill=X, padx=5, expand=True)

        frame3 = Frame(master)
        frame3.pack(fill=X,pady=5)

        self.lab_limit = ttk.Label(frame3, text='download limited to:')
        self.lab_limit.pack(side=LEFT, padx=5, pady=5)

        self.limit_entry = ttk.Entry(frame3, width=5)  # number of characters along the width
        self.limit_entry.pack(side=LEFT, padx=5)

        self.lab_pic = ttk.Label(frame3, text='picture(s)')
        self.lab_pic.pack(side=LEFT, padx=5, pady=5)

        frame4 = Frame(master)
        frame4.pack(fill=X,pady=5)

        self.lab_maxPic = ttk.Label(frame4, text='Picture by user limited to:')
        self.lab_maxPic.pack(side=LEFT, padx=5, pady=5)

        self.maxPic_byUser_entry = ttk.Entry(frame4, width=5)  # number of characters along the width
        self.maxPic_byUser_entry.pack(side=LEFT, padx=5)

        self.lab_pic = ttk.Label(frame4, text='picture(s)')
        self.lab_pic.pack(side=LEFT, padx=5, pady=5)


        frame5 = Frame(master)
        frame5.pack(pady=20)

        self.btnRun = ttk.Button(frame5, text="Start")
        self.btnRun.pack()
        self.btnRun.bind('<Button-1>', self.run)
     #   self.btnRun.config(command=se lf.run)

    #total download picture labels
        self.lab_tdpic = ttk.Label(frame5, text='Total downloaded pictures:')
        self.lab_tnum = ttk.Label(frame5, text='0')

        self.progress = ttk.Progressbar(frame5, orient=HORIZONTAL, length=50, mode='determinate')

        frame6 = Frame(master)
        frame6.pack(pady=20, side=TOP)

        self.btn_stop = ttk.Button(frame6, text='Stop')
        self.btn_stop.pack(padx=10, side=tk.LEFT)
        self.btn_stop.bind('<Button-1>', self.btnStop_func)

        self.btnClear = ttk.Button(frame6, text='Clear', command=self.btnClearfunc)
        self.btnClear.pack(padx=10, side=tk.LEFT)

        self.btn_quit = ttk.Button(frame6, text='Quit')
        self.btn_quit.pack(padx=10, side=tk.LEFT)
        self.btn_quit.bind('<Button-1>', self.btnQuit_func)


    def btnStop_func(self,event):
        app.InstagramScraper.stop = True
        self.progress.stop()
        self.progress.pack_forget()
        self.btnRun['state'] = 'normal'
        self.lab_tnum['text'] = str(app.InstagramScraper.total_pic_downl)
        GUI.flag = False

    def btnQuit_func(self,event):
        sys.exit(0)

    def btnClearfunc(self):

        self.lab_tdpic.pack_forget()
        self.lab_tnum.pack_forget()
        self.htag_entry.delete(0, tk.END)  # delete all from 0 to END character in Entry Widget
        self.limit_entry.delete(0, tk.END)  # delete all from 0 to END character in Entry Widget
        self.dst_path_entry.delete(0, tk.END)
        self.maxPic_byUser_entry.delete(0, tk.END)
        app.InstagramScraper.total_pic_downl = 0


    def btnBrowsefunc(self,event):
        current_directory = filedialog.askdirectory()
        self.dst_path_entry.delete(0, END)
        self.dst_path_entry.insert(0, current_directory)

    def traitement(self):
        def real_traitement():
            self.lab_tdpic.pack(side=tk.LEFT,pady=5)
            self.lab_tnum.pack(side=tk.LEFT,pady=5)
            self.progress.pack(side=tk.LEFT,pady=5, padx = 5)

            self.progress.start()


        self.btnRun['state'] = 'disabled'
        t2 = threading.Thread(target=real_traitement)
        t2.daemon = True
        t2.start()

    def update_total_downl(self):
        def update_():
            while(not app.InstagramScraper.stop):
                self.lab_tnum['text'] = str(app.InstagramScraper.total_pic_downl)
                print("total_pic_downl update")
                time.sleep(1)

            t3 = threading.Thread(target=update_)
            t3.daemon = True
            t3.start()

    #checking for each entry field
    def check_fields(self,dst_f,htag_f,limit_f,limit_user_f):
        if dst_f == '' or not os.path.isdir(dst_f):
            messagebox.showerror("Wrong destination folder",
                                 "Please input a path folder or choose a destination folder")
            return False

        if htag_f == '':
            messagebox.showerror("Empty field",
                                 "Please choose a HashTag (e.g: Weddingxny)")
            return False

        if limit_f == '' or not limit_f.isdigit():
            messagebox.showerror("Empty/wrong field",
                                 "Please choose the max number of picture you wan't to download ")
            return False

        if limit_user_f == '' or not limit_user_f.isdigit():
            messagebox.showerror("Empty/wrong field",
                                 "Please choose the max number by User of picture you wan't to download ")
            return False
        return True



    def run(self,event):

        self.lab_tnum['text'] = '0'
        self.update_total_downl()
        htag = self.htag_entry.get()
        limit_pic = self.limit_entry.get()
        dst = self.dst_path_entry.get()
        max_pic_by_user = self.maxPic_byUser_entry.get()
        app.InstagramScraper.max_by_owner = max_pic_by_user
        app.InstagramScraper.stop = False
        if self.check_fields(dst, htag, limit_pic, max_pic_by_user):
            self.traitement()
            t = threading.Thread(target=app.run,args=(htag,limit_pic,dst))
            t.daemon = True
            t.start()
        # t.join()
       # app.run(htag,limit_pic)


def launchEntryApp():
    root = tk.Tk()
    root.title("Insta'mag")
    root.geometry("400x500")
    img = tk.Image("photo", file="icon_insta_mag.icns")
    # root.iconphoto(True, img) # you may also want to try this.
    root.tk.call('wm', 'iconphoto', root._w, img)
    GUI(root)
    tk.mainloop()


def test():
    launchEntryApp()


if __name__ == '__main__': test()
