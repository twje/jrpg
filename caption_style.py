from core.graphics import FontStyle
from core.graphics import Font


__data = None


def apply_fade(target, alpha):
    target.set_alpha(alpha)


def caption_syles(style_id):
    global __data

    if __data is None:
        __data = {
            "default": {
                "font": Font(style=FontStyle.default()),
                "apply_func": lambda value, target: None
            },
            "title": {
                "font": Font(style=FontStyle.storyboard_title()),
                "apply_func": apply_fade,
                "duration": 3
            },
            "subtitle": {
                "font": Font(style=FontStyle.default()),
                "apply_func": apply_fade,
                "duration": 1
            },
        }

    return __data[style_id]
