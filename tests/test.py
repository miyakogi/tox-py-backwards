import unittest


def number(i: int, j: int) -> int:
    result: int = (i + j) * 1_000
    return result


def fstring(s: str) -> str:
    result: str = f'string: {s}'
    return result


class Test(unittest.TestCase):
    def test_number(self):
        self.assertEqual(number(1, 2), 3000)

    def test_fstring(self):
        self.assertEqual(fstring('a'), 'string: a')
