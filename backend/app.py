from flask import Flask, Response, render_template
import cv2
import threading

app = Flask(__name__)

# RTMP
RTMP_URL = "rtmp://localhost/live/test"

# Haar cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


class VideoStream:
    def __init__(self, url):
        self.cap = cv2.VideoCapture(url)
        self.frame = None
        self.stopped = False
        self.lock = threading.Lock()

        if self.cap.isOpened():
            thread = threading.Thread(target=self.update, daemon=True)
            thread.start()

    def update(self):
        while not self.stopped:
            ret, frame = self.cap.read()
            if not ret:
                continue

            frame = cv2.resize(frame, (640, 360))  
            with self.lock:
                self.frame = frame

    def read(self):
        with self.lock:
            return self.frame.copy() if self.frame is not None else None

    def stop(self):
        self.stopped = True
        self.cap.release()


video_stream = VideoStream(RTMP_URL)

def generate_frames():
    while True:
        frame = video_stream.read()
        if frame is None:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            # Kutu çiz
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Etiket yazısı çiz
            label_y = y - 10 if y - 10 > 10 else y + 20
            cv2.putText(frame, "Face", (x, label_y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (0, 255, 0), 2, cv2.LINE_AA)

        success, buffer = cv2.imencode('.jpg', frame)
        if not success:
            continue
        frame = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
        )


@app.route("/")
def index():
    return render_template("live.html")


@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(debug=True)