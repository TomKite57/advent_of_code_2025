
from typing import Callable, Any, Final, Sequence, TypeVar, Iterable
import time
from collections import defaultdict
import bisect

_IDENTITY: Final = lambda x: x
_T = TypeVar('_T')
COMPLEX_DOWN = (-1j)
COMPLEX_UP = (1j)
COMPLEX_LEFT = (-1+0j)
COMPLEX_RIGHT = (1+0j)


def read_raw_file(
    file_name: str
) -> str:
  with open(file_name, 'r') as open_file:
    return open_file.read()


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
    separator: str | None = None,
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
        line = line.strip()
        for col, char in enumerate(line):
          pos = col - row*1j
          map_content_by_coord[pos] = char
  return map_content_by_coord


def get_complex_directions(
    *,
    include_diagonals=False
) -> Iterable[complex]:
   yield from (1, 1j, -1, -1j)
   if include_diagonals:
      yield from (1+1j, 1-1j, -1+1j, -1-1j)


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


class AdventOfCodeManager:
  def __init__(self):
    self.start_time = time.perf_counter()
    self.part_1_solution = None
    self.part_2_solution = None

  def submit_part_1(
      self,
      solution: _T,
      expectation: _T | None = None
  ):
    if self.part_1_solution is not None:
      raise ValueError("Part 1 time already set. Did you mean part_2_checkpoint?")
    self.part_1_solution = (solution, expectation, time.perf_counter())

  def submit_part_2(
      self,
      solution: _T,
      expectation: _T | None = None
  ):
    if self.part_2_solution is not None:
      raise ValueError("Part 2 time already set. Did you mean part_1_checkpoint?")
    if self.part_1_solution is None:
      raise ValueError("Part 1 not set. Did you mean part_1_checkpoint?")
    self.part_2_solution = (solution, expectation, time.perf_counter())


  def show(self):
    if self.part_1_solution is not None:
      pretty_format_and_maybe_check(
        self.part_1_solution[0],
        1,
        self.part_1_solution[1]
      )
    if self.part_2_solution is not None:
      pretty_format_and_maybe_check(
        self.part_2_solution[0],
        2,
        self.part_2_solution[1]
      )

    if self.part_1_solution is not None:
      part_1_delta = self.part_1_solution[2] - self.start_time
      print(f"Part 1 took {part_1_delta:.3f} s")
    if self.part_2_solution is not None:
      part_2_delta = self.part_2_solution[2] - self.part_1_solution[2]
      print(f"Part 2 took {part_2_delta:.3f} s")


def get_grid_extent(
    tile_map: dict[complex, Any]
) -> tuple[int, int, int, int]:
  all_keys = list(tile_map.keys())
  return (
    min(int(x.real) for x in all_keys),
    max(int(x.real) for x in all_keys),
    min(int(x.imag) for x in all_keys),
    max(int(x.imag) for x in all_keys),
  )


def print_complex_grid(
    tile_map: dict[complex, Any]
):
  grid_extent = get_grid_extent(tile_map)
  max_element_extent = max(len(str(elem)) for elem in tile_map.values())
  padding = int(max_element_extent > 1)
  for y in range(grid_extent[3], grid_extent[2]-1, -1):
    for x in range(grid_extent[0], grid_extent[1]+1):
      string = str(tile_map[x+y*1j])
      string = ''.join((string, ' '*(max_element_extent-len(string)+padding)))
      print(string, end='')
    print()


class SortedLookupList:
  def __init__(
      self,
      elements: Sequence[_T],
      sort_key: Callable[[_T], int] | None = None,
      allow_duplicates: bool = False
  ):
    self._list = list(elements)
    self._counts = defaultdict(lambda: 0)
    for elem in self._list:
      self._counts[elem] += 1

    self._sort_key = sort_key
    self._allow_duplicates = allow_duplicates
    self._sort()

  def _sort(self):
    self._list = sorted(self._list, key=self._sort_key)

  def add(self, element: _T):
    if not self._allow_duplicates and self._counts[element] > 1:
      raise ValueError(f"Element {element} already in container")
    bisect.insort(self._list, element, key=self._sort_key)
    self._counts[element] += 1

  def pop(self, index: int = -1):
    element = self._list.pop(index)
    self._counts[element] -= 1
    return element

  def __contains__(self, element: _T):
    return element in self._counts


if __name__ == "__main__":
  # Test parsing function
  data = read_and_parse_multicolumn_file(
    'data/test_data.txt',
    [int, None, int, int, None]
  )
  assert data[0] == [1, 'A', 23, 88, 'T']
  assert len(data) == 20
