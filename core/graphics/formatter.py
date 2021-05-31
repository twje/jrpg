# -------
# Helpers
# -------
def cap(min_value, max_value, value):
    return min(max(value, min_value), max_value)


def left_justify(margin, drawable_0, drawable_1):
    extreme = drawable_0.x + drawable_0.width - drawable_1.width
    return cap(
        drawable_0.x,
        extreme,
        drawable_0.x + margin
    )


def right_justify(margin, drawable_0, drawable_1):
    extreme = drawable_0.x + drawable_0.width - drawable_1.width
    return cap(
        drawable_0.x,
        extreme,
        extreme - margin
    )


def bottom_justify(margin, drawable_0, drawable_1):
    extreme = drawable_0.y + drawable_0.height - drawable_1.height
    return cap(
        drawable_0.y,
        extreme,
        extreme - margin
    )


def top_justify(margin, drawable_0, drawable_1):
    extreme = drawable_0.y + drawable_0.height - drawable_1.height
    return cap(
        drawable_0.y,
        extreme,
        drawable_0.y + margin
    )


def center_x(drawable_0, drawable_1):
    return drawable_0.x + (drawable_0.width - drawable_1.width)/2


def center_y(drawable_0, drawable_1):
    return drawable_0.y + (drawable_0.height - drawable_1.height)/2


def place_ratio_x(ratio, drawable_0, drawable_1):
    return cap(
        drawable_0.x,
        drawable_0.width - drawable_1.width,
        drawable_0.x + ratio * drawable_0.width - drawable_1.width/2
    )


def place_ratio_y(ratio, drawable_0, drawable_1):
    return cap(
        drawable_0.y,
        drawable_0.height - drawable_1.height,
        drawable_0.x + ratio * drawable_0.height - drawable_1.height/2
    )


def vert_stack(index, top_margin, space_margin, drawable_0, drawable_1):
    start_y = drawable_0.y + top_margin
    start_y += index * drawable_1.height
    start_y += (index + 1) * space_margin
    return start_y


# -------------------
# In Place Formatters
# -------------------
def in_place_center(drawable_0, drawable_1):
    x = center_x(drawable_0, drawable_1)
    y = center_y(drawable_0, drawable_1)
    drawable_1.x = x
    drawable_1.y = y


def in_place_positon(ratio_x, ratio_y, drawable_0, drawable_1):
    x = place_ratio_x(ratio_x, drawable_0, drawable_1)
    y = place_ratio_y(ratio_y, drawable_0, drawable_1)
    drawable_1.x = x
    drawable_1.y = y
