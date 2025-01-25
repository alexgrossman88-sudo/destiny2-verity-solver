from argparse import ArgumentParser, RawTextHelpFormatter
from enum import StrEnum
from typing import assert_never

import solve
from .combo import get_best_double_key
from .config import KeySetName, read_config
from .key_sets import *
from .move_analyzer import *


class EncounterParts(StrEnum):
    SOLO_ROOMS = 'solo-rooms'
    DISSECTION = 'dissection'
    BOTH = 'both'


def main(
        config_filepath: str,
        encounter_part: EncounterParts,
        /,
        interactive: bool,
        ) -> None:
    config = read_config(config_filepath)

    match encounter_part:
        case EncounterParts.SOLO_ROOMS:
            do_rooms = True
            do_dissect = False
        case EncounterParts.DISSECTION:
            do_rooms = False
            do_dissect = True
        case EncounterParts.BOTH:
            do_rooms = True
            do_dissect = True
        case unknown:
            assert_never(unknown)

    with_triumph = config.is_doing_triumph
    last_position = config.last_position
    rooms, statues, aliases = config.encounter_data()
    match config.key_set_name:
        case KeySetName.MIXED:
            key_set = KS_MIXED
        case KeySetName.DOUBLE:
            key_set = get_best_double_key(
                rooms=rooms if do_rooms else None,
                statues=statues if do_dissect else None,
                )
        case unknown:
            assert_never(unknown)

    print('--- FINAL SHAPES FROM LEFT TO RIGHT ---')
    print(*map(key_set.__getitem__, config.shades))

    print_step = input if interactive else print

    if do_rooms:
        print('\n--- STEPS FOR SOLO ROOMS ---')
        room_state = rooms.to_room_state(key_set)
        rooms_solutions = room_state.solve(with_triumph, last_position)
        rooms_best, rooms_steps = best_solution(rooms_solutions, aliases, describe_pass_moves)
        for step in rooms_steps:
            print_step(step.render())

        last_position = rooms_best.last_position
        print(
            '--- SOLO ROOMS ARE DONE ---\n'
            'All players in solo rooms must collect two shapes and wait'
            )

    if do_dissect:
        print('\n--- STEPS FOR DISSECTION ---')
        statue_state = statues.to_statue_state(key_set)
        statues_solutions = statue_state.solve(with_triumph, last_position)
        statues_best, statues_steps = best_solution(
            statues_solutions,
            aliases,
            describe_dissect_moves,
            )
        for step in statues_steps:
            print_step(step.render())

        last_position = statues_best.last_position
        print(
            '--- DISSECTION IS DONE ---\n'
            'All players in solo rooms must leave them'
            )

    print(f'\n--- LAST POSITION ---\n{last_position}')


def define_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog=f'python -m {solve.__name__}',
        description='A script for solving 4th encounter of Salvation Edge in Destiny 2',
        formatter_class=RawTextHelpFormatter,
        add_help=False,
        )

    parser.add_argument(
        'encounter_part',
        metavar='ENCOUNTER-PART',
        choices=EncounterParts,
        default=EncounterParts.BOTH,
        help='Specifies what encounter part to solve.\n'
             f'  - "{EncounterParts.SOLO_ROOMS}" - '
             f'the script prints solution only for solo rooms.\n'
             f'  - "{EncounterParts.DISSECTION}" - '
             f'the script prints solution only for dissection.\n'
             f'  - "{EncounterParts.BOTH}" - '
             f'the script prints solution for solo rooms, then for dissection.\n'
             f'Defaults to "{EncounterParts.BOTH}".',
        )

    parser.add_argument(
        '-h',
        '--help',
        action='help',
        help='If specified, the script shows this help message and exits.',
        )

    parser.add_argument(
        '-i',
        '--interactive',
        action='store_true',
        help='If specified, the script requests user prompt after every step of the solution. '
             'The user must press Enter to go to the next step.',
        )

    parser.add_argument(
        '-c',
        '--config',
        default='config.toml',
        help='Path to the configuration file with the encounter settings. '
             'You can create one from file "config-template.toml". '
             'Defaults to "config.toml".',
        )

    return parser


if __name__ == '__main__':
    args = define_parser().parse_args()
    main(args.config, args.encounter_part, args.interactive)
