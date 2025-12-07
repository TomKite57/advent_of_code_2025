
from typing import Final

import common

_DATA_FILE_NAME: Final = 'data/day_07.txt'
_START_TILE: Final = 'S'
_SPACE_TILE: Final = '.'
_SPLITTER_TILE: Final = '^'


class TachyonBeam:
  def __init__(
      self,
      tile_map: dict[complex, str],
  ):
    self._tile_map = tile_map
    self._find_starting_tile()
    self._grid_extent = common.get_grid_extent(self._tile_map)

    self._total_timeline_counts = 0
    self._splitters_hit = set()

    self._evolve_beam()

  def _find_starting_tile(self):
    self._start_pos = None
    for key, value in data.items():
      if value == _START_TILE:
        self._start_pos = key
        break
    if self._start_pos is None:
      raise ValueError("Could not find start tile")

  def _evolve_beam_one_step(
      self,
      position: complex
  ) -> list[complex]:
    one_down = position + common.COMPLEX_DOWN
    if one_down not in self._tile_map:
      return []
    tile_at_one_down = self._tile_map[one_down]
    if tile_at_one_down == _SPACE_TILE:
      return [one_down]
    if tile_at_one_down == _SPLITTER_TILE:
      self._splitters_hit.add(one_down)
      new_positions = [
        one_down+common.COMPLEX_LEFT,
        one_down+common.COMPLEX_RIGHT
      ]
      new_positions = [pos for pos in new_positions if pos in self._tile_map]
      return new_positions
    raise ValueError(f"Unexpected tile found {tile_at_one_down} at position {one_down}")

  def _evolve_beam(self):
    open_positions = common.SortedLookupList(
      [self._start_pos],
      sort_key=lambda x: int(x.imag)
    )
    timeline_lookup = {self._start_pos: 1}

    while open_positions._list:
      current_position = open_positions.pop()
      current_timelines = timeline_lookup[current_position]

      if int(current_position.imag) ==  self._grid_extent[2]:
        self._total_timeline_counts += current_timelines
        continue

      new_positions = self._evolve_beam_one_step(current_position)

      for new_pos in new_positions:
        if new_pos in open_positions:
          timeline_lookup[new_pos] += current_timelines
        else:
          timeline_lookup[new_pos] = current_timelines
          open_positions.add(new_pos)

  def get_split_count(self):
    return len(self._splitters_hit)

  def get_timeline_count(self):
    return self._total_timeline_counts


if __name__ == "__main__":
  aoc_manager = common.AdventOfCodeManager()
  data = common.read_and_parse_grid_to_dict(_DATA_FILE_NAME)
  part_1_sol = part_2_sol = 0

  beamline = TachyonBeam(data)
  part_1_sol = beamline.get_split_count()
  aoc_manager.submit_part_1(part_1_sol, expectation=1642)

  part_2_sol = beamline.get_timeline_count()
  aoc_manager.submit_part_2(part_2_sol, expectation=47274292756692)

  aoc_manager.show()
