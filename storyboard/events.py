import utils
import functools
from core.graphics.sprite_font import Font, FontStyle
from state_stack.effects import ScreenState
from state_stack.world import ExploreState
from state_stack.menu import CaptionState
from core import Camera
from core import Context
from core import tween
from caption_style import caption_syles
from actions import action_registry


def debug_storyboard_event(event):
    def event_object(func):
        @functools.wraps(func)
        def debug_wrapper(*args, **kwargs):
            # print(event.__name__)
            return func(*args, **kwargs)
        return debug_wrapper
    return event_object


# ------
# Events
# ------
class NullEvent:
    def update(self, dt):
        pass

    def is_blocking(self):
        return True

    def is_finished(self):
        return True

    def render(self, renderer):
        pass


class WaitEvent:
    def __init__(self, seconds):
        self.seconds = seconds

    def update(self, dt):
        self.seconds = self.seconds - dt

    def is_blocking(self):
        return True

    def is_finished(self):
        return self.seconds <= 0

    def render(self, renderer):
        pass


class TweenEvent:
    def __init__(self, tween, target, apply_func):
        self.tween = tween
        self.target = target
        self.apply_func = apply_func

    def update(self, dt):
        self.tween.update(dt)
        self.apply_func(self.target, self.tween.value)

    def is_blocking(self):
        return True

    def is_finished(self):
        return self.tween.is_finished

    def render(self, renderer):
        pass


class BlockUntilEvent:
    def __init__(self, until_func):
        self.until_func = until_func

    def update(self, dt):
        pass

    def is_blocking(self):
        return not self.until_func()

    def is_finished(self):
        return not self.is_blocking()

    def render(self, renderer):
        pass


class TimedTextboxEvent:
    def __init__(self, box, time):
        self.box = box
        self.count_down = time

    def update(self, dt):
        self.count_down -= dt
        if self.count_down <= 0:
            self.box.on_click()

    def is_blocking(self):
        return self.count_down > 0

    def is_finished(self):
        return not self.is_blocking()

    def render(self, renderer):
        pass


# ---------
# Factories
# ---------
def wait(seconds):
    @debug_storyboard_event(wait)
    def create(storyboard):
        return WaitEvent(seconds)
    return create


def black_screen(idz=None, alpha=1):
    idz = "blackscreen" if idz is None else idz

    @debug_storyboard_event(black_screen)
    def create(storyboard):
        state = ScreenState()
        state.set_alpha(alpha)
        storyboard.push_state(idz, state)
        return NullEvent()
    return create


def play(resource_id, volume=1):
    @debug_storyboard_event(play)
    def create(storyboard):
        sound_manger = Context.instance().sound_manager
        sound = sound_manger.get_sound(resource_id)
        sound.play()
        sound.set_volume(volume)
        storyboard.add_sound(resource_id, sound)
        return NullEvent()
    return create


def stop(sound_id):
    @debug_storyboard_event(stop)
    def create(storyboard):
        storyboard.stop_sound(sound_id)
        return NullEvent()
    return create


def fade_sound(sound_id, start, finish, duration):
    @debug_storyboard_event(fade_sound)
    def create(storyboard):
        sound = storyboard.playing_sounds[sound_id]
        return TweenEvent(
            tween.Tween(start, finish, duration),
            sound,
            lambda target, value: target.set_volume(value)
        )
    return create


def fade_screen(idz, duration, start, finish):
    duration = 3 if duration is None else duration

    @debug_storyboard_event(fade_screen)
    def create(storyboard):
        target = storyboard.sub_stack.top()
        if idz is not None:
            target = storyboard.states[idz]
        assert target is not None

        return TweenEvent(
            tween.Tween(start, finish, duration),
            target,
            lambda target, value: target.set_alpha(value)
        )
    return create


def fade_in_screen(idz=None, duration=None):
    return fade_screen(idz, duration, 0, 1)


def fade_out_screen(idz=None, duration=None):
    return fade_screen(idz, duration, 1, 0)


def caption(idz, style_id, text, layouter):
    @debug_storyboard_event(caption)
    def create(storybaord):
        style = caption_syles(style_id)
        caption = CaptionState(text, style["font"], layouter)
        storybaord.push_state(idz, caption)

        return TweenEvent(
            tween.Tween(0, 1, style.get("duration", 1)),
            caption,
            lambda target, value: target.set_alpha(value)
        )
    return create


def fade_out_caption(idz=None, duration=None):
    if duration is None:
        duration = 1

    @debug_storyboard_event(fade_out_caption)
    def create(storybaord):
        if idz is None:
            target = storybaord.sub_stack.top()
        else:
            target = storybaord.states[idz]

        return TweenEvent(
            tween.Tween(1, 0, duration),
            target,
            lambda target, value: target.set_alpha(value)
        )

    return create


def no_block(f):
    @debug_storyboard_event(no_block)
    def create(storybaord):
        event = f(storybaord)
        event.is_blocking = lambda: False
        return event
    return create


def kill_state(idz):
    @debug_storyboard_event(kill_state)
    def create(storybaord):
        storybaord.remove_state(idz)
        return NullEvent()
    return create


def scene(params):
    @debug_storyboard_event(scene)
    def create(storyboard):
        idz = params.get("name", params["map"])
        state = ExploreState(
            None,
            Camera.create_camera_from_surface(
                Context.instance().info.surface
            ),
            params["map"],
            params.get("focus_x", 0),
            params.get("focus_y", 0),
            params.get("focus_z", 0),
        )
        if params.get("hide_hero", False):
            state.hide_hero()
        storyboard.push_state(idz, state)
        return NullEvent()
    return create


def get_map_ref(storyboard, state_id):
    explore_state = storyboard.states[state_id]
    return explore_state.map


def replace_scene(name, params):
    @debug_storyboard_event(replace_scene)
    def create(storyboard):
        state = storyboard.states[name]

        # give the state an updated name
        idz = params.get("name", params["map"])
        storyboard.states[name] = None
        storyboard.states[idz] = state

        # load map
        map_db = Context.instance().data["maps"]
        state.map = map_db.new_map(params["map"], params.get("seed"))

        # position camera and hero
        state.go_to_tile(params["focus_x"], params["focus_y"])
        state.hero.entity.set_tile_pos(
            params["focus_x"],
            params["focus_y"],
            params.get("focus_z", 0),
            state.map
        )
        state.hero.reset_map(state.map)
        state.set_follow_cam(True, state.hero)

        if params.get("hide_hero", False):
            state.hide_hero()
        else:
            state.show_hero()

        return no_block(wait(0.1))(storyboard)
    return create


def say(map_id, npc_id, text, time):
    @debug_storyboard_event(say)
    def create(storyboard):
        map = get_map_ref(storyboard, map_id)
        if npc_id == "hero":
            npc = storyboard.states[map_id].hero
        else:
            npc = map.npc_by_id[npc_id]

        x, y = map.get_tile_foot(npc.entity.tile_x, npc.entity.tile_y)
        font = Font(FontStyle.npc_dialogue())

        storyboard.stack.push_fitted(
            x - map.cam_x + npc.entity.sprite.width/2,
            y - map.cam_y - npc.entity.sprite.height - font.height(),
            font,
            text,
            200  # hack
        )
        box = storyboard.stack.top()
        return TimedTextboxEvent(box, time)
    return create


def run_action(action_id, action_params, parm_ops={}):
    @debug_storyboard_event(run_action)
    def create(storyboard):
        # format params
        params, location = utils.extract_from_dict(
            action_params, [], {"tile_x": None, "tile_y": None, "layer": 0}
        )

        # pre-process params
        for key, value in params.items():
            if key in parm_ops:
                new_value = parm_ops[key](storyboard, value)
                params[key] = new_value

        # invoke action
        action = action_registry[action_id]
        action(**params)(None, None, **location)

        return NullEvent()
    return create


def move_npc(npc_id, map_id, path):
    @debug_storyboard_event(move_npc)
    def create(storyboard):
        map = get_map_ref(storyboard, map_id)
        npc = map.npc_by_id[npc_id]
        npc.follow_path(path)
        return BlockUntilEvent(
            lambda: npc.is_path_complete()
        )
    return create


def hand_off(map_id):
    @debug_storyboard_event(hand_off)
    def create(storyboard):
        explore_state = storyboard.states[map_id]

        # remove storyboard from top of the stack
        storyboard.stack.pop()
        storyboard.stack.push(explore_state)
        explore_state.stack = storyboard.stack

        return NullEvent()
    return create


def fade_out_char(map_id, npc_id, duration=1):
    @debug_storyboard_event(fade_out_char)
    def create(storyboard):
        map = get_map_ref(storyboard, map_id)
        if npc_id == "hero":
            npc = storyboard.states[map_id].hero
        else:
            npc = map.npc_by_id[npc_id]

        return TweenEvent(
            tween.Tween(1, 0, duration),
            npc.entity.sprite,
            lambda target, value: target.set_alpha(value)
        )
    return create


def write_to_tile(map_id, x, y, layer, tile, detail=0, is_collision=False):
    @debug_storyboard_event(write_to_tile)
    def create(storyboard):
        map = get_map_ref(storyboard, map_id)
        map.write_tile(x, y, layer, tile, detail, is_collision)
        return NullEvent()
    return create


def move_cam_to_tile(state_id, tile_x, tile_y, duration=1):
    @debug_storyboard_event(move_cam_to_tile)
    def create(storyboard):
        state = storyboard.states[state_id]
        state.set_follow_cam(False)

        start_x = state.manual_cam_x
        start_y = state.manual_cam_y
        end_x, end_y = state.map.get_tile_centre(tile_x, tile_y)
        distance_x = end_x - start_x
        distance_y = end_y - start_y

        def animiate(target, value):
            dx = start_x + (distance_x * value)
            dy = start_y + (distance_y * value)
            target.manual_cam_x = dx
            target.manual_cam_y = dy

        return TweenEvent(
            tween.Tween(0, 1, duration, tween.ease_out_quad),
            state,
            animiate
        )

    return create

def function(func):
    @debug_storyboard_event(move_cam_to_tile)
    def create(storyboard):
        func()
        return NullEvent()
    return create


def run_state(statemachine, state_id, params):
    @debug_storyboard_event(move_cam_to_tile)
    def create(storyboard):
        statemachine.change(state_id, params)
        return BlockUntilEvent(
            lambda: statemachine.current.is_finished()
        )
    return create
