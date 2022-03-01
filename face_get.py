"""
第一引数：opencvの特徴ファイル（/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_alt.xml　など）
第二引数：画像ファイルのパス（/*で指定するのがいい）
アニメだからなのか「エウレカセブン」の検索結果でやると精度が低い印象を受ける。てか画像ピクセルが小さすぎる。現状ではあまり使い道を見いだせない。
"""

import sys
import os
import cv2
# import numpy

try:
    casacde_path = sys.argv[1]
except IndexError:
    print('Usage: python face_get.py CASCADSE_PATH IMAGE_PATH...', file=sys.stderr)
    exit(1)

output_dir = 'faces'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

assert os.path.exists(casacde_path)

classifier = cv2.CascadeClassifier(casacde_path)

for image_path in sys.argv[2:]:
    print('Processing', image_path, file=sys.stderr)

    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = classifier.detectMultiScale(gray_image)

    image_name = os.path.splitext(os.path.basename(image_path))[0]

    for i, (x, y, w, h) in enumerate(faces):
        face_image = image[y:y+h, x:x+w]
        output_path = os.path.join(output_dir, '{0}_{1}.jpg'.format(image_name, i))
        cv2.imwrite(output_path, face_image)