import cv2

rtmp_url = "rtmp://localhost/live/test"

cap = cv2.VideoCapture(rtmp_url)

if not cap.isOpened():
    print("RTMP akışı açılamadı.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Kare alınamadı.")
        break

    cv2.imshow("RTMP Yayını", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
