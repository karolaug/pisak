import os

from pisak import launcher
from pisak import cursor


def prepare_head_editing_view(stage, script, data):
    pass
    

def fix_path(path):
    return os.path.join(os.path.split(__file__)[0], path)


VIEWER_APP = {
    "views": {
        "head": (fix_path("head_tracking.json"), prepare_head_editing_view)
    },
    "initial-view": "head",
    "initial-data": None
}


if __name__ == "__main__":
    launcher.run(VIEWER_APP)
