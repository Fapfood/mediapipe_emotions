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



def none():
   print( "Hello Python", "Hello World")

Button1 = tk.Button(win, text ="Hello", command = none(), height= 2, width=20)
Button1.place(x=746, y=750)


show_frames()
win.mainloop()