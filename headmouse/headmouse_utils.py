from scipy.spatial import distance as dist
from dlib import rectangle

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def get_closest_face(rects: rectangle)-> rectangle: 
    closest = 0
    for index, rect in enumerate(rects):
        if rect.area() > rects[closest].area():
            closest = index
    return rects[closest]

def eye_processing(eye, counter):
    ear_consec_frames = 4
    ear_thresh = 0.2
    has_winked = False
    ear = eye_aspect_ratio(eye)
    if ear < ear_thresh:
        counter += 1
    else:
        if counter >= ear_consec_frames:
            has_winked = True
        counter = 0
    return [has_winked, counter]
