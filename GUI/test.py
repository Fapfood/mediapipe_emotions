
from kivy.uix.image import Image
from kivy.core.camera import Camera as CoreCamera
from kivy.properties import NumericProperty, ListProperty, BooleanProperty

# access to camera
core_camera = CoreCamera(resolution=(640, 480), stopped=True)

# Widget to display camera
class MyCamera(Image):

    play = BooleanProperty(True)
    index = NumericProperty(-1)
    resolution = ListProperty([-1, -1])


    def __init__(self, **kwargs):
        self._camera = None
        super(MyCamera, self).__init__(**kwargs)  # `MyCamera` instead of `Camera`
        if self.index == -1:
            self.index = 0
        on_index = self._on_index
        fbind = self.fbind
        fbind('index', on_index)
        fbind('resolution', on_index)
        on_index()

    def on_tex(self, *l):
        self.canvas.ask_update()

    def _on_index(self, *largs):
        self._camera = None
        if self.index < 0:
            return
        if self.resolution[0] < 0 or self.resolution[1] < 0:
            return

        self._camera = core_camera

        self._camera.bind(on_load=self._camera_loaded)
        if self.play:
            self._camera.start()
            self._camera.bind(on_texture=self.on_tex)

    def _camera_loaded(self, *largs):
        self.texture = self._camera.texture
        self.texture_size = list(self.texture.size)

    def on_play(self, instance, value):
        if not self._camera:
            return
        if value:
            self._camera.start()
        else:
            self._camera.stop()


from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import time

Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    MyCamera:
        id: camera1
        resolution: (640, 480)
    MyCamera:
        id: camera2
        resolution: (640, 480)
    
''')


class CameraClick(BoxLayout):
    def capture(self):
       pass

class TestCamera(App):

    def build(self):
        return CameraClick()

if __name__ == '__main__':
    TestCamera().run()
