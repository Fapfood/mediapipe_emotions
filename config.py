from face_swapping import mp_face_mesh, mp_drawing, create_config

face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_faces=3)
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

config_man1 = create_config(face_mesh, drawing_spec, 'Boy')
config_man2 = create_config(face_mesh, drawing_spec, 'men')
config_man3 = create_config(face_mesh, drawing_spec, 'OldMen')
config_woman1 = create_config(face_mesh, drawing_spec, 'girl')
config_woman2 = create_config(face_mesh, drawing_spec, 'womanl')
config_woman3 = create_config(face_mesh, drawing_spec, 'Grandma')
configs = {1: config_man1, 2: config_man2, 3: config_man3, 'mode': 'none'}


def seam():
    configs['mode'] = 'seam'


def seamless():
    configs['mode'] = 'seamless'


def none():
    configs['mode'] = 'none'


def user3_man():
    configs[3] = config_man3


def user3_woman():
    configs[3] = config_woman3


def user2_man():
    configs[2] = config_man2


def user2_woman():
    configs[2] = config_woman2


def user1_man():
    configs[1] = config_man1


def user1_woman():
    configs[1] = config_woman1
