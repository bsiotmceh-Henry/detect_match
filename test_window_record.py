import numpy as np
import cv2
from keras.models import load_model
from PIL import Image, ImageOps, ImageGrab

# image = ImageGrab.grab()
# width, height = image.size

# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# video = cv2.VideoWriter('test.avi', fourcc, 25, (width, height))

model = load_model('x.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)


def cross_detect(image):

    # resize to 224, 224
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    # 轉換成np數組
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array

    # 進行辨識
    prediction = model.predict(data)
    print(prediction)

    x, not_x, skip = prediction[0]
    if x > 0.8:
        print("x!")
    elif skip > 0.8:
        print("skip!")
    

while True:
    # img_rgb = ImageGrab.grab()
    img_rgb = ImageGrab.grab(bbox = (300, 300, 360, 360))
    img_bgr = cv2.cvtColor(np.array(img_rgb), cv2.COLOR_RGB2BGR)
    # video.write(img_bgr)
    # cross_detect(img_rgb)
    cv2.imshow('imm', img_bgr)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# video.release()
cv2.destroyAllWindows()