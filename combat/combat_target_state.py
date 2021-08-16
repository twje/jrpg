import random
import pygame
import sys
from core.graphics import Sprite
from utils import lookup_texture_filepath


class CombatSelector:
    @staticmethod
    def weakest_enemy(state):
        return CombatSelector.weakest_actor(state.actors["enemy"], False)

    @staticmethod
    def weakest_party(state):
        return CombatSelector.weakest_actor(state.actors["party"], False)

    @staticmethod
    def most_hurt_enemy(state):
        return CombatSelector.weakest_actor(state.actors["enemy"], True)

    @staticmethod
    def most_hurt_party(state):
        return CombatSelector.weakest_actor(state.actors["party"], True)

    @staticmethod
    def most_drained_party(state):
        return CombatSelector.most_drained_actor(state.actors["party"], True)

    @staticmethod
    def dead_party(state):
        actors = state.actors["party"]
        for actor in actors:
            hp = actor.stats.get("hp_now")
            if hp == 0:
                return [actor]

        return [actors[0]]

    @staticmethod
    def side_enemy(state):
        return state.actors["enemy"]

    @staticmethod
    def sellect_all(state):
        targets = []
        targets.extend(state.actors["enemy"])
        targets.extend(state.actors["party"])
        return targets

    @staticmethod
    def random_alive_player(state):
        targets = []
        for actor in state.actors["party"]:
            if actor.stats.get("hp_now") > 0:
                targets.append(actor)

        target = random.choice(targets)
        return [target]

    # --------------
    # Helper Methods
    # --------------
    def weakest_actor(actors, only_check_hurt):
        target = None
        health = sys.maxsize

        for actor in actors:
            hp = actor.stats.get("hp_now")
            is_hurt = hp < actor.stats.get("hp_max")
            skip = False
            if only_check_hurt and not is_hurt:
                skip = True

            if hp < health and not skip:
                health = hp
                target = actor

        if target is None:
            target = actors[0]

        return [target]

    def most_drained_actor(actors, only_check_drained):
        target = None
        magic = sys.maxsize

        for actor in actors:
            mp = actor.stats.get("mp_now")
            is_hurt = mp < actor.stats.get("mp_max")
            skip = False
            if only_check_drained and not is_hurt:
                skip = True

            if mp < magic and not skip:
                magic = mp
                target = actor

        if target is None:
            target = actors[0]

        return [target]


class CombatTargetType:
    ONE = "one"
    SIDE = "side"
    ALL = "all"


class CombatTargetState:
    def __init__(self, context, **kwargs):
        self.combat_state = context
        self.stack = context.stack
        self.default_selector = kwargs.get("default_selector")
        self.can_switch_sides = kwargs.get("can_switch_sides", True)
        self.select_type = kwargs.get("target_type", CombatTargetType.ONE)
        self.on_select = kwargs["on_select"]
        self.on_exit = kwargs.get("on_exit", lambda: None)
        self.targets = []
        self.enemy = []
        self.party = []
        self.maker = Sprite.load_from_filesystem(
            lookup_texture_filepath("cursor.png")
        )
        self.maker.flip(True, False)

        # init defaults
        if self.default_selector == None:
            if self.select_type == CombatTargetType.ONE:
                self.default_selector = CombatSelector.weakest_enemy
            elif self.select_type == CombatTargetType.SIDE:
                self.default_selector = CombatSelector.side_enemy
            elif self.select_type == CombatTargetType.ALL:
                self.default_selector = CombatSelector.sellect_all
        else:
            self.default_selector = getattr(
                CombatSelector, self.default_selector)

    def enter(self):
        self.enemy = self.combat_state.actors["enemy"]
        self.party = self.combat_state.actors["party"]
        self.targets = self.default_selector(self.combat_state)

    def exit(self):
        self.enemy = []
        self.party = []
        self.targets = []

    def get_actor_list(self, actor):
        is_party = self.combat_state.is_party_member(actor)
        if is_party:
            return self.party
        else:
            return self.enemy

    def up(self):
        if self.select_type != CombatTargetType.ONE:
            return

        selected = self.targets[0]
        actors = self.get_actor_list(selected)
        index = actors.index(selected)

        index -= 1
        if index < 0:
            index = len(actors) - 1
        self.targets = [actors[index]]

    def down(self):
        if self.select_type != CombatTargetType.ONE:
            return

        selected = self.targets[0]
        actors = self.get_actor_list(selected)
        index = actors.index(selected)

        index += 1
        if index >= len(actors):
            index = 0
        self.targets = [actors[index]]

    def left(self):
        if not self.can_switch_sides:
            return

        if not self.combat_state.is_party_member(self.targets[0]):
            return

        # select enemy members
        if self.select_type == CombatTargetType.ONE:
            self.targets = [self.enemy[0]]

        if self.select_type == CombatTargetType.SIDE:
            self.targets = self.enemy

    def right(self):
        if not self.can_switch_sides:
            return

        if self.combat_state.is_party_member(self.targets[0]):
            return

        # select party members
        if self.select_type == CombatTargetType.ONE:
            self.targets = [self.party[0]]

        if self.select_type == CombatTargetType.SIDE:
            self.targets = self.party

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.up()
            elif event.key == pygame.K_DOWN:
                self.down()
            elif event.key == pygame.K_RIGHT:
                self.right()
            elif event.key == pygame.K_LEFT:
                self.left()
            elif event.key == pygame.K_SPACE:
                self.on_select(self.targets)

    def update(self, dt):
        return False

    def render(self, renderer):
        for actor in self.targets:
            character = self.combat_state.actor_char_map[actor]
            x, y = character.entity.get_target_position()
            self.maker.set_position(x, y - self.maker.height/2)
            renderer.draw(self.maker)
