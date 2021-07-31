class Widget:
    def __init__(self):
        pass


class Widgets(Widget):
    def __init__(self):
        self.children = []

    def add(self, child):
        pass


class HortSpacer(Widget):
    def __init__(self):
        pass


class VertSpacer(Widget):
    def __init__(self):
        pass

    def layout(self):
        pass


class Col(Widgets):
    def __init__(self):
        pass

    pass


class Row(Widgets):
    def __init__(self):
        pass

    pass


class Box(Widget):
    def __init__(self):
        pass


# stack = []
# node = Widgets()
# stack.append(node)
# node = node.add(Col())
# stack.append(node)
# node = node.add(Row())
# stack.append(node)
# node.add(HortSpacer)
# node = stack.pop()

layout = [
    [HortSpacer(5)],
    [VertSpacer(5), Box(50, 50), VertSpacer(5)],
    [HortSpacer(5)],
]

col = Col()
for row in layout:    
    col.add(row)
    for node in row:
        row.add(node)


# class Compositor:
#     def __init__(self):
#         self.current = None

#     def composit(self, parent, layout):
#         self.current = parent
#         for node in layout:
#             self.current.children.append(node)
#             node.composit(self)
