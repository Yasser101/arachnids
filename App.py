from pickle import FRAME
import tkinter as tk
from tkinter import messagebox
import tkinter
from turtle import onclick
from click import command
import cv2
import PIL.Image
import PIL.ImageTk
import time
import datetime as dt
import argparse
from tkinter import *
from numpy import pad
from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT
from tkinter.ttk import Frame, Label, Entry


import MovCli 
from MovCli import tempp, humii, gass, diss
class SpiderApp:

    sensorReading=NONE

    #def tempp(self):
    #    tkinter.messagebox.showinfo("hi","hello1")
    #def humii(self):
    #    tkinter.messagebox.showinfo("hi","hello2")
    #def gass(self):
    #    tkinter.messagebox.showinfo("hi","hello3")
    #def diss(self):
    #    tkinter.messagebox.showinfo("hi","hello4")


    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.ok = False

        # timer
        self.timer = ElapsedTimeClock(self.window)

        # open video source (by default this will try to open the computer webcam)
        self.vid = VideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        
       # self.camm=tk.Button(window,text="Camera",command=lambda:MovCli.camera('c'))
        #self.camm.pack(side=tk.BOTTOM)

        self.canvas = tk.Canvas(
            window, width=500, height=500)
        self.canvas.pack()
########################################################


        self.temp = tk.Button(
           window, text="Temprature" , command=lambda: MovCli.tempp('2'))
        self.temp.pack(side=tk.BOTTOM)

        self.gas = tk.Button(
           window, text="Gas" , command=lambda: MovCli.gass('3'))
        self.gas.pack(side=tk.BOTTOM)

        self.dist = tk.Button(
           window, text="Distance" , command=lambda: MovCli.diss('1'))
        self.dist.pack(side=tk.BOTTOM)

        self.humid = tk.Button(
           window, text="Humidty" , command=lambda: MovCli.humii('4'))
        self.humid.pack(side=tk.BOTTOM)


        #######################################
        self.btn_snapshot = tk.Button(
            window, text="Snapshot", command=self.snapshot)
        self.btn_snapshot.pack(side=tk.LEFT)

        self.cameraa = tk.Button(
            window, text="Camera", command=lambda: MovCli.camera('c'))
        self.cameraa.pack(side=tk.LEFT)

        self.btn_start = tk.Button(
            window, text='START', command=self.open_camera)
        self.btn_start.pack(side=tk.LEFT)

        self.btn_stop = tk.Button(
            window, text='STOP', command=self.close_camera)
        self.btn_stop.pack(side=tk.LEFT)

        self.btn_quit = tk.Button(window, text='QUIT', command=lambda: MovCli.my_client('q'))
        self.btn_quit.pack(side=tk.LEFT)

        self.moveForwardW = tk.Button(
            window, text="Forward", command=lambda: MovCli.my_client('w'))
        self.moveForwardW.pack(side=tk.LEFT)

        self.moveBacwardS = tk.Button(
            window, text="Backward", command=lambda:MovCli. my_client('s'))
        self.moveBacwardS.pack(side=tk.LEFT)

        self.sit = tk.Button(
            window, text="Sit", command=lambda:MovCli. my_client('sit'))
        self.sit.pack(side=tk.LEFT)

        self.stand = tk.Button(
            window, text="Stand", command=lambda: MovCli.my_client('stand'))
        self.stand.pack(side=tk.LEFT)

        self.dance = tk.Button(
            window, text="Dance", command=lambda:MovCli. my_client('dance'))
        self.dance.pack(side=tk.LEFT)

        self.wave = tk.Button(
            window, text="Wave", command=lambda: MovCli.my_client('wave'))
        self.wave.pack(side=tk.LEFT)

        self.shake = tk.Button(
            window, text="Shake", command=lambda: MovCli.my_client('shake'))
        self.shake.pack(side=tk.LEFT)

        self.moveRightD = tk.Button(
            window, text="Move Right", command=lambda: MovCli.my_client('d'))
        self.moveRightD.pack(side=tk.LEFT)

        self.moveLeftA = tk.Button(
            window, text="Move Left", command=lambda: MovCli.my_client('a'))
        self.moveLeftA.pack(side=tk.LEFT)

        self.delay = 10
        self.update()
        self.window.mainloop()

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            cv2.imwrite("frame-"+time.strftime("%d-%m-%Y-%H-%M-%S") +
                        ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def open_camera(self):
        self.ok = True
        self.timer.start()
        print("camera opened => Recording")

    def close_camera(self):
        self.ok = False
        self.timer.stop()
        print("camera closed => Not Recording")

    def update(self):

        #Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if self.ok:
            self.vid.out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

        self.photo = PIL.ImageTk.PhotoImage(
                image=PIL.Image.fromarray(frame))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(self.delay, self.update)


class VideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Command Line Parser
        args = CommandLineParser().args

        VIDEO_TYPE = {
            'avi': cv2.VideoWriter_fourcc(*'XVID'),
            # 'mp4': cv2.VideoWriter_fourcc(*'H264'),
            'mp4': cv2.VideoWriter_fourcc(*'XVID'),
        }

        self.fourcc = VIDEO_TYPE[args.type[0]]

        STD_DIMENSIONS = {
            '480p': (640, 480),
            '720p': (1280, 720),
            '1080p': (1920, 1080),
            '4k': (3840, 2160),
        }
        res = STD_DIMENSIONS[args.res[0]]
        print(args.name, self.fourcc, res)
        self.out = cv2.VideoWriter(
            args.name[0]+'.'+args.type[0], self.fourcc, 10, res)

        self.vid.set(3, res[0])
        self.vid.set(4, res[1])

        self.width, self.height = res

    # To get frames

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
            self.out.release()
            cv2.destroyAllWindows()


class ElapsedTimeClock:
    def __init__(self, window):
        self.T = tk.Label(window, text='00:00:00', font=(
            'times', 20, 'bold'), bg='green')
        self.T.pack(fill=tk.BOTH, expand=1)
        self.elapsedTime = dt.datetime(1, 1, 1)
        self.running = 0
        self.lastTime = ''
        t = time.localtime()
        self.zeroTime = dt.timedelta(hours=t[3], minutes=t[4], seconds=t[5])
        # self.tick()

    def tick(self):
        self.now = dt.datetime(1, 1, 1).now()
        self.elapsedTime = self.now - self.zeroTime
        self.time2 = self.elapsedTime.strftime('%H:%M:%S')
        # if time string has changed, update it
        if self.time2 != self.lastTime:
            self.lastTime = self.time2
            self.T.config(text=self.time2)

        self.updwin = self.T.after(100, self.tick)

    def start(self):
        if not self.running:
            self.zeroTime = dt.datetime(1, 1, 1).now()-self.elapsedTime
            self.tick()
            self.running = 1

    def stop(self):
        if self.running:
            self.T.after_cancel(self.updwin)
            self.elapsedTime = dt.datetime(1, 1, 1).now()-self.zeroTime
            self.time2 = self.elapsedTime
            self.running = 0


class CommandLineParser:

    def __init__(self):
        parser = argparse.ArgumentParser(description='Script to record videos')
        # required_arguments=parser.add_argument_group('Required command line arguments')

        parser.add_argument('--type', nargs=1, default=[
                            'avi'], type=str, help='Type of the video output: for now we have only AVI & MP4')

        parser.add_argument('--res', nargs=1, default=[
                            '480p'], type=str, help='Resolution of the video output: for now we have 480p, 720p, 1080p & 4k')

        # Only one values are going to accept for the tag --name. So nargs will be '1'
        parser.add_argument(
            '--name', nargs=1, default=['output'], type=str, help='Enter Output video title/name')

        def __init__(self):
            super().__init__()

            self.initUI()

        # Parse the arguments and get all the values in the form of namespace.
        # Here args is of namespace and values will be accessed through tag names
        self.args = parser.parse_args()


def main():
    SpiderApp(tk.Tk(), 'Spider')


main()
