from dis import dis
import socket
import threading
import time
from PIL import Image
import matplotlib.pyplot as pl
import msvcrt
import tkinter
import tkinter.messagebox
from tkinter import messagebox
import msvcrt
import struct
import io
import pickle
import cv2
from yolov5 import detect
import os
#from App import tempp,humii,diss,gass

HOST = '192.168.1.11'  # The server's hostname or IP address
PORT = 5555      # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))

#global data 
def camera(my):
    #my = "c"
    i = 0
    my_inp = my.encode('utf-8')
    s.sendall(my_inp)
    #data = s.recv(1024).decode('utf-8') 
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        while len(data) < payload_size:
            packet = s.recv(4*1024)
            if not packet: break
            data+=packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q",packed_msg_size)[0]

        while len(data) < msg_size:
            data+= s.recv(4*1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imwrite('Frame'+str(i)+'.jpg', frame)
        if i < 5:
            i += 1
        #os.system("cd/yolov5")
        #os.system("python detect.py path/C:\Users\tygre\Desktop\Mov\Frame2.jpg")
        cv2.imshow("Recived", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            cv2.destroyAllWindows()
            return

def tempp(my):
        my_inp = my.encode('utf-8')
        s.sendall(my_inp)
        data = s.recv(1024).decode('utf-8') 
        tkinter.messagebox.showinfo("Info: ", data)
def humii(my):
        my_inp = my.encode('utf-8')
        s.sendall(my_inp)
        data = s.recv(1024).decode('utf-8')
        tkinter.messagebox.showinfo("Info: ", data)
def gass(my):
        my_inp = my.encode('utf-8')
        s.sendall(my_inp)
        data = s.recv(1024).decode('utf-8')
        tkinter.messagebox.showinfo("Info: ", data)
def diss(my):
        my_inp = my.encode('utf-8')
        s.sendall(my_inp)
        data = s.recv(1024).decode('utf-8')
        tkinter.messagebox.showinfo("Info: ", data)

def my_client(my):

    #threading.Timer(11, my_client).start()
    #         
    #print("Sending Command")
    #while True:
        #my = input("Enter Command: ")
    my_inp = my.encode('utf-8')
    s.sendall(my_inp)

    #if my == 'q':
    #    s.close()
    #elif my == '1':
    #    data = s.recv(1024).decode('utf-8')   
    #    print(data)
    #elif my == '2':
    #    data = s.recv(1024).decode('utf-8')   
    #    print(data)
    #elif my == '3':
    #    data = s.recv(1024).decode('utf-8')   
    #    print(data)
    #elif my == '4':
    #    data = s.recv(1024).decode('utf-8')   
    #    print(data)


    #data = s.recv(1024).decode('utf-8')  
    #print(data)
    
    #data = s.recv(1024).decode('utf-8')   
    #print(data)
    
    #data = s.recv(1024).decode('utf-8')   
    #print(data)
    
    #data = s.recv(1024).decode('utf-8')   
    #print(data)
    
    if my == 'q':
        s.close()
    
        #if str(data) == 'w':
        #    print("Forward:   ", data)
        #elif str(data) == 's':
        #    print ("Downward:  ", data)
        #elif str(data) == 'a':
        #    print ("Leftward:  ",data)
        #elif str(data) == 'd':
        #    print ("Rightward: ", data)
        #elif str(data) == 'q':
        #    s.close()


if __name__ == "__main__":
    while 1:
        my_client()
        tempp()
        humii()
        gass()
        diss()
        camera()