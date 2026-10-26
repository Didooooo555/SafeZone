#ONLY CAMERA AND DETEC (mvp)
import cv2
import numpy as np
from ultralytics import YOLO

# 🔹 Путь к твоей модели
model_path = "yolov8n-face.pt"
model = YOLO(model_path)

# 🔹 Запуск камеры
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Ошибка: не удалось открыть камеру")
    exit()

print("Камера запущена. Нажмите 'q' чтобы выйти.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 🔹 Детекция лиц через YOLO
    results = model.predict(frame)

    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()  # [x1, y1, x2, y2]
        scores = result.boxes.conf.cpu().numpy()  # вероятность
        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = box.astype(int)
            score = scores[i]

            # 🔹 Вырезаем лицо из кадра
            face_roi = frame[y1:y2, x1:x2]

            # 🔹 Простейшая проверка маски
            # Метод: проверяем средний цвет нижней части лица
            if face_roi.size > 0:
                h = y2 - y1
                lower_face = face_roi[h//2:h, :, :]
                avg_color = np.mean(lower_face, axis=(0,1))

                # Простейшая эвристика: если слишком светлое = нет маски
                if np.mean(avg_color) < 120:
                    label = "Mask"
                    color = (0,0,255)  # красный
                else:
                    label = "No Mask"
                    color = (0,255,0)  # зеленый

                # Рисуем рамку и подпись
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    # 🔹 Отображение кадра
    cv2.imshow("Mask Detection MVP", frame)

    # 🔹 Выход по клавише 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
