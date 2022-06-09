import io

from flask import Flask, request
from retinaface import RetinaFace
import s3_connection
from PIL import Image
import numpy as np


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello'


@app.route('/api/profile', methods=['POST'])
def detect_face_from_profile():

    # 업로드한 프로필 사진 읽어옴
    req_json = request.get_json()
    profile_img_url = req_json['profile_img_url']
    print("profile_img_url:", profile_img_url)
    profile_img = s3_connection.read_s3_images(profile_img_url)

    # 프로필 사진에서 얼굴 추출
    np_img = np.array(profile_img)
    profile_face_list = RetinaFace.extract_faces(np_img)

    if len(profile_face_list) > 1:
        return "인식된 얼굴이 하나 이상입니다."

    if len(profile_face_list) == 0:
        return "인식된 얼굴이 없습니다."

    # 추출된 얼굴 이미지 업로드
    img = Image.fromarray(profile_face_list[0]).convert('RGB')
    out_img = io.BytesIO()
    img.save(out_img, format='png')
    out_img.seek(0)
    s3_connection.upload_image(out_img, profile_img_url, 'profile_face')

    return "얼굴 추출 및 저장 완료"


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)