# Import required Libraries
from tkinter import *
from PIL import Image, ImageTk
import cv2
import tkinter as tk
from face_swapping import mp_face_mesh, mp_drawing, create_config, process_target_face_mesh, classify, swap_faces

# Create an instance of TKinter Window or frame
win = Tk()

# Set the size of the window
win.geometry('1440x800')

# Create a Label to capture the Video frames
label = Label(win)
label.place(x=720, y=250, anchor=CENTER)
cap = cv2.VideoCapture(0)
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_faces=3)
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

config_men1 = create_config(face_mesh, drawing_spec, 'Boy')
config_men2 = create_config(face_mesh, drawing_spec, 'men')
config_men3 = create_config(face_mesh, drawing_spec, 'OldMen')
config_women1 = create_config(face_mesh, drawing_spec, 'girl')
config_women2 = create_config(face_mesh, drawing_spec, 'womanl')
config_women3 = create_config(face_mesh, drawing_spec, 'Grandma')
configs = {0: config_men1, 1: config_men2, 2: config_men3}

mode = ['none']


# Define function to show frame
def show_frames():
    # Get the latest frame and convert into Image
    cv2image = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    # Convert image to PhotoImage
    imgtk = ImageTk.PhotoImage(image=img)
    label.imgtk = imgtk
    label.configure(image=imgtk)
    # Repeat after an interval to capture continiously
    label.after(20, show_frames)


def main():
    success, webcam_img = cap.read()

    landmark_target_ocvs, target_input_image, multi_face_landmarks = process_target_face_mesh(face_mesh, webcam_img)
    out_image = webcam_img.copy()
    clone = target_input_image

    if multi_face_landmarks is not None:
        for index, face_landmarks in enumerate(multi_face_landmarks):
            mp_drawing.draw_landmarks(
                image=out_image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=drawing_spec,
                connection_drawing_spec=drawing_spec)
            emotion = classify(face_landmarks.landmark)
            print(index, emotion)

            if len(landmark_target_ocvs[index]) > 0:
                for i, elem in enumerate(landmark_target_ocvs[index]):
                    if elem is None:
                        emotion = 'unknown'
                        break
                    if len(elem) != 2:
                        print(i)

                if emotion != 'unknown':
                    landmark_base_ocv, base_input_image = configs[index][emotion]
                    seam_clone, seamless_clone = swap_faces(landmark_base_ocv, landmark_target_ocvs[index],
                                                            base_input_image, clone)
                    if mode[0] == 'seamless':
                        clone = seamless_clone
                    elif mode[0] == 'seam':
                        clone = seam_clone
                    else:
                        clone = out_image

    cv2image = cv2.cvtColor(clone, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    label.imgtk = imgtk
    label.configure(image=imgtk)
    label.after(20, main)


def seam():
    mode[0] = 'seam'


Button1 = tk.Button(win, text="SEAM", command=seam, height=2, width=20, bg='white')
Button1.place(x=746, y=550)


def seamless():
    mode[0] = 'seamless'


Button2 = tk.Button(win, text="SEAMLESS", command=seamless, height=2, width=20, bg='white')
Button2.place(x=939, y=550)


def none():
    mode[0] = 'none'


Button3 = tk.Button(win, text="NONE", command=none, height=2, width=20, bg='white')
Button3.place(x=1132, y=550)


def user3_man():
    configs[2] = config_men3


Button4 = tk.Button(win, text="MAN", command=user3_man, height=2, width=20, bg='white')
Button4.place(x=553, y=550)


def user3_woman():
    configs[2] = config_women3


Button5 = tk.Button(win, text="WOMAN", command=user3_woman, height=2, width=20, bg='white')
Button5.place(x=553, y=620)


def user2_man():
    configs[1] = config_men2


Button6 = tk.Button(win, text="MAN", command=user2_man, height=2, width=20, bg='white')
Button6.place(x=360, y=550)


def user2_woman():
    configs[1] = config_women2


Button6 = tk.Button(win, text="WOMAN", command=user2_woman, height=2, width=20, bg='white')
Button6.place(x=360, y=620)


def user1_man():
    configs[0] = config_men1


Button7 = tk.Button(win, text="MAN", command=user1_man, height=2, width=20, bg='white')
Button7.place(x=167, y=550)


def user1_woman():
    configs[0] = config_women1


Button8 = tk.Button(win, text="WOMAN", command=user1_woman, height=2, width=20, bg='white')
Button8.place(x=167, y=620)

main()
win.mainloop()
face_mesh.close()
cap.release()
