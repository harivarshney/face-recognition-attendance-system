# Modernized Face Recognition Attendance System

import tkinter as tk
from tkinter import ttk, messagebox as mess
import tkinter.simpledialog as tsd
import cv2, os, csv, numpy as np
from PIL import Image
import pandas as pd
import datetime, time

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200, tick)

def contact():
    mess._show(title='Contact Us', message="Please contact us at: 'yourmail@domain.com'")

def check_haarcascadefile():
    if not os.path.isfile("haarcascade_frontalface_default.xml"):
        mess._show(title='File Missing', message='Haarcascade file missing. Please place it correctly.')
        window.destroy()

def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel/psd.txt")
    if exists1:
        tf = open("TrainingImageLabel/psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('No Password Found', 'Set a new password:', show='*')
        if new_pas is None:
            mess._show(title='Password Error', message='Password not set. Try again.')
        else:
            with open("TrainingImageLabel/psd.txt", "w") as tf:
                tf.write(new_pas)
            mess._show(title='Success', message='New password registered successfully.')
            return

    op, newp, nnewp = old.get(), new.get(), nnew.get()
    if op == key:
        if newp == nnewp:
            with open("TrainingImageLabel/psd.txt", "w") as txf:
                txf.write(newp)
            mess._show(title='Success', message='Password changed successfully!')
            master.destroy()
        else:
            mess._show(title='Error', message='New passwords do not match.')
    else:
        mess._show(title='Error', message='Old password is incorrect.')

def change_pass():
    global master
    master = tk.Toplevel(window)
    master.geometry("400x180")
    master.title("Change Password")
    master.configure(bg="#2c2c2c")

    tk.Label(master, text='Old Password', bg='#2c2c2c', fg='white', font=('Helvetica', 12)).place(x=10, y=10)
    tk.Label(master, text='New Password', bg='#2c2c2c', fg='white', font=('Helvetica', 12)).place(x=10, y=50)
    tk.Label(master, text='Confirm Password', bg='#2c2c2c', fg='white', font=('Helvetica', 12)).place(x=10, y=90)

    global old, new, nnew
    old = tk.Entry(master, show='*', width=25)
    new = tk.Entry(master, show='*', width=25)
    nnew = tk.Entry(master, show='*', width=25)
    old.place(x=160, y=10)
    new.place(x=160, y=50)
    nnew.place(x=160, y=90)

    tk.Button(master, text='Save', command=save_pass, bg='#00bcd4', fg='white', width=12).place(x=40, y=130)
    tk.Button(master, text='Cancel', command=master.destroy, bg='red', fg='white', width=12).place(x=200, y=130)


def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel/psd.txt")
    if exists1:
        tf = open("TrainingImageLabel/psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Password Setup', 'Set a new password:', show='*')
        if new_pas is not None:
            with open("TrainingImageLabel/psd.txt", "w") as tf:
                tf.write(new_pas)
            mess._show(title='Success', message='Password registered successfully.')
        return

    password = tsd.askstring('Authentication', 'Enter Password', show='*')
    if password == key:
        TrainImages()
    elif password is None:
        pass
    else:
        mess._show(title='Error', message='Incorrect password.')


def clear():
    txt.delete(0, 'end')
    message1.configure(text="1) Take Images  >>>  2) Save Profile")

def clear2():
    txt2.delete(0, 'end')
    message1.configure(text="1) Take Images  >>>  2) Save Profile")


def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    serial = 1

    if os.path.isfile("StudentDetails/StudentDetails.csv"):
        with open("StudentDetails/StudentDetails.csv", 'r') as file:
            serial = sum(1 for line in file) // 2
    else:
        with open("StudentDetails/StudentDetails.csv", 'a+') as file:
            writer = csv.writer(file)
            writer.writerow(columns)

    Id, name = txt.get().strip(), txt2.get().strip()
    
    # Validate inputs
    if not Id:
        message.configure(text="Please enter a valid ID")
        return
    if not name or not name.replace(' ', '').isalpha():
        message.configure(text="Please enter a valid name (letters only)")
        return
    
    # Try multiple camera indices if needed
    cam = None
    for camera_idx in [0, 1, 2]:
        test_cam = cv2.VideoCapture(camera_idx)
        if test_cam.isOpened():
            cam = test_cam
            break
        test_cam.release()
    
    if cam is None:
        mess._show(title='Camera Error', message='No camera found! Please check your camera connection.')
        return
    
    # Set camera properties for better performance
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cam.set(cv2.CAP_PROP_FPS, 30)
    
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    sampleNum = 0
    message.configure(text=f"Taking images for {name}. Press 'q' to stop or wait for 100 samples")
    
    while True:
        ret, img = cam.read()
        if not ret:
            mess._show(title='Camera Error', message='Failed to read from camera!')
            break
            
        # Flip image horizontally for mirror effect
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5, minSize=(30, 30))
        
        for (x, y, w, h) in faces:
            sampleNum += 1
            # Save the face image
            cv2.imwrite(f"TrainingImage/{name}.{serial}.{Id}.{sampleNum}.jpg", gray[y:y+h, x:x+w])
            # Draw rectangle around face
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # Show sample count
            cv2.putText(img, f"Sample: {sampleNum}/100", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        # Show instructions
        cv2.putText(img, "Press 'q' to quit", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(img, f"ID: {Id}, Name: {name}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        cv2.imshow('Capturing Images - Position your face in the frame', img)
        
        # Break conditions
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or sampleNum >= 100:
            break
    
    cam.release()
    cv2.destroyAllWindows()
    
    if sampleNum > 0:
        with open('StudentDetails/StudentDetails.csv', 'a+') as file:
            writer = csv.writer(file)
            writer.writerow([serial, '', Id, '', name])
        message1.configure(text=f"Successfully captured {sampleNum} images for {name} (ID: {Id})")
        message.configure(text="Images captured successfully! Now you can train the model.")
    else:
        message.configure(text="No face detected! Please ensure good lighting and try again.")
        message1.configure(text="No images captured. Please try again.")


def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    faces, ID = getImagesAndLabels("TrainingImage")
    if not faces:
        mess._show(title='Error', message='No faces found to train!')
        return
    recognizer.train(faces, np.array(ID))
    recognizer.save("TrainingImageLabel/Trainner.yml")
    message1.configure(text='Training Complete')
    message.configure(text=f'Total Registrations: {len(set(ID))}')


def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces, Ids = [], []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")
    
    for k in tv.get_children():
        tv.delete(k)
    
    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    if not os.path.isfile("TrainingImageLabel/Trainner.yml"):
        mess._show(title='Error', message='No training data found! Please train the model first.')
        return
    
    recognizer.read("TrainingImageLabel/Trainner.yml")
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    
    if not os.path.isfile("StudentDetails/StudentDetails.csv"):
        mess._show(title='Error', message='No student details found! Please register students first.')
        return
    
    df = pd.read_csv("StudentDetails/StudentDetails.csv")
    cam = cv2.VideoCapture(0)
    
    # Create attendance file for today
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    attendance_file = f"Attendance/Attendance_{date_str}.csv"
    
    if not os.path.isfile(attendance_file):
        with open(attendance_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Name', 'Time', 'Status'])
    
    # Read existing attendance
    attendance_df = pd.read_csv(attendance_file)
    
    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            serial, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            
            if confidence < 50:
                # Find student name
                student_row = df[df['SERIAL NO.'] == serial]
                if not student_row.empty:
                    student_name = student_row.iloc[0]['NAME']
                    student_id = student_row.iloc[0]['ID']
                    
                    # Check if already marked present today
                    if not ((attendance_df['ID'] == student_id) & (attendance_df['Status'] == 'Present')).any():
                        # Mark attendance
                        with open(attendance_file, 'a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([student_id, student_name, time_str, 'Present'])
                        
                        msg = f"Attendance marked for {student_name} (ID: {student_id})"
                        cv2.putText(img, f"Present: {student_name}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    else:
                        msg = f"{student_name} already marked present"
                        cv2.putText(img, f"Already Present: {student_name}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                else:
                    cv2.putText(img, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            else:
                cv2.putText(img, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        
        cv2.imshow('Attendance System', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cam.release()
    cv2.destroyAllWindows()
    
    # Update the treeview
    if msg:
        message.configure(text=msg)
    
    # Load and display today's attendance
    if os.path.isfile(attendance_file):
        attendance_df = pd.read_csv(attendance_file)
        for index, row in attendance_df.iterrows():
            tv.insert('', 'end', values=(row['ID'], row['Name'], row['Time'], row['Status']))

window = tk.Tk()
window.geometry("1280x720")
window.title("Face Attendance System")
window.configure(bg='#1e1e1e')

title_label = tk.Label(window, text="Face Recognition Attendance System", 
                      bg='#1e1e1e', fg='#00bcd4', font=('Helvetica', 20, 'bold'))
title_label.pack(pady=10)

clock = tk.Label(window, bg='#1e1e1e', fg='white', font=('Helvetica', 14))
clock.pack()
tick()

main_frame = tk.Frame(window, bg='#1e1e1e')
main_frame.pack(fill='both', expand=True, padx=20, pady=20)

left_frame = tk.Frame(main_frame, bg='#2c2c2c', width=400)
left_frame.pack(side='left', fill='y', padx=(0, 10))
left_frame.pack_propagate(False)

reg_frame = tk.LabelFrame(left_frame, text="Student Registration", bg='#2c2c2c', fg='white', font=('Helvetica', 12, 'bold'))
reg_frame.pack(fill='x', padx=10, pady=10)

tk.Label(reg_frame, text="Enter ID:", bg='#2c2c2c', fg='white', font=('Helvetica', 10)).pack(anchor='w', padx=10, pady=(10, 0))
txt = tk.Entry(reg_frame, width=25, font=('Helvetica', 10))
txt.pack(padx=10, pady=(0, 10))

tk.Label(reg_frame, text="Enter Name:", bg='#2c2c2c', fg='white', font=('Helvetica', 10)).pack(anchor='w', padx=10)
txt2 = tk.Entry(reg_frame, width=25, font=('Helvetica', 10))
txt2.pack(padx=10, pady=(0, 10))

btn_frame = tk.Frame(reg_frame, bg='#2c2c2c')
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Take Images", command=TakeImages, bg='#00bcd4', fg='white', width=12, font=('Helvetica', 10)).pack(side='left', padx=5)
tk.Button(btn_frame, text="Clear", command=clear, bg='#ff5722', fg='white', width=8, font=('Helvetica', 10)).pack(side='left', padx=5)

train_frame = tk.LabelFrame(left_frame, text="Model Training", bg='#2c2c2c', fg='white', font=('Helvetica', 12, 'bold'))
train_frame.pack(fill='x', padx=10, pady=10)

tk.Button(train_frame, text="Train Model", command=psw, bg='#4caf50', fg='white', width=20, font=('Helvetica', 10)).pack(pady=10)
tk.Button(train_frame, text="Change Password", command=change_pass, bg='#ff9800', fg='white', width=20, font=('Helvetica', 10)).pack(pady=(0, 10))

attendance_frame = tk.LabelFrame(left_frame, text="Attendance Tracking", bg='#2c2c2c', fg='white', font=('Helvetica', 12, 'bold'))
attendance_frame.pack(fill='x', padx=10, pady=10)

tk.Button(attendance_frame, text="Track Attendance", command=TrackImages, bg='#9c27b0', fg='white', width=20, font=('Helvetica', 10)).pack(pady=10)

other_frame = tk.LabelFrame(left_frame, text="Other Options", bg='#2c2c2c', fg='white', font=('Helvetica', 12, 'bold'))
other_frame.pack(fill='x', padx=10, pady=10)

tk.Button(other_frame, text="Contact Us", command=contact, bg='#607d8b', fg='white', width=20, font=('Helvetica', 10)).pack(pady=10)

right_frame = tk.Frame(main_frame, bg='#2c2c2c')
right_frame.pack(side='right', fill='both', expand=True)

display_frame = tk.LabelFrame(right_frame, text="Today's Attendance", bg='#2c2c2c', fg='white', font=('Helvetica', 12, 'bold'))
display_frame.pack(fill='both', expand=True, padx=10, pady=10)

columns = ('ID', 'Name', 'Time', 'Status')
tv = ttk.Treeview(display_frame, columns=columns, show='headings', height=15)

for col in columns:
    tv.heading(col, text=col)
    tv.column(col, width=120, anchor='center')

scrollbar = ttk.Scrollbar(display_frame, orient='vertical', command=tv.yview)
tv.configure(yscrollcommand=scrollbar.set)

tv.pack(side='left', fill='both', expand=True, padx=10, pady=10)
scrollbar.pack(side='right', fill='y', pady=10)

message_frame = tk.Frame(window, bg='#1e1e1e')
message_frame.pack(fill='x', padx=20, pady=(0, 20))

message = tk.Label(message_frame, text="System Ready", bg='#1e1e1e', fg='#00bcd4', font=('Helvetica', 12))
message.pack(side='left')

message1 = tk.Label(message_frame, text="1) Take Images  >>>  2) Save Profile", bg='#1e1e1e', fg='white', font=('Helvetica', 10))
message1.pack(side='right')

window.mainloop()
