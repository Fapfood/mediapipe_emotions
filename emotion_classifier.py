import math
import statistics


def classify(points):  # keypoints.multi_face_landmarks[x].landmark:
    # print('nose_length', nose_length(points))
    # print('inner_eyebrows', inner_eyebrows(points))
    # print('mouth_openness', mouth_openness(points))
    # print('chin', chin(points))
    # print('mouth_width', mouth_width(points))
    # print('mouth_corners', mouth_corners(points))
    # print('top_of_eyebrows', top_of_eyebrows(points))
    if top_of_eyebrows(points) < 0.79:
        if mouth_openness(points) > 0.2:
            return 'disgust'
        else:
            return 'anger'
    elif top_of_eyebrows(points) > 0.91 or mouth_openness(points) > 0.2 or chin(points) > 1.2:
        if mouth_width(points) > 0.64:
            return 'fear'
        else:
            return 'surprise'
    elif mouth_corners(points) > 1.30:
        return 'sadness'
    elif mouth_corners(points) < 1.15:
        return 'happiness'
    else:
        return 'unknown'


def normalize_distance(points, distance):
    right = get_point(points, 33)
    left = get_point(points, 263)
    scale_distance = get_distance(left, right)
    return distance / scale_distance


def get_point(points, index):
    point = points[index]
    return [point.x, point.y, point.z]


def get_distance(point1, point2):
    return math.dist(point1, point2)


def get_mean(distances):
    return statistics.mean(distances)


def top_of_eyebrows(points):
    eyebrow_left = get_point(points, 334)
    eyebrow_right = get_point(points, 105)
    nose_right = get_point(points, 129)
    nose_left = get_point(points, 358)
    distances = [get_distance(eyebrow_left, nose_left), get_distance(eyebrow_right, nose_right)]
    distance = get_mean(distances)
    return normalize_distance(points, distance)


def inner_eyebrows(points):
    left = get_point(points, 336)
    right = get_point(points, 107)
    nose = get_point(points, 1)
    distances = [get_distance(left, nose), get_distance(right, nose)]
    distance = get_mean(distances)
    return normalize_distance(points, distance)


def mouth_corners(points):
    eyebrow_left = get_point(points, 334)
    eyebrow_right = get_point(points, 105)
    mouth_left = get_point(points, 291)
    mouth_right = get_point(points, 61)
    distances = [get_distance(eyebrow_left, mouth_left), get_distance(eyebrow_right, mouth_right)]
    distance = get_mean(distances)
    return normalize_distance(points, distance)


def chin(points):
    down = get_point(points, 152)
    nose = get_point(points, 1)
    distance = get_distance(down, nose)
    return normalize_distance(points, distance)


def mouth_width(points):
    left = get_point(points, 291)
    right = get_point(points, 61)
    distance = get_distance(left, right)
    return normalize_distance(points, distance)


def mouth_openness(points):
    top = get_point(points, 13)
    down = get_point(points, 14)
    distance = get_distance(top, down)
    return normalize_distance(points, distance)


def nose_length(points):
    top = get_point(points, 8)
    nose = get_point(points, 1)
    distance = get_distance(top, nose)
    return normalize_distance(points, distance)


def left_eye_openness(points):
    top_inner = get_point(points, 385)
    down_inner = get_point(points, 380)
    top_outer = get_point(points, 387)
    down_outer = get_point(points, 373)
    distances = [get_distance(top_inner, down_inner), get_distance(top_outer, down_outer)]
    distance = get_mean(distances)
    return normalize_distance(points, distance)


def right_eye_openness(points):
    top_inner = get_point(points, 158)
    down_inner = get_point(points, 153)
    top_outer = get_point(points, 160)
    down_outer = get_point(points, 144)
    distances = [get_distance(top_inner, down_inner), get_distance(top_outer, down_outer)]
    distance = get_mean(distances)
    return normalize_distance(points, distance)
