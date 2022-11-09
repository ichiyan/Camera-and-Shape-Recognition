from datetime import datetime
import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import StringVar, messagebox, filedialog



class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.delay = 10
        self.is_detecting_shapes = False

        self.vid = cv2.VideoCapture(self.video_source)

        self.camera_label = tk.Label(window, width= int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)), height=int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        self.camera_label.grid(row=0, columnspan=8, padx=0, pady=0)

        self.capture_btn = tk.Button(window, width=10, text="Capture", command=self.capture, borderwidth=3, padx=7, pady=7, relief=tk.RAISED, bg="#4465e7", fg="#ffffff")
        self.capture_btn.grid(row=1, column=3, padx=0, pady=10)

        self.detect_shapes_btn = tk.Button(window, width=15, text="Detect Shapes", command=self.detect_shapes_btn_on_click, borderwidth=3, padx=7, pady=7, relief=tk.RAISED, bg="#4465e7", fg="#ffffff")
        self.detect_shapes_btn.grid(row=1, column=4, padx=0, pady=10)

        self.window.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.show_feed()
        self.window.mainloop()

    def show_feed(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.flip(frame, 1)
            # cv2.putText(frame, datetime.now().strftime('%d/%m/%y %H:%M:%S'), (20,30), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,255)) 
            # img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

            if not self.is_detecting_shapes:
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 
            else:
                processed = self.process_image(frame)
                img = processed

            imgtk = ImageTk.PhotoImage(Image.fromarray(img))
            self.camera_label.configure(image=imgtk)
            self.camera_label.imgtk = imgtk
            self.camera_label.after(self.delay, self.show_feed)

            # if self.is_detecting_shapes:
            #     processed = self.process_image(frame)

        else:
            self.camera_label.configure(image='')


    def capture(self):

        default_img_name = datetime.now().strftime('%d-%m-%y %H-%M-%S')   

        img = filedialog.asksaveasfilename(filetypes=[('JPEG Image', '*.jpg'), ('PNG Image', '*.png')], 
                                            initialfile=default_img_name,
                                            defaultextension='.jpg',
                                            initialdir="images")

        ret, frame = self.vid.read()
        saved_img = cv2.imwrite(img, frame)
    
        if saved_img:
            messagebox.showinfo("Success", "Image saved at " + img)

    def process_image(self, frame):
        # ret, frame = self.vid.read()

        processed = cv2.GaussianBlur(frame, (7, 7), 1)
        processed = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)
        processed = cv2.Canny(processed, 200, 25)


        contours, hierarchy = cv2.findContours(processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # print
        # print(type(contours))
        # print(type(contours[0]))
        # exit()

        # for cnt in contours:
        #     print(type(cnt))
        #     print(cnt)
        #     exit()
            # peri = cv2.arcLength(cnt, True)
        #     approx = rdp(cnt, peri * 0.02)
        #     # print(approx)
        #     print(len(approx))

        # processed = gaussian_blurv2(frame, 3, 2)  
        # processed = CannyEdgeDetector(processed)
        # test = cv2.drawContours(frame, contours, -1, (255, 0, 255), 7)

   


        return processed


    def detect_shapes_btn_on_click(self):
        self.is_detecting_shapes = not self.is_detecting_shapes
        if self.is_detecting_shapes:
            self.detect_shapes_btn.configure(text="Stop Shape Detection")
        else: 
            self.detect_shapes_btn.configure(text="Detect Shape")

    def on_exit(self):
        self.vid.release()
        self.window.destroy()

def main():
    App(tk.Tk(), 'Camera')
    
if __name__  == "__main__":
    main()





