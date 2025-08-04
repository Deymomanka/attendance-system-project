from PIL import Image, ImageDraw, ImageFont
import cv2
import face_recognition
import numpy as np
import os
import sqlite3
from datetime import datetime


def init_db(db_path):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # 新しいデータベースを作らない。「IF NOT EXISTS attendance」の時のみ作成
    c.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            status TEXT,
            time TEXT )
''')
    conn.commit()
    conn.close()

def get_last_status(db_path, name):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # 新しいデータベースを作らない。「IF NOT EXISTS attendance」の時のみ作成
    c.execute("SELECT status from attendance WHERE name = ? ORDER BY id DESC LIMIT 1", (name,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def insert_attendance(db_path, name, status):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO attendance (name, status, time) VALUES (?, ?, ?)", (name, status, now))
    conn.commit()
    conn.close()
    print(f"DB記録：{name}, {status}, {now}")



def load_known_faces(image_folder):
    known_face_encodings = []
    known_face_names = []
    for file_name in os.listdir(image_folder):
        if file_name.endswith((".jpg", ".png")):
            image_path = os.path.join(image_folder, file_name)
            image = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encodings(image)  # どういうふうにencodingを行っているか
            if encoding:
                known_face_encodings.append(encoding[0])
                # 例えば、file_nameは　「Tanaka Rin.jpg」のとき、encoding[0]　＝＞　Tanaka Rin。encoding[1]＝＞ .jpg
                known_face_names.append(os.path.splitext(file_name)[0])  
                print(f"顔をロード：{file_name}")
            else:
                print(f"顔が検出できなかった：{file_name}")
    return known_face_encodings, known_face_names


def main():

    db_path = "logs/attendance.db"
    image_folder="images/"
    init_db(db_path)
    known_face_encodings, known_face_names = load_known_faces(image_folder)
    video_capture = cv2.VideoCapture(0)  # どのカメラに接続するか指定する・選択する｜カメラのオブジェクト名

    recognized_users = set()

    while True:
        ret, frame = video_capture.read()  # カメラの画像取得：retは、画像取得が成功したかどうか（True/False）。frameは、カメラから取得した画像データが格納される。　
        if not ret:
            print("カメラが取得できませでした")
            break

        frame = cv2.flip(frame, 1) # 左右反転

        rgb_frame = np.ascontiguousarray(frame[:, :, ::-1])
        face_locations = face_recognition.face_locations(rgb_frame)  # 顔の場所（位置）を検出している

        for face_location in face_locations:
            encodings = face_recognition.face_encodings(rgb_frame, [face_location])
            if len(encodings) == 0:
                continue
            face_encodings = encodings[0]
        
        # 1フレームで検出した顔分をループする
            #matches = face_recognition.compare_faces(known_face_encodings, face_encodings, tolerance=0.5) # tolerance=0.5 は適合度みたいな、顔認識の許容範囲、どれだけマッチしていればおっけとみなすか
            matches = face_recognition.compare_faces(known_face_encodings, face_encodings) 
            face_distances = face_recognition.face_distance(known_face_encodings, face_encodings) # カメラの感覚のdistances
            best_match_index = np.argmin(face_distances)
            name = "Unknown"

            if matches[best_match_index]:
                name = known_face_names[best_match_index]

                if name not in recognized_users:
                    last_status = get_last_status(db_path, name)
                    next_status = "退勤" if last_status == "出勤" else "出勤"
                    insert_attendance(db_path, name, next_status)
                    recognized_users.add(name)

            
            # 日本語描画
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb )
            draw = ImageDraw.Draw(pil_image)
            font = ImageFont.truetype("fonts/Arial Unicode.ttf", 30)

            # テキストを中央に置く
            text = f"おはようございます、{name}"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            image_width, image_height = pil_image.size
            x = (image_width - text_width) // 2
            y = (image_height - text_height) // 6

            draw.text((x, y), text, font=font, fill=(0,0,255)) # fill=(0,0,255) : 色を変える部分
            frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

            cv2.imshow('Face Attendance', frame)
            if cv2.waitKey(1) & 0xFF == ord('r'):
                recognized_users.clear()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
            
