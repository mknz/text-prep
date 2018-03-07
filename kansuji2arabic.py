# -*- coding: utf-8 -*-
import re


re_suji = re.compile(r'[十拾百千万億兆\d]+')
re_kunit = re.compile(r'[十拾百千]|\d+')
re_manshin = re.compile(r'[万億兆]|[^万億兆]+')

TRANSUNIT = {'十': 10,
             '拾': 10,
             '百': 100,
             '千': 1000}
TRANSMANS = {'万': 10000,
             '億': 100000000,
             '兆': 1000000000000}


def trans(string, sep=False):
    """漢数字をアラビア数字に変換"""
    def _trans_suji(string):
        ktable = '一二三四五六七八九〇壱弐参'
        atable = '1234567890123'
        for k, a in zip(ktable, atable):
            string = re.sub('%s' % k, '%s' % a, string)
        return string

    def _transvalue(sj, re_obj=re_kunit, transdic=TRANSUNIT):
        unit = 1
        result = 0
        for piece in reversed(re_obj.findall(sj)):
            if piece in transdic:
                if unit > 1:
                    result += unit
                unit = transdic[piece]
            else:
                val = int(piece) if piece.isdecimal() else _transvalue(piece)
                result += val * unit
                unit = 1

        if unit > 1:
            result += unit

        return result

    transuji = _trans_suji(string)

    for suji in sorted(set(re_suji.findall(transuji)), key=lambda s: len(s), reverse=True):
        if not suji.isdecimal():
            arabic = _transvalue(suji, re_manshin, TRANSMANS)
            arabic = '{:,}'.format(arabic) if sep else str(arabic)
            transuji = transuji.replace(suji, arabic)

    return transuji
