import cv2
import numpy as np
from tqdm import tqdm


def merge_images(image1, image2):

    combined_image = np.zeros((max(image1.shape[0], image2.shape[0]), image1.shape[1] + image2.shape[1], 3), dtype=np.uint8)
    # Place the images on the combined image
    combined_image[0:image1.shape[0], 0:image1.shape[1]] = image1
    combined_image[0:image2.shape[0], image1.shape[1]:image1.shape[1] + image2.shape[1]] = image2

    return combined_image


def add_text(frame, text):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.4
    text_color = (255, 255, 255)
    thickness = 1
    strip_height = 40

    extended_image = np.ones((frame.shape[0] + strip_height, frame.shape[1], 3), dtype=np.uint8) * 0
    extended_image[strip_height:, :] = frame
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    x_center = (frame.shape[1] - text_width) // 2
    position = (x_center, strip_height - 10)

    cv2.putText(extended_image, text, position, font, font_scale, text_color, thickness, cv2.LINE_AA)

    return extended_image


def make_video(frames, output_path):
    size = frames[0].shape[1], frames[0].shape[0]
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'MP4V'), 25, size)
    for img in tqdm(frames, total=len(frames), desc="Processing Frames"):
        out.write(img)
    out.release()
    del out