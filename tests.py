import unittest

from pconverter import normalize


class Test(unittest.TestCase):
    def test_normalize(self):
        strings = (('一昨年', '一昨年'),
                   ('三三五五', '三三五五'),
                   ('この三年', 'この３年'),
                   ('〜', '〜'),
                   ('“', '“'),
                   ('その程度', 'その程度'),
                   ('ｱ', 'ア'),
                   ('*', '＊'),
                   ('1', '１'),
                   ('12', '12'),
                   ('a12b', 'ａ12ｂ'),
                   ('ab', 'ａｂ'),
                   ('a', 'ａ')
                   )

        for source, result in strings:
            with self.subTest():
                self.assertEqual(result, normalize(source))


if __name__ == "__main__":
    unittest.main()
