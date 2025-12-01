
from typing import Callable, Any, Final, Sequence, TypeVar

_IDENTITY: Final = lambda x: x
_T = TypeVar('_T')

def read_and_parse_file(
    file_name: str,
    parse_fn: Callable[[str], Any] = lambda x: x
):
  with open(file_name, 'r') as open_file:
    data = [parse_fn(line.strip()) for line in open_file]
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
