from datetime import datetime
import cv2
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import StringVar, messagebox, filedialog

class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.delay = 10

        self.vid = cv2.VideoCapture(self.video_source)

        self.camera_label = tk.Label(window, width= int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)), height=int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        self.camera_label.grid(row=0, columnspan=8, padx=0, pady=0)

        self.capture_btn = tk.Button(window, width=10, text="Capture", command=self.capture, borderwidth=3, padx=7, pady=7, relief=tk.RAISED, bg="#4465e7", fg="#ffffff")
        self.capture_btn.grid(row=1, column=3, padx=0, pady=10)

        self.detect_shapes_btn = tk.Button(window, width=10, text="Detect Shapes", command="", borderwidth=3, padx=7, pady=7, relief=tk.RAISED, bg="#4465e7", fg="#ffffff")
        self.detect_shapes_btn.grid(row=1, column=4, padx=0, pady=10)

        self.window.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.show_feed()
        self.window.mainloop()

    def show_feed(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.flip(frame, 1)
            # cv2.putText(frame, datetime.now().strftime('%d/%m/%y %H:%M:%S'), (20,30), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,255)) 
            cv2img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            imgtk = ImageTk.PhotoImage(Image.fromarray(cv2img))
            self.camera_label.configure(image=imgtk)
            self.camera_label.imgtk = imgtk
            self.camera_label.after(self.delay, self.show_feed)
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

    def process_image():
        pass

    def on_exit(self):
        self.vid.release()
        self.window.destroy()

def main():
    App(tk.Tk(), 'Camera')
    
if __name__  == "__main__":
    main()





