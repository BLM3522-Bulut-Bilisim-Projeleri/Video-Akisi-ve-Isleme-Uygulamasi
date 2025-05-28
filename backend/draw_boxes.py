import cv2

def draw_bounding_boxes(video_path, labels, output_path="output_with_boxes.mp4"):
    cap = cv2.VideoCapture(video_path)

    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*"avc1")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_idx = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        timestamp = frame_idx / fps  

        for label in labels:
            if label["start_time"] <= timestamp <= label["end_time"]:
                box = label["bounding_box"]
                left   = int(box["left"] * width)
                top    = int(box["top"] * height)
                right  = int(box["right"] * width)
                bottom = int(box["bottom"] * height)

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, label["label"], (left, top - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        out.write(frame)
        frame_idx += 1

    cap.release()
    out.release()
    print("✅ Yeni video kaydedildi:", output_path)