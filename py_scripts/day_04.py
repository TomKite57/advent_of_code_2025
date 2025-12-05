
from typing import Final, Mapping

import common

_DATA_FILE_NAME: Final = 'data/day_04.txt'
_PAPER_TILE: Final = '@'
_FLOOR_TILE: Final = '.'


def is_paper_accessible(
    factory_map: Mapping[complex, str],
    query_position: complex
):
  if factory_map[query_position] != _PAPER_TILE:
    return False

  adjacent_paper_count = 0
  for delta in common.get_complex_directions(include_diagonals=True):
    adjacent_paper_count += int(factory_map.get(query_position+delta, _FLOOR_TILE) == _PAPER_TILE)
  return adjacent_paper_count < 4


def remove_accesible_paper(
    factory_map: Mapping[complex, str],
):
  remaining_paper_positions = set((pos for pos in factory_map.keys() if factory_map[pos]==_PAPER_TILE))
  coords_to_check_next_iter = remaining_paper_positions
  while True:
    new_coords_to_remove = [
      pos for pos in coords_to_check_next_iter
      if is_paper_accessible(factory_map, pos)
    ]
    if not new_coords_to_remove:
      return factory_map

    coords_to_check_next_iter = set()
    for pos in new_coords_to_remove:
      factory_map[pos] = _FLOOR_TILE
      remaining_paper_positions.remove(pos)
      for delta in common.get_complex_directions(include_diagonals=True):
        new_pos = pos+delta
        if new_pos in remaining_paper_positions:
          coords_to_check_next_iter.add(new_pos)


if __name__ == "__main__":
  aoc_manager = common.AdventOfCodeManager()

  data = common.read_and_parse_grid_to_dict(_DATA_FILE_NAME)
  part_1_sol = part_2_sol = 0

  part_1_sol = sum(is_paper_accessible(data, pos) for pos in data.keys())
  aoc_manager.submit_part_1(part_1_sol, expectation=1602)

  starting_paper_count = sum(char==_PAPER_TILE for char in data.values())
  data_after_paper_removal = remove_accesible_paper(data)
  ending_paper_count = sum(char==_PAPER_TILE for char in data_after_paper_removal.values())
  part_2_sol = starting_paper_count - ending_paper_count
  aoc_manager.submit_part_2(part_2_sol, expectation=9518)

  aoc_manager.show()
