# Import required Libraries
from tkinter import *
from PIL import Image, ImageTk
import cv2
import tkinter as tk
from face_swapping import mp_face_mesh, mp_drawing, process_target_face_mesh, classify, swap_faces
from config import configs, face_mesh, drawing_spec
from config import seam, seamless, none, user1_man, user2_man, user3_man, user1_woman, user2_woman, user3_woman

# Create an instance of TKinter Window or frame
win = Tk()

# Set the size of the window
win.geometry('850x800')

# Create a Label to capture the Video frames
label = Label(win)
label.place(x=100, y=150)
cap = cv2.VideoCapture(0)


def show_frames():
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
                    landmark_base_ocv, base_input_image = configs[index + 1][emotion]
                    seam_clone, seamless_clone = swap_faces(landmark_base_ocv, landmark_target_ocvs[index],
                                                            base_input_image, clone)

                    if configs['mode'] == 'seamless':
                        clone = seamless_clone
                    elif configs['mode'] == 'seam':
                        clone = seam_clone
                    else:
                        clone = out_image

    cv2image = cv2.cvtColor(clone, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    label.imgtk = imgtk
    label.configure(image=imgtk)
    label.after(20, show_frames)


Button1 = tk.Button(win, text="SEAM", command=seam, height=2, width=20, bg='green')
Button1.place(x=100, y=50)
Button2 = tk.Button(win, text="SEAMLESS", command=seamless, height=2, width=20, bg='green')
Button2.place(x=350, y=50)
Button3 = tk.Button(win, text="NONE", command=none, height=2, width=20, bg='green')
Button3.place(x=600, y=50)

Button4 = tk.Button(win, text="MAN", command=user1_man, height=2, width=20, bg='white')
Button4.place(x=100, y=650)
Button5 = tk.Button(win, text="WOMAN", command=user1_woman, height=2, width=20, bg='white')
Button5.place(x=100, y=720)
Button6 = tk.Button(win, text="MAN", command=user2_man, height=2, width=20, bg='white')
Button6.place(x=350, y=650)
Button6 = tk.Button(win, text="WOMAN", command=user2_woman, height=2, width=20, bg='white')
Button6.place(x=350, y=720)
Button7 = tk.Button(win, text="MAN", command=user3_man, height=2, width=20, bg='white')
Button7.place(x=600, y=650)
Button8 = tk.Button(win, text="WOMAN", command=user3_woman, height=2, width=20, bg='white')
Button8.place(x=600, y=720)

show_frames()
win.mainloop()
face_mesh.close()
cap.release()
