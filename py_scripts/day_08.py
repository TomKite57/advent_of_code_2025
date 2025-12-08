
from typing import Final, NewType, Sequence
from collections import defaultdict

import common

_DATA_FILE_NAME: Final = 'data/day_08.txt'
_NUM_PAIRS_TO_CONNECT: Final = 1000

Coord = NewType("Coord", tuple[int, int, int])
IntMatrix = NewType("IntMatrix", list[list[int]])


def square_distance(coord_a: Coord, coord_b: Coord) -> int:
  return sum((a-b)**2 for a, b in zip(coord_a, coord_b, strict=True))


def build_distance_pairs(coords: Sequence[Coord]) -> list[tuple[int, int, int]]:
  pairs_and_distances: list[tuple[int, int, int]] = []
  for i, coord_i in enumerate(coords):
    for j, coord_j in enumerate(coords):
      if j >= i:
        break
      distance = square_distance(coord_i, coord_j)
      pairs_and_distances.append((j, i, distance))
  return pairs_and_distances


def get_island_sizes(
    num_coords: int,
    connected_pairs: Sequence[tuple[int, int, int]]
):
  all_coords = list(range(num_coords))
  already_seen = set()
  pair_dict = defaultdict(list)
  for i, j, _ in connected_pairs:
    pair_dict[i].append(j)
    pair_dict[j].append(i)
  island_sizes = []

  while all_coords:
    new_coord = all_coords.pop()
    if new_coord in already_seen:
      continue

    already_seen.add(new_coord)
    island_size = 1
    to_explore = pair_dict[new_coord]
    while to_explore:
      explore_coord = to_explore.pop()
      if explore_coord in already_seen:
        continue
      already_seen.add(explore_coord)
      island_size += 1
      to_explore.extend(pair_dict[explore_coord])
    island_sizes.append(island_size)

  return island_sizes


if __name__ == "__main__":
  aoc_manager = common.AdventOfCodeManager()
  data = common.read_and_parse_multicolumn_file(
    _DATA_FILE_NAME,
    [int, int, int],
    separator=','
  )
  data = [tuple(coord) for coord in data]
  part_1_sol = part_2_sol = 0

  distance_pairs = build_distance_pairs(data)
  distance_pairs = sorted(distance_pairs, key=lambda x: x[2])
  connected_pairs = distance_pairs[:_NUM_PAIRS_TO_CONNECT]
  island_sizes = get_island_sizes(len(data), connected_pairs)
  island_sizes = sorted(island_sizes, reverse=True)

  part_1_sol = island_sizes[0]*island_sizes[1]*island_sizes[2]
  aoc_manager.submit_part_1(part_1_sol, expectation=50568)

  num_connections = _NUM_PAIRS_TO_CONNECT
  while len(island_sizes) > 1:
    num_connections = num_connections + len(island_sizes) - 1
    connected_pairs = distance_pairs[:num_connections]
    island_sizes = get_island_sizes(len(data), connected_pairs)
  final_connection = connected_pairs[-1]
  part_2_sol = (
    data[final_connection[0]][0] *
    data[final_connection[1]][0]
  )
  aoc_manager.submit_part_2(part_2_sol, expectation=None)

  aoc_manager.show()
