import math
import statistics


def classify(points):  # keypoints.multi_face_landmarks[x].landmark:
    if nose_length(points) < 0.52 or inner_eyebrows(points) < 0.82:
        if mouth_openness(points) > 0.05:
            return 'disgust'
        else:
            return 'anger'
    elif mouth_openness(points) > 0.1 or chin(points) > 1.5:
        if mouth_width(points) > 0.8:
            return 'fear'
        else:
            return 'surprise'
    elif mouth_corners(points) > 0.55:
        return 'sadness'
    elif mouth_corners(points) < 0.45:
        return 'happiness'
    else:
        return 'unknown'


#   def rotate_points()
#   def shift_points()
#   def scale_points()

def get_point(points, index):
    point = points[index]
    return [point.x, point.y, point.z]


def get_distance(point1, point2):
    return math.dist(point1, point2)


def get_mean(distances):
    return statistics.mean(distances)


def top_of_eyebrows(points):
    left = get_point(points, 334)
    right = get_point(points, 105)
    nose = get_point(points, 1)
    distances = [get_distance(left, nose), get_distance(right, nose)]
    return get_mean(distances)


def inner_eyebrows(points):
    left = get_point(points, 336)
    right = get_point(points, 107)
    nose = get_point(points, 1)
    distances = [get_distance(left, nose), get_distance(right, nose)]
    return get_mean(distances)


def mouth_corners(points):
    left = get_point(points, 291)
    right = get_point(points, 61)
    nose = get_point(points, 1)
    distances = [get_distance(left, nose), get_distance(right, nose)]
    return get_mean(distances)


def chin(points):
    down = get_point(points, 152)
    nose = get_point(points, 1)
    distance = get_distance(down, nose)
    return distance


def mouth_width(points):
    left = get_point(points, 291)
    right = get_point(points, 61)
    distance = get_distance(left, right)
    return distance


def mouth_openness(points):
    top = get_point(points, 13)
    down = get_point(points, 14)
    distance = get_distance(top, down)
    return distance


def nose_length(points):
    top = get_point(points, 8)
    nose = get_point(points, 1)
    distance = get_distance(top, nose)
    return distance


def left_eye_openness(points):
    top_inner = get_point(points, 385)
    down_inner = get_point(points, 380)
    top_outer = get_point(points, 387)
    down_outer = get_point(points, 373)
    distances = [get_distance(top_inner, down_inner), get_distance(top_outer, down_outer)]
    return get_mean(distances)


def right_eye_openness(points):
    top_inner = get_point(points, 158)
    down_inner = get_point(points, 153)
    top_outer = get_point(points, 160)
    down_outer = get_point(points, 144)
    distances = [get_distance(top_inner, down_inner), get_distance(top_outer, down_outer)]
    return get_mean(distances)
