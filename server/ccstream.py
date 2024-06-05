import cv2
import numpy as np
from sklearn.cluster import KMeans

RESOLUTION = (164, 81)


def display_cv_image(image):
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def resize_and_crop(image, target_width, target_height):
    original_height, original_width = image.shape[:2]

    target_ratio = target_width / target_height
    original_ratio = original_width / original_height

    if original_ratio > target_ratio:
        new_height = target_height
        new_width = int(target_height * original_ratio)
    else:
        new_width = target_width
        new_height = int(target_width / original_ratio)

    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

    x_center = new_width // 2
    y_center = new_height // 2
    x_crop_start = x_center - (target_width // 2)
    y_crop_start = y_center - (target_height // 2)

    cropped_image = resized_image[y_crop_start:y_crop_start + target_height, x_crop_start:x_crop_start + target_width]
    return cropped_image


def flatten_image(image):
    return image.reshape((-1, 3))


def unflatten_image(image, shape):
    return image.reshape(shape)


def get_palette(image, n_colors):
    arr = flatten_image(image)
    return KMeans(n_clusters=n_colors).fit(arr)


def map_palette(image, palette):
    arr = flatten_image(image)
    labels = palette.predict(arr)
    pal = palette.cluster_centers_[labels].astype('uint8')
    return unflatten_image(pal, image.shape)


def quantize(image, palette):
    arr = flatten_image(image)
    labels = palette.predict(arr)
    labels = labels.reshape(image.shape[:2]).tolist()
    labels = np.vectorize(lambda a: hex(a)[2])(labels)
    l = list(map(lambda a: ''.join(a), labels))
    return l


def palette_to_hex(palette):
    return [int(r) * 256 ** 2 + int(g) * 256 + int(b) for b, g, r in palette.cluster_centers_]


def get_image_from_webcam():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    return frame


def process_image(image):
    resized = resize_and_crop(image, *RESOLUTION)
    palette = get_palette(resized, 16)
    return map_palette(resized, palette), palette_to_hex(palette)


def process_image_to_chars(image):
    resized = resize_and_crop(image, *RESOLUTION)
    palette = get_palette(resized, 16)
    return quantize(resized, palette), palette_to_hex(palette)
