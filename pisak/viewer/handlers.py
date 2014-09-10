from pisak import signals
from pisak.viewer import database_agent, image


@signals.registered_handler("viewer/next_page")
def next_page(pager):
    pager.flip()


@signals.registered_handler("viewer/previous_page")
def previous_page(pager):
    pager.previous_page()


@signals.registered_handler("viewer/slideshow_toggle")
def slideshow_toggle(slideshow_widget):
    if slideshow_widget.slideshow_on is True:
        slideshow_widget.stop()
    else:
        slideshow_widget.run()


@signals.registered_handler("viewer/next_slide")
def next_slide(slideshow_widget):
    slideshow_widget.next_slide()


@signals.registered_handler("viewer/previous_slide")
def previous_slide(slideshow_widget):
    slideshow_widget.previous_slide()


@signals.registered_handler("viewer/add_to_favourite_photos")
def add_to_favourite_photos(slideshow_widget):
    path = slideshow_widget.slide.photo_path
    album = slideshow_widget.data_source.data[slideshow_widget.index]["category"]
    database_agent.add_to_favourite_photos(path, album)
    

@signals.registered_handler("viewer/zoom")
def zoom(slide_space):
    slide = slide_space.get_children()[0]
    if slide.image_buffer is not None:
        slide.image_buffer.zoom()
    else:
        slide.image_buffer = image.ImageBuffer()
        slide.image_buffer.zoom()


@signals.registered_handler("viewer/contour")
def contour(slide_space):
    slide = slide_space.get_children()[0]
    if slide.image_buffer is not None:
        slide.image_buffer.contour()
    else:
        slide.image_buffer = image.ImageBuffer()
        slide.image_buffer.contour()


@signals.registered_handler("viewer/edges")
def edges(slide_space):
    slide = slide_space.get_children()[0]
    if slide.image_buffer is not None:
        slide.image_buffer.edges()
    else:
        slide.image_buffer = image.ImageBuffer()
        slide.image_buffer.edges()


@signals.registered_handler("viewer/sepia")
def sepia(slide_space):
    slide = slide_space.get_children()[0]
    if slide.image_buffer is not None:
        slide.image_buffer.sepia()
    else:
        slide.image_buffer = image.ImageBuffer()
        slide.image_buffer.sepia()
        

@signals.registered_handler("viewer/invert")
def invert(slide_space):
    slide = slide_space.get_children()[0]
    if slide.image_buffer is not None:
        slide.image_buffer.invert()
    else:
        slide.image_buffer = image.ImageBuffer()
        slide.image_buffer.invert()


@signals.registered_handler("viewer/rotate")
def rotate(slide_space):
    slide = slide_space.get_children()[0]
    if slide.image_buffer is not None:
        slide.image_buffer.rotate()
    else:
        slide.image_buffer = image.ImageBuffer()
        slide.image_buffer.rotate()


@signals.registered_handler("viewer/mirror")
def mirror(slide_space):
    slide = slide_space.get_children()[0]
    if slide.image_buffer is not None:
        slide.image_buffer.mirror()
    else:
        slide.image_buffer = image.ImageBuffer()
        slide.image_buffer.mirror()


@signals.registered_handler("viewer/grayscale")
def grayscale(slide_space):
    slide = slide_space.get_children()[0]
    if slide.image_buffer is not None:
        slide.image_buffer.grayscale()
    else:
        slide.image_buffer = image.ImageBuffer()
        slide.image_buffer.grayscale()


@signals.registered_handler("viewer/noise")
def noise(slide_space):
    slide = slide_space.get_children()[0]
    if slide.image_buffer is not None:
        slide.image_buffer.noise()
    else:
        slide.image_buffer = image.ImageBuffer()
        slide.image_buffer.noise()


@signals.registered_handler("viewer/solarize")
def solarize(slide_space):
    slide = slide_space.get_children()[0]
    if slide.image_buffer is not None:
        slide.image_buffer.solarize()
    else:
        slide.image_buffer = image.ImageBuffer()
        slide.image_buffer.solarize()


@signals.registered_handler("viewer/original")
def original(slide_space):
    slide = slide_space.get_children()[0]
    if slide.image_buffer is not None:
        slide.image_buffer.original()
    else:
        slide.image_buffer = image.ImageBuffer()
        slide.image_buffer.original()
