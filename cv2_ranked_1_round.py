import cv2
import numpy as np

from tqdm import tqdm
from typing import Union

def crop_frame_killfeed(frame: np.ndarray) -> np.ndarray:
    height = frame.shape[0]
    width = frame.shape[1]
    cropped_frame = frame[(height//24)*4:(height//24)*7, (width//32)*22:(width//32)*28]
    return cropped_frame


def opencv_box(frame: np.ndarray) -> Union[np.ndarray, None]:
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY)

    # contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    image_copy = frame.copy()
    # cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
    #
    # contours1, hierarchy1 = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    image_copy1 = frame.copy()
    # cv2.drawContours(image_copy1, contours1, -1, (0, 255, 0), 2, cv2.LINE_AA)

    # cv2.imwrite(f'ranked_1_round/{vid_name}_contours_none.jpg', image_copy)
    cv2.imwrite(f'ranked_1_round/{frame_number}_frame_original_{vid_name}.jpg', frame)
    cv2.imwrite(f'ranked_1_round/{frame_number}_frame_thresh_{vid_name}.jpg', thresh)
    # cv2.imwrite(f'ranked_1_round/{vid_name}_contours_simple.jpg', image_copy1)

    if debug:
        horizontal1 = np.concatenate((cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR), cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)), axis=1)
        horizontal2 = np.concatenate((image_copy, image_copy1), axis=1)
        vertical = np.concatenate((horizontal1, horizontal2), axis=0)
        return vertical
    else:
        return None


def show_comparison(frame: np.ndarray) -> None:
    cv2.imshow('Frame', frame)


debug = False
vid_path = 'videos/ranked_1_round.mp4'
vid_name = vid_path.split(sep='.')[0].split(sep='/')[1]

cap = cv2.VideoCapture(vid_path)
if (cap.isOpened()== False):
    print("Error opening video")
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_number = 0
skip_frames = 10
with tqdm(total=frame_count) as pbar:
    while(cap.isOpened()):
        frame_number += skip_frames
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        success, frame = cap.read()
        if success == True:
            frame = cv2.resize(frame, None, fx=2, fy=2, interpolation= cv2.INTER_LINEAR)
            cropped_frame = crop_frame_killfeed(frame=frame)
            comparison_frame = opencv_box(cropped_frame)
            if debug: show_comparison(frame=comparison_frame)
            if cv2.waitKey(20) & 0xFF == ord('q'): break
            pbar.update(skip_frames)
        else:
            pbar.update(frame_count - frame_number - skip_frames)
            break
cap.release()
cv2.destroyAllWindows()
