import sys
from pisak import switcher_app
from gi.repository import Clutter, GObject, Mx, Gst, ClutterGst


class ButtonStage(Clutter.Stage):
    '''
    Clutter stage with single button in the center
    '''
    def __init__(self):
        ClutterGst.init()
        super().__init__()
        self.button = Mx.Button()
        self.button.set_label("Don't click")
        self.add_child(self.button)
        
        self.video_texture = ClutterGst.VideoTexture(**{"disable-slicing": True})
        self.add_child(self.video_texture)
        
        descriptor = "playbin uri=http://docs.gstreamer.com/media/sintel_trailer-480p.webm"
        self.pipeline = Gst.parse_launch(descriptor)
        
        self.clutter_sink = Gst.ElementFactory.make("autocluttersink")
        self.clutter_sink.set_property("texture", self.video_texture)
        self.pipeline.set_property("video-sink", self.clutter_sink)
        
        self.pipeline.set_state(Gst.State.PLAYING)
        
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)


class ButtonApp(switcher_app.Application):
    '''
    Simple app written for test purposes
    '''
    def create_stage(self, argv):
        return ButtonStage()
        

if __name__ == '__main__':
    ButtonApp(sys.argv).main()