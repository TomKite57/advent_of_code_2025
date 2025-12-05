
from typing import Final, Callable

import common

_DATA_FILE_NAME: Final = 'data/day_02.txt'


def line_parse_fn(line: str) -> list[list[int]]:
  ranges = line.split(',')
  return [[int(x) for x in r.split('-')] for r in ranges]


def is_number_doubled(num: int) -> bool:
  num = str(num)
  if len(num)%2 != 0:
    return False
  mid = len(num) // 2
  return num[:mid] == num[mid:]


def is_number_repeating_pattern(num: int) -> bool:
  num = str(num)
  for repeat_length in range(1, len(num)//2+1):
    if len(num)%repeat_length != 0:
      continue

    proposed_template = num[:repeat_length]
    for idx in range(repeat_length, len(num), repeat_length):
      if num[idx:idx+repeat_length] != proposed_template:
        break
    else:
      return True
  return False


def count_matching_numbers_in_range(
    start: int,
    end: int,
    match_function: Callable[[int], bool],
):
  count = 0
  for num in range(start, end+1):
    if match_function(num):
      count += num
  return count


if __name__ == "__main__":
  aoc_manager = common.AdventOfCodeManager()
  data = common.read_and_parse_file(_DATA_FILE_NAME, line_parse_fn)
  part_1_sol = part_2_sol = 0

  part_1_sol = sum(count_matching_numbers_in_range(*ran, is_number_doubled) for ran in data)
  aoc_manager.submit_part_1(part_1_sol, expectation=23534117921)
  part_2_sol = sum(count_matching_numbers_in_range(*ran, is_number_repeating_pattern) for ran in data)
  aoc_manager.submit_part_2(part_2_sol, expectation=31755323497)

  aoc_manager.show()
