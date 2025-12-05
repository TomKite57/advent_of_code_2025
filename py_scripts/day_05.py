
from typing import Final, Sequence, NewType

import common

_DATA_FILE_NAME: Final = 'data/day_05.txt'


Range = NewType("Range", tuple[int, int])


def read_and_parse_file(
    file_name: str
) -> tuple[list[Range], list[int]]:
  with open(file_name, 'r') as open_file:
    raw_lines = open_file.read()
  ranges, ingredients = raw_lines.split('\n\n')
  ranges = [line for line in ranges.split('\n') if line]
  ingredients = [line for line in ingredients.split('\n') if line]

  ranges = [tuple(map(int, line.split('-'))) for line in ranges]
  ingredients = [int(x) for x in ingredients]
  return ranges, ingredients


def is_number_in_any_range(
    number: int,
    ranges: Sequence[Range],
) -> bool:
  for ran in ranges:
    if ran[0] <= number <= ran[1]:
      return True
  return False


def can_ranges_be_merged(
    range_a: Range,
    range_b: Range,
) -> bool:
  if range_a[0] == range_b[0] or range_a[1] == range_b[1]:
    return True
  if range_b[0] < range_a[0]:
    return can_ranges_be_merged(range_b, range_a)
  return range_a[1] >= range_b[0]


def merge_ranges(
    range_a: Range,
    range_b: Range,
) -> Range:
  if not can_ranges_be_merged(range_a, range_b):
    raise ValueError(f"Can't merge ranges {range_a} and {range_b}")
  return min(range_a[0], range_b[0]), max(range_a[1], range_b[1])


def iteratively_merge_all_ranges(
    ranges: Sequence[Range],
) -> list[Range]:
  ranges = sorted(ranges, key=lambda x: x[0])

  while True:
    new_ranges = []
    idx = 0
    while idx < len(ranges)-1:
      range_a, range_b = ranges[idx], ranges[idx+1]
      if can_ranges_be_merged(range_a, range_b):
        new_ranges.append(merge_ranges(range_a, range_b))
        idx += 2
        if idx == len(ranges) - 1:
          new_ranges.append(ranges[-1])
      else:
        new_ranges.append(range_a)
        idx += 1
        if idx == len(ranges) - 1:
          new_ranges.append(ranges[-1])
    if len(new_ranges) == len(ranges):
      return new_ranges
    ranges = new_ranges


def count_all_in_range(
    ranges: Sequence[Range],
):
  for range_a, range_b in zip(ranges[:-1], ranges[1:], strict=True):
    if can_ranges_be_merged(range_a, range_b):
      raise ValueError(f"Found mergable ranges {range_a} and {range_b}")
  return sum(b-a+1 for a, b in ranges)


if __name__ == "__main__":
  timer = common.AdventOfCodeTimer()
  ranges, ingredients = read_and_parse_file(_DATA_FILE_NAME)
  ranges = sorted(ranges, key=lambda x: x[0])
  merged_ranges = iteratively_merge_all_ranges(ranges)
  part_1_sol = part_2_sol = 0

  part_1_sol = sum(is_number_in_any_range(num, merged_ranges) for num in ingredients)
  timer.part_1_checkpoint()

  part_2_sol = count_all_in_range(merged_ranges)
  timer.part_2_checkpoint()

  common.pretty_format_and_maybe_check(
    answer=part_1_sol,
    part=1,
    expectation=896
  )

  common.pretty_format_and_maybe_check(
    answer=part_2_sol,
    part=2,
    expectation=346240317247002
  )

  timer.show_times()
