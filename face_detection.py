import tkinter as tk
from tkinter import Label
import cv2
from PIL import Image, ImageTk


class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.video_source = 0

        # Video yakalama
        self.vid = cv2.VideoCapture(self.video_source)

        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", self.video_source)

        # Önceden eğitilmiş yüz algılama modelinin yüklenmesi
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Video çerçevesi için canvas
        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH),
                                height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        # Ekranı kapatmak için "close" butonu
        self.btn_close = tk.Button(window, text="Close", width=50, command=self.quit)
        self.btn_close.pack(anchor=tk.CENTER, expand=True)

        # Video karelerinin update edilmesi
        self.update()

        self.window.mainloop()

    def update(self):
        # Video kaynağından bir kare alınması
        ret, frame = self.vid.read()
        if ret:
            # Yüz algılama için görüntünün gri tonlamaya dönüştürülmesi
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Görüntüdeki yüzlerin algılanması
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # Algılanan yüzlerin etrafına bir dikdörtgen çizilmesi
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Görüntünün PhotoImage'a dönüştürülmesi
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        # Belirli bir gecikmeden sonra update() öğesinin tekrar çağrılması
        self.window.after(10, self.update)

    def quit(self):
        self.window.destroy()
        self.vid.release()


# Bir pencere oluşturulup  App sınıfına iletilmesi
App(tk.Tk(), "Tkinter and OpenCV")
