
from typing import Final, Sequence, Iterator

import common

_DATA_FILE_NAME: Final = 'data/day_06.txt'


def parse_if_numbers(line: str) -> list[str] | list[int]:
  split_line = line.strip().split()
  return split_line if '+' in split_line else list(map(int, split_line))


def pad_string(
    string: str,
    pad_to: int,
    fill_char: str = ' '
):
  if len(fill_char) != 1:
    raise ValueError(f"Expected fill_char to be one character, got {fill_char}")
  if pad_to < 1:
    raise ValueError(f"Expected pad_to to be positive, got {pad_to}")
  if len(string) >= pad_to:
    return string
  return ''.join([string, fill_char*(pad_to - len(string))])


def get_separator_columns(numbers: list[str]) -> list[int]:
  num_total_rows = len(numbers)
  num_total_columns = len(numbers[0])

  separator_columns = set(range(num_total_columns))
  for col in range(num_total_columns):
    for row in range(num_total_rows):
      if numbers[row][col] != ' ':
        separator_columns.remove(col)
        break
  return list(separator_columns)


def split_lines_by_columns(
    lines: list[str],
    split_columns: Sequence[int]
) -> list[str]:
  split_columns = sorted(list(split_columns))
  split_columns = [-1] + split_columns + [len(lines[0])]
  new_lines = []
  for line in lines:
    new_line = []
    for i0, i1 in zip(split_columns[:-1], split_columns[1:], strict=True):
      new_line.append(line[i0+1:i1])
    new_lines.append(new_line)
  return new_lines


def pad_number_matrix(numbers: list[str]) -> list[str]:
  num_total_rows = len(numbers)
  num_total_columns = len(numbers[0])

  separator_columns = set(range(num_total_columns))
  for col in range(num_total_columns):
    for row in range(num_total_rows):
      if numbers[row][col] != ' ':
        separator_columns.remove(col)
        break

  for row in range(num_total_rows):
    new_row = []
    for col in range(num_total_columns):
      if col in separator_columns:
        new_row.append(' ')
      elif numbers[row][col] == ' ':
        new_row.append('0')
      else:
        new_row.append(numbers[row][col])
    numbers[row] = ''.join(new_row)

  return numbers

def long_sum(elements: Sequence[int]) -> int:
  return sum(elements)


def long_product(elements: Sequence[int]) -> int:
  mult = 1
  for element in elements:
    mult *= element
  return mult


def extract_column_numbers(elements: Sequence[str]) -> list[int]:
  num_cols = len(elements[0])
  num_rows = len(elements)
  column_nums = []
  for col in range(num_cols):
    num = int(''.join((elements[row][col] for row in range(num_rows))))
    column_nums.append(num)
  return column_nums


_SYMBOL_TO_FUNCTION: Final = {
  '+': long_sum,
  '*': long_product
}


if __name__ == "__main__":
  aoc_manager = common.AdventOfCodeManager()
  part_1_data = common.read_and_parse_file(_DATA_FILE_NAME, parse_if_numbers)
  part_1_sol = part_2_sol = 0

  numbers = part_1_data[:-1]
  operations = part_1_data[-1]
  for col, op in enumerate(operations):
    number_column = [numbers[i][col] for i in range(len(numbers))]
    part_1_sol += _SYMBOL_TO_FUNCTION[op](number_column)
  aoc_manager.submit_part_1(part_1_sol, expectation=6100348226985)

  number_matrix = common.read_raw_file(_DATA_FILE_NAME).strip().split('\n')[:-1]
  max_length = max(len(line) for line in number_matrix)
  number_matrix = [pad_string(line, max_length) for line in number_matrix]
  separator_columns = get_separator_columns(number_matrix)
  number_matrix = split_lines_by_columns(number_matrix, separator_columns)
  for col, op in enumerate(operations):
    number_column = [number_matrix[i][col] for i in range(len(number_matrix))]
    part_2_sol += _SYMBOL_TO_FUNCTION[op](extract_column_numbers(number_column))
  aoc_manager.submit_part_2(part_2_sol, expectation=12377473011151)

  aoc_manager.show()
