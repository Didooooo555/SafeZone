# TIME+FOLDER (mvp+)
import cv2
import numpy as np
from ultralytics import YOLO
import os
import time

# 🔹 Путь к модели
model_path = "yolov8n-face.pt"
model = YOLO(model_path)

# 🔹 Папка для сохранения
folder_name = "mask"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

counter = 0
mask_start_time = None
saved_first = False
saved_3sec = False

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

    results = model.predict(frame, conf=0.5, verbose=False)

    mask_detected = False

    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()

        for box in boxes:
            x1, y1, x2, y2 = box.astype(int)

            # 🔹 Защита от выхода за границы кадра
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(frame.shape[1], x2)
            y2 = min(frame.shape[0], y2)

            face_roi = frame[y1:y2, x1:x2]

            if face_roi.size == 0:
                continue

            h = face_roi.shape[0]
            lower_face = face_roi[h//2:h, :, :]

            # Было: avg_color = np.mean(lower_face, axis=(0, 1))
            # Чтобы сравнение было корректным, берем яркость (среднее по всем каналам)
            avg_brightness = float(np.mean(lower_face))

            # 🔹 Простая эвристика (ИСПРАВЛЕНО: теперь "Mask" там, где по твоей камере должно быть)
            # Было: if np.mean(avg_color) < 120:
            if avg_brightness > 120:
                label = "Mask"
                color = (0, 0, 255)
                mask_detected = True

                # Если маска только появилась
                if mask_start_time is None:
                    mask_start_time = time.time()
                    saved_first = False
                    saved_3sec = False

                elapsed = time.time() - mask_start_time

                # 📸 Первое фото
                if not saved_first:
                    counter += 1
                    filename = os.path.join(folder_name, f"mask_{counter}.jpg")
                    cv2.imwrite(filename, face_roi)
                    print(f"[INFO] Сохранено первое фото: {filename}")
                    saved_first = True

                # 📸 Фото после 3 секунд
                if elapsed >= 3 and not saved_3sec:
                    counter += 1
                    filename = os.path.join(folder_name, f"mask_{counter}_3sec.jpg")
                    cv2.imwrite(filename, face_roi)
                    print(f"[INFO] Сохранено фото после 3 сек: {filename}")
                    saved_3sec = True

            else:
                label = "No Mask"
                color = (0, 255, 0)

            # Рисуем рамку
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    # Если маска пропала — сбрасываем таймер
    if not mask_detected:
        mask_start_time = None
        saved_first = False
        saved_3sec = False

    cv2.imshow("Mask Detection MVP", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()