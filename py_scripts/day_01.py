
from typing import Final

import common

_DATA_FILE_NAME: Final = 'data/day_01.txt'


if __name__ == "__main__":
  data = common.read_and_parse_multicolumn_file(_DATA_FILE_NAME, [int, int])
  part_1_sol, part_2_sol = "TBD", "TBD"


  common.pretty_format_and_maybe_check(
    answer=part_1_sol,
    part=1,
    expectation=None
  )


  common.pretty_format_and_maybe_check(
    answer=part_2_sol,
    part=2,
    expectation=None
  )
