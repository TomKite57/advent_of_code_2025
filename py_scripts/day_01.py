
from typing import Final
import enum

import common

_DATA_FILE_NAME: Final = 'data/day_01.txt'


class Direction(enum.Enum):
  LEFT = 'L'
  RIGHT = 'R'


def line_parse_fn(line: str) -> tuple[Direction, int]:
  direc = line[0]
  count = int(line[1:])

  if direc == Direction.LEFT.value:
    return Direction.LEFT, count
  elif direc == Direction.RIGHT.value:
    return Direction.RIGHT, count
  raise ValueError(f"Could not parse direction {direc}. Expected one of {list(Direction)}")


def rotate_dial(
    position: int,
    instruction: tuple[Direction, int]
) -> tuple[int, int]:
  direction, count = instruction
  multiplier = +1 if direction == Direction.RIGHT else -1
  hidden_zeros, new_position = divmod(position + multiplier*count, 100)
  hidden_zeros = abs(hidden_zeros)
  if position == 0 and direction == Direction.LEFT:
    hidden_zeros -= 1
  if new_position == 0 and direction == Direction.RIGHT:
    hidden_zeros -= 1
  return new_position, hidden_zeros


def dial_position_generator(
    instructions: tuple[Direction, int],
    start_position: int = 50
):
  position = start_position
  for instruction in instructions:
    position, hidden_zeros = rotate_dial(position, instruction)
    yield position, hidden_zeros


if __name__ == "__main__":
  aoc_manager = common.AdventOfCodeManager()
  data = common.read_and_parse_file(_DATA_FILE_NAME, line_parse_fn)
  part_1_sol = part_2_sol = 0

  for pos, hidden_zeros in dial_position_generator(data):
    part_1_sol += pos==0
    part_2_sol += hidden_zeros
  aoc_manager.submit_part_1(part_1_sol, expectation=984)
  part_2_sol += part_1_sol
  aoc_manager.submit_part_2(part_2_sol, expectation=5657)

  aoc_manager.show()
