import cv2
import abc
import threading
import time
import customtkinter as CTk
from enum import IntEnum
from PIL import Image, ImageTk


class RecognitionType(IntEnum):
    Off = 0,
    Face = 1,
    FaceAndEyes = 2,
    FaceAndEyesAndSmile = 3
    FaceAndSmile = 4


faceCascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier('cascades/haarcascade_eye.xml')
smileCascade = cv2.CascadeClassifier('cascades/haarcascade_smile.xml')


class CaptureBase(metaclass=abc.ABCMeta):

    def __init__(self, video_source, width, height, fps):
        self.video_source = video_source
        self.width = width
        self.height = height
        self.fps = fps

        # Open the video source
        self.vid = cv2.VideoCapture(video_source, cv2.CAP_DSHOW)
        if not self.vid.isOpened():
            raise ValueError("[MyVideoCapture] Unable to open video source", video_source)

        # Get video source width and height
        if not self.width:
            self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))  # convert float to int
        if not self.height:
            self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))  # convert float to int
        if not self.fps or self.fps == 0:
            self.fps = int(self.vid.get(cv2.CAP_PROP_FPS))  # convert float to int
            if self.fps == 0: self.fps = 60

        # default value at start
        self.ret = False
        self.frame = None

        # start thread
        self.running = True
        self.thread = threading.Thread(target=self.process)
        self.thread.start()

    @abc.abstractmethod
    def process(self):
        pass

    def get_frame(self):
        return self.ret, self.frame

    def release_video(self):
        # stop thread
        if self.running:
            self.running = False
            self.thread.join()

        # release stream
        if self.vid.isOpened():
            self.vid.release()

    # Release the video source when the object is destroyed
    def __del__(self):
        self.release_video()
        cv2.destroyAllWindows()


class VideoCapture(CaptureBase):

    def __init__(self, video_source, width=None, height=None, fps=None):
        if int(video_source) == video_source:
            raise ValueError("You are passing a webcam index. For WebCam, you should use WebcamCapture class.")
        super().__init__(video_source, width, height, fps)

    def process(self):
        while self.running:
            ret, frame = self.vid.read()

            if ret:
                # process image
                frame = cv2.resize(frame, (self.width, self.height))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                print('[MyVideoCapture] stream end:', self.video_source)
                # TODO: reopen stream
                self.running = False
                break

            # assign new frame
            self.ret = ret
            self.frame = frame

            # sleep for next frame
            time.sleep(1 / self.fps)


class WebcamCapture(CaptureBase):

    def __init__(self, video_source=0, width=None, height=None, fps=None, recognition=RecognitionType.Off):

        if int(video_source) != video_source:
            raise ValueError("You should pass a webcam index. For a video stream, please provide the video URL or path string.")
        super().__init__(video_source, width, height, fps)
        self.recognition = recognition

    def process(self):
        while self.running:
            ret, frame = self.vid.read()

            frame = cv2.resize(frame, (self.width, self.height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.3,
                minNeighbors=5,
                minSize=(30, 30)
            )

            if self.recognition > RecognitionType.Off:

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                    roi_gray = gray[y:y + h, x:x + w]
                    roi_color = frame[y:y + h, x:x + w]

                    if self.recognition == RecognitionType.FaceAndEyes or self.recognition == RecognitionType.FaceAndEyesAndSmile:
                        eyes = eyeCascade.detectMultiScale(
                            roi_gray,
                            scaleFactor=1.5,
                            minNeighbors=5,
                            minSize=(5, 5),
                        )

                        for (ex, ey, ew, eh) in eyes:
                            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

                    if self.recognition == RecognitionType.FaceAndEyesAndSmile or self.recognition == RecognitionType.FaceAndSmile:
                        smile = smileCascade.detectMultiScale(
                            roi_gray,
                            scaleFactor=1.5,
                            minNeighbors=15,
                            minSize=(25, 25),
                        )
#
                        for (xx, yy, ww, hh) in smile:
                            cv2.rectangle(roi_color, (xx, yy), (xx + ww, yy + hh), (0, 255, 0), 2)

            # assign new frame
            self.ret = ret
            self.frame = frame

            # sleep for next frame
            time.sleep(1 / self.fps)


class VideoStreamWidget(CTk.CTkFrame):

    def __init__(self, master, text="", video_source=0, width=None, height=None, enable_start_stop=True, enable_snapshot=True):
        super().__init__(master)

        self.window = master
        self.video_source = video_source
        self.width = width
        self.height = height
        self.vid = None
        self.running = False
        self.photo = None

        if video_source == 0:
            self.isWebCam = True

        self.label = CTk.CTkLabel(self, text=text)
        self.label.pack()

        self.canvas = CTk.CTkCanvas(self, width=self.width, height=self.height)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        if enable_start_stop:
            if enable_snapshot:
                self.btn_snapshot = CTk.CTkButton(self, text="Ligar/Desligar", command=self.start_stop, fg_color="teal")
                self.btn_snapshot.pack(anchor='center', side='left', pady=10)

                # Button that lets the user take a snapshot
                self.btn_snapshot = CTk.CTkButton(self, text="Salvar Snapshot", command=self.snapshot, fg_color="teal")
                self.btn_snapshot.pack(anchor='center', side='right', pady=10)
            else:
                self.btn_snapshot = CTk.CTkButton(self, text="Ligar/Desligar", command=self.start_stop, fg_color="teal")
                self.btn_snapshot.pack(anchor='center', side='top', pady=10)

        self.image = None

    def initialize_driver(self):
        if self.isWebCam:
            self.vid = WebcamCapture(self.video_source, self.width, self.height)
        else:
            self.vid = VideoCapture(self.video_source, self.width, self.height)

        # After it is called once, the update method will be automatically called every delay milliseconds
        # calculate delay using `FPS`
        self.delay = int(1000 / self.vid.fps)

        print('[tkCamera] source:', self.video_source)
        print('[tkCamera] fps:', self.vid.fps, 'delay:', self.delay)

        self.running = True
        self.update_frame()

    def start_stop(self):
        if not self.running:
            self.running = True
            self.update_frame()
        else:
            self.running = False

    def snapshot(self):
        # Get a frame from the video source
        # ret, frame = self.vid.get_frame()
        # if ret:
        #    cv2.imwrite(time.strftime("frame-%d-%m-%Y-%H-%M-%S.jpg"), cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR))

        # Save current frame in widget - not get new one from camera - so it can save correct image when it stoped
        if self.image:
            self.image.save(time.strftime("frame-%d-%m-%Y-%H-%M-%S.jpg"))

    def update_frame(self):
        # widgets in tkinter already have method `update()` so I have to use different name -

        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.image = Image.fromarray(frame)
            self.photo = ImageTk.PhotoImage(image=self.image)
            self.canvas.create_image(0, 0, image=self.photo, anchor='nw')

        if self.running:
            self.window.after(self.delay, self.update_frame)

    def close_driver(self):
        self.vid.running = False
        self.vid.release_video()
        cv2.destroyAllWindows()
