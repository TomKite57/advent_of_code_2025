
from typing import Callable, Any, Final, Sequence, TypeVar, Iterable
import time
from collections import defaultdict

_IDENTITY: Final = lambda x: x
_T = TypeVar('_T')


def read_and_parse_file(
    file_name: str,
    parse_fn: Callable[[str], Any] = lambda x: x
):
  with open(file_name, 'r') as open_file:
    data = [parse_fn(line.strip()) for line in open_file]
  if len(data) == 1:
     return data[0]
  return data


def read_and_parse_multicolumn_file(
    file_name: str,
    parse_fns: Sequence[Callable[[str], Any] | None] = [lambda x: x],
    separator: str = '\t',
    exclude_empty: bool = True
):
  for idx, fn in enumerate(parse_fns):
    if fn is None:
      parse_fns[idx] = _IDENTITY

  def parse_fn(line) -> list[Any]:
    if not line:
      if exclude_empty:
        return
      raise ValueError("Found empty line, but exclude_empty=False")
    return [fn(chunk) for fn, chunk in
              zip(parse_fns, line.split(separator), strict=True)
            ]

  return read_and_parse_file(file_name, parse_fn)


def read_and_parse_grid_to_dict(
    file_name: str,
    *,
    default_return: str | None = None,
) -> dict[complex, str]:
  if default_return is not None:
    map_content_by_coord = defaultdict(lambda: default_return)
  else:
    map_content_by_coord = dict()
  with open(file_name, 'r') as open_file:
    for row, line in enumerate(open_file):
        for col, char in enumerate(line):
          pos = col + row*1.j
          map_content_by_coord[pos] = char
  return map_content_by_coord


def get_complex_directions(
    *,
    include_diagonals=False
) -> Iterable[complex]:
   yield from (1, 1.j, -1, -1.j)
   if include_diagonals:
      yield from (1+1.j, 1-1.j, -1+1.j, -1-1.j)


class AdventOfCodeTimer:
  def __init__(self):
    self.start_time = time.perf_counter()
    self.part_1_time = None
    self.part_2_time = None

  def part_1_checkpoint(self):
    if self.part_1_time is not None:
      raise ValueError("Part 1 time already set. Did you mean part_2_checkpoint?")
    self.part_1_time = time.perf_counter()

  def part_2_checkpoint(self):
    if self.part_2_time is not None:
      raise ValueError("Part 2 time already set. Did you mean part_1_checkpoint?")
    self.part_2_time = time.perf_counter()

  def show_times(self):
    if self.part_1_time:
      part_1_delta = self.part_1_time - self.start_time
      print(f"Part 1 took {part_1_delta:.3f} s")
      if self.part_2_time:
        part_2_delta = self.part_2_time - self.part_1_time
        print(f"Part 2 took {part_2_delta:.3f} s")




def pretty_format_and_maybe_check(
    answer: _T,
    part: int,
    expectation: _T | None = None
):
    print(f"🎄 Part {part} 🎄")
    print(f"{answer}")
    if expectation is not None:
        if answer == expectation:
            print("✨ Correct! Look at you, you festive little genius ✨")
        else:
            print("💀 Wrong! Santa's weeping and the elves are on strike 💀")
    print()


if __name__ == "__main__":
  # Test parsing function
  data = read_and_parse_multicolumn_file(
    'data/test_data.txt',
    [int, None, int, int, None]
  )
  assert data[0] == [1, 'A', 23, 88, 'T']
  assert len(data) == 20
