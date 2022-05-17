import cv2
import mediapipe as mp
import triangulation_media_pipe as tmp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

change_face = 'jim_carrey.jpg'


def load_base_img(face_mesh, image_file_name):
    image = cv2.imread(image_file_name)
    landmarks = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    return {'img': image, 'landmarks': landmarks}


def transform_landmarks_from_tf_to_ocv(keypoints, face_width, face_height):
    landmark_list = []
    if keypoints.multi_face_landmarks is not None:
        for face_landmarks in keypoints.multi_face_landmarks:
            for lm in face_landmarks.landmark:
                # print(l.x, l.y, l.z)
                pt = mp_drawing._normalized_to_pixel_coordinates(lm.x, lm.y, face_width, face_height)
                landmark_list.append(pt)
    return landmark_list


def draw_triangulated_mesh(ocv_keypoints, img):
    for i in range(len(tmp.TRIANGULATION) // 3):
        result1 = ocv_keypoints[tmp.TRIANGULATION[i * 3]]
        result2 = ocv_keypoints[tmp.TRIANGULATION[i * 3 + 1]]
        result3 = ocv_keypoints[tmp.TRIANGULATION[i * 3 + 2]]
        cv2.line(img, result1, result2, 255)
        cv2.line(img, result2, result3, 255)
        cv2.line(img, result3, result1, 255)
    return img


def process_base_face_mesh(drawing_spec,
                           face_mesh,
                           image_file,
                           show_landmarks=False,
                           show_triangulated_mesh=False):
    base_face_handler = load_base_img(face_mesh, image_file)
    base_input_image = base_face_handler['img'].copy()
    image_rows, image_cols, _ = base_face_handler['img'].shape
    landmark_base_ocv = transform_landmarks_from_tf_to_ocv(base_face_handler['landmarks'], image_cols, image_rows)
    if show_landmarks:
        mp_drawing.draw_landmarks(
            image=base_face_handler['img'],
            landmark_list=base_face_handler['landmarks'].multi_face_landmarks[0],
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=drawing_spec,
            connection_drawing_spec=drawing_spec)
    if show_triangulated_mesh:
        base_face_handler['img'] = draw_triangulated_mesh(landmark_base_ocv, base_face_handler['img'])
    return landmark_base_ocv, base_input_image


def process_target_face_mesh(face_mesh,
                             webcam_img):
    image_rows, image_cols, _ = webcam_img.shape
    webcam_img.flags.writeable = False
    results = face_mesh.process(webcam_img)
    landmark_target_ocv = transform_landmarks_from_tf_to_ocv(results, image_cols, image_rows)
    webcam_img.flags.writeable = True
    target_input_image = webcam_img.copy()
    return landmark_target_ocv, target_input_image, results.multi_face_landmarks


def swap_faces(landmark_base_ocv, landmark_target_ocv, base_input_image, target_input_image):
    seam_clone = target_input_image.copy()
    img2_gray = cv2.cvtColor(target_input_image, cv2.COLOR_BGR2GRAY)
    img2_new_face = np.zeros_like(target_input_image)

    points2 = np.array(landmark_target_ocv, np.int32)
    convexhull2 = cv2.convexHull(points2)

    for i in range(len(tmp.TRIANGULATION) // 3):
        triangle_index = [tmp.TRIANGULATION[i * 3],
                          tmp.TRIANGULATION[i * 3 + 1],
                          tmp.TRIANGULATION[i * 3 + 2]]
        tbas1 = landmark_base_ocv[triangle_index[0]]
        tbas2 = landmark_base_ocv[triangle_index[1]]
        tbas3 = landmark_base_ocv[triangle_index[2]]
        triangle1 = np.array([tbas1, tbas2, tbas3], np.int32)

        rect1 = cv2.boundingRect(triangle1)
        (x, y, w, h) = rect1
        cropped_triangle = base_input_image[y: y + h, x: x + w]
        cropped_tr1_mask = np.zeros((h, w), np.uint8)

        points = np.array([[tbas1[0] - x, tbas1[1] - y],
                           [tbas2[0] - x, tbas2[1] - y],
                           [tbas3[0] - x, tbas3[1] - y]], np.int32)

        cv2.fillConvexPoly(cropped_tr1_mask, points, 255)
        ttar1 = landmark_target_ocv[triangle_index[0]]
        ttar2 = landmark_target_ocv[triangle_index[1]]
        ttar3 = landmark_target_ocv[triangle_index[2]]

        triangle2 = np.array([ttar1, ttar2, ttar3], np.int32)

        rect2 = cv2.boundingRect(triangle2)
        (x, y, w, h) = rect2

        cropped_tr2_mask = np.zeros((h, w), np.uint8)

        points2 = np.array([[ttar1[0] - x, ttar1[1] - y],
                            [ttar2[0] - x, ttar2[1] - y],
                            [ttar3[0] - x, ttar3[1] - y]], np.int32)

        cv2.fillConvexPoly(cropped_tr2_mask, points2, 255)
        # Warp triangles
        points = np.float32(points)
        points2 = np.float32(points2)
        M = cv2.getAffineTransform(points, points2)
        warped_triangle = cv2.warpAffine(cropped_triangle, M, (w, h))
        warped_triangle = cv2.bitwise_and(warped_triangle, warped_triangle, mask=cropped_tr2_mask)

        # Reconstructing destination face
        img2_new_face_rect_area = img2_new_face[y: y + h, x: x + w]
        img2_new_face_rect_area_gray = cv2.cvtColor(img2_new_face_rect_area, cv2.COLOR_BGR2GRAY)
        _, mask_triangles_designed = cv2.threshold(img2_new_face_rect_area_gray, 1, 255,
                                                   cv2.THRESH_BINARY_INV)
        warped_triangle = cv2.bitwise_and(warped_triangle, warped_triangle,
                                          mask=mask_triangles_designed)

        img2_new_face_rect_area = cv2.add(img2_new_face_rect_area, warped_triangle)
        img2_new_face[y: y + h, x: x + w] = img2_new_face_rect_area
    # Face swapped (putting 1st face into 2nd face)
    img2_face_mask = np.zeros_like(img2_gray)
    img2_head_mask = cv2.fillConvexPoly(img2_face_mask, convexhull2, 255)
    img2_face_mask = cv2.bitwise_not(img2_head_mask)

    img2_head_noface = cv2.bitwise_and(seam_clone, seam_clone, mask=img2_face_mask)
    result = cv2.add(img2_head_noface, img2_new_face)

    (x, y, w, h) = cv2.boundingRect(convexhull2)
    center_face2 = (int((x + x + w) / 2), int((y + y + h) / 2))
    seamless_clone = cv2.seamlessClone(result, seam_clone, img2_head_mask, center_face2, cv2.MIXED_CLONE)

    return result, seamless_clone


def main():
    key_draw_landmarks = True
    flag_change_face = False

    # For webcam input:
    face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

    landmark_base_ocv, base_input_image = process_base_face_mesh(drawing_spec, face_mesh, change_face,
                                                                 show_landmarks=key_draw_landmarks,
                                                                 show_triangulated_mesh=key_draw_landmarks)

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        success, webcam_img = cap.read()
        if not success:
            continue
        if flag_change_face:
            landmark_base_ocv, base_input_image = process_base_face_mesh(drawing_spec, face_mesh, change_face,
                                                                         show_landmarks=key_draw_landmarks,
                                                                         show_triangulated_mesh=key_draw_landmarks)
            flag_change_face = False

        landmark_target_ocv, target_input_image, multi_face_landmarks = process_target_face_mesh(face_mesh, webcam_img)
        out_image = webcam_img.copy()

        if multi_face_landmarks is not None:
            for face_landmarks in multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=out_image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=drawing_spec,
                    connection_drawing_spec=drawing_spec)
                out_image = draw_triangulated_mesh(landmark_target_ocv, out_image)

                if len(landmark_target_ocv) > 0:
                    print(len(landmark_target_ocv[0]))
                    for i, elem in enumerate(landmark_target_ocv):
                        if len(elem) != 2:
                            print(i)

                    seam_clone, seamless_clone = swap_faces(landmark_base_ocv, landmark_target_ocv,
                                                            base_input_image, target_input_image)

        cv2.imshow('input', out_image)
        cv2.imshow('seam', seam_clone)
        cv2.imshow('seamless', seamless_clone)
        key = cv2.waitKey(5)
        if key == 27:
            break

    face_mesh.close()
    cap.release()


if __name__ == '__main__':
    main()
