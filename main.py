#!/usr/bin/env python3
import logging
import random

import tcod

import game.color
import game.engine
import game.entity
import game.input_handlers
import game.procgen
from game.components.ai import HostileEnemy
from game.components.fighter import Fighter


def main() -> None:
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    max_monsters_per_room = 2

    tileset = tcod.tileset.load_tilesheet("data/dejavu16x16_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)

    engine = game.engine.Engine()
    engine.rng = random.Random()
    engine.game_map = game.procgen.generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        max_monsters_per_room=max_monsters_per_room,
        engine=engine,
    )
    engine.player = game.entity.Actor(
        engine.game_map,
        *engine.game_map.enter_xy,
        char="@",
        color=(255, 255, 255),
        name="Player",
        ai_cls=HostileEnemy,
        fighter=Fighter(hp=30, defense=2, power=5),
    )
    engine.update_fov()

    event_handler: game.input_handlers.EventHandler = game.input_handlers.MainGameEventHandler(engine)

    engine.message_log.add_message("Hello and welcome, adventurer, to yet another dungeon!", game.color.welcome_text)

    with tcod.context.new(
        columns=screen_width,
        rows=screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            root_console.clear()
            event_handler.on_render(console=root_console)
            context.present(root_console)

            for event in tcod.event.wait():
                event_handler = event_handler.handle_events(event)


if __name__ == "__main__":
    if __debug__:
        logging.basicConfig(level=logging.DEBUG)
    main()
