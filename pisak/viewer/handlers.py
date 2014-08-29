from pisak import signals


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


@signals.registered_handler("viewer/zoom")
def zoom(photo):
    photo.image_buffer.zoom()


@signals.registered_handler("viewer/contour")
def contour(photo):
    photo.image_buffer.contour()


@signals.registered_handler("viewer/edges")
def edges(photo):
    photo.image_buffer.edges()


@signals.registered_handler("viewer/sepia")
def sepia(photo):
    photo.image_buffer.sepia()


@signals.registered_handler("viewer/invert")
def invert(photo):
    photo.image_buffer.invert()


@signals.registered_handler("viewer/rotate")
def rotate(photo):
    photo.image_buffer.rotate()


@signals.registered_handler("viewer/mirror")
def mirror(photo):
    photo.image_buffer.mirror()


@signals.registered_handler("viewer/grayscale")
def grayscale(photo):
    photo.image_buffer.grayscale()


@signals.registered_handler("viewer/noise")
def noise(photo):
    photo.image_buffer.noise()


@signals.registered_handler("viewer/solarize")
def solarize(photo):
    photo.image_buffer.solarize()


@signals.registered_handler("viewer/original")
def original(photo):
    photo.image_buffer.original()
