# Import required Libraries
from tkinter import *
from PIL import Image, ImageTk
import cv2
import tkinter as tk


# Create an instance of TKinter Window or frame
win = Tk()

# Set the size of the window
win.geometry("1440x900")

# Create a Label to capture the Video frames
label =Label(win)
label.place(x=720, y=450, anchor= CENTER)
cap= cv2.VideoCapture(0)

# Define function to show frame
def show_frames():
   # Get the latest frame and convert into Image
   cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
   img = Image.fromarray(cv2image)
   # Convert image to PhotoImage
   imgtk = ImageTk.PhotoImage(image = img)
   label.imgtk = imgtk
   label.configure(image=imgtk)
   # Repeat after an interval to capture continiously
   label.after(20, show_frames)



def seam():
   print( "Hello Python", "Hello World")

Button1 = tk.Button(win, text ="SEAM", command = seam(), height= 2, width=20, bg='white')
Button1.place(x=746, y=750)


def seamless():
   print( "Hello Python", "Hello World")

Button2 = tk.Button(win, text ="SEAMLESS", command = seamless(), height= 2, width=20, bg='white')
Button2.place(x=939, y=750)

def none():
   print( "Hello Python", "Hello World")

Button3 = tk.Button(win, text ="NONE", command = none(), height= 2, width=20, bg='white')
Button3.place(x=1132, y=750)

def user3_men():
   print( "Hello Python", "Hello World")

Button4 = tk.Button(win, text ="MEN", command = user3_men(), height= 2, width=20, bg='white')
Button4.place(x=553, y=750)

def user3_woman():
   print( "Hello Python", "Hello World")

Button5 = tk.Button(win, text ="WOMAN", command = user3_woman(), height= 2, width=20, bg='white')
Button5.place(x=553, y=820)

def user2_men():
   print( "Hello Python", "Hello World")

Button6 = tk.Button(win, text ="MEN", command = user2_men(), height= 2, width=20, bg='white')
Button6.place(x=360, y=750)

def user2_woman():
   print( "Hello Python", "Hello World")

Button6 = tk.Button(win, text ="WOMAN", command = user2_woman(), height= 2, width=20, bg='white')
Button6.place(x=360, y=820)

def user1_men():
   print( "Hello Python", "Hello World")

Button7 = tk.Button(win, text ="MEN", command = user1_men(), height= 2, width=20, bg='white')
Button7.place(x=167, y=750)

def user1_woman():
   print( "Hello Python", "Hello World")

Button8 = tk.Button(win, text ="WOMAN", command = user1_woman(), height= 2, width=20, bg='white')
Button8.place(x=167, y=820)




show_frames()
win.mainloop()