
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
  timer = common.AdventOfCodeTimer()
  data = common.read_and_parse_file(_DATA_FILE_NAME, line_parse_fn)
  part_1_sol = part_2_sol = 0

  for pos, hidden_zeros in dial_position_generator(data):
    part_1_sol += pos==0
    part_2_sol += hidden_zeros
  timer.part_1_checkpoint()
  part_2_sol += part_1_sol
  timer.part_2_checkpoint()

  common.pretty_format_and_maybe_check(
    answer=part_1_sol,
    part=1,
    expectation=984
  )

  common.pretty_format_and_maybe_check(
    answer=part_2_sol,
    part=2,
    expectation=5657
  )

  timer.show_times()
