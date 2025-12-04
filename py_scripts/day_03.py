
from typing import Final

import common

_DATA_FILE_NAME: Final = 'data/day_03.txt'


def line_parse_fn(line: str) -> list[int]:
  return [int(char) for char in line]


def get_largest_combination(line: list[int], num_digits: int) -> int:
  running_digits = [line[-i] for i in range(1, num_digits+1)][::-1]

  for new_digit in line[-num_digits-1::-1]:
    if new_digit >= running_digits[0]:
      for i, running_digit in enumerate(running_digits):
        if new_digit >= running_digit:
          running_digits[i], new_digit = new_digit, running_digits[i]
        else:
          break

  largest_pairing = int(''.join([str(digit) for digit in running_digits]))
  return largest_pairing


def get_largest_pairing(line: list[int]) -> int:
  return get_largest_combination(line, 2)


if __name__ == "__main__":
  timer = common.AdventOfCodeTimer()
  data = common.read_and_parse_file(_DATA_FILE_NAME, line_parse_fn)
  part_1_sol = part_2_sol = 0

  part_1_sol = sum(get_largest_pairing(line) for line in data)
  timer.part_1_checkpoint()
  part_2_sol = sum(get_largest_combination(line, 12) for line in data)
  timer.part_2_checkpoint()

  common.pretty_format_and_maybe_check(
    answer=part_1_sol,
    part=1,
    expectation=16993
  )

  common.pretty_format_and_maybe_check(
    answer=part_2_sol,
    part=2,
    expectation=168617068915447
  )

  timer.show_times()


"""
These were my functions for the less general part one, and my naive (slow) function for debugging

def slow_get_largest_pairing(line: list[int]) -> int:
  running_max = 0
  for i, left in enumerate(line):
    for right in line[i+1:]:
      num = left*10 + right
      running_max = max(running_max, num)
  return running_max


def get_largest_pairing(line: list[int]) -> int:
  left, right = line[-2], line[-1]
  for digit in line[-3::-1]:
    if digit >= left:
      if left > right:
        right = left
      left = digit
  largest_pairing = left*10 + right
  return largest_pairing
"""
