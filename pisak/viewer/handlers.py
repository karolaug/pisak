@signals.registereg_handler("viewer/next_page")
def next_page(pager):
    pager.flip()


@signals.registered_handler("viewer/previous_page")
def previous_page(pager):
    pager.previous_page()


@signals.registered_handler("viewer/zoom")
def zoom(photo):
    photo.image_buffer.zoom()
    photo.image_buffer.load()


@signals.registered_handler("viewer/contour")
def contour(photo):
    photo.image_buffer.contour()
    photo.image_buffer.load()


@signals.registered_handler("viewer/edges")
def edges(photo):
    photo.image_buffer.edges()
    photo.image_buffer.load()


@signals.registered_handler("viewer/sepia")
def sepia(photo):
    photo.image_buffer.sepia()
    photo.image_buffer.load()


@signals.registered_handler("viewer/invert")
def invert(photo):
    photo.image_buffer.invert()
    photo.image_buffer.load()


@signals.registered_handler("viewer/rotate")
def rotate(photo):
    photo.image_buffer.rotate()
    photo.image_buffer.load()


@signals.registered_handler("viewer/mirror")
def mirror(photo):
    photo.image_buffer.mirror()
    photo.image_buffer.load()


@signals.registered_handler("viewer/grayscale")
def grayscale(photo):
    photo.image_buffer.grayscale()
    photo.image_buffer.load()


@signals.registered_handler("viewer/noise")
def noise(photo):
    photo.image_buffer.noise()
    photo.image_buffer.load()


@signals.registered_handler("viewer/solarize")
def solarize(photo):
    photo.image_buffer.solarize()
    photo.image_buffer.load()


@signals.registered_handler("viewer/original")
def original(photo):
    photo.image_buffer.original()
    photo.image_buffer.load()
