# -*- coding: utf-8 -*-
import re

import jctconv

import kansuji2arabic


def preprocess(string):
    string = re.sub('\(', '（', string)
    string = re.sub('\)', '）', string)
    string = re.sub(r'([0-9]),([0-9])', r'\1\2', string)
    return string


def convert_digit(string):
    """Convert kanji digit into arabic digit, considering context"""
    _KAN_SUJI = '〇一二三四五六七八九十百千万億兆'

    patterns = re.findall(r'[{0}]{{1,2}}月[{1}]{{1,2}}日'
                          .format(_KAN_SUJI, _KAN_SUJI), string)
    patterns += re.findall(r'(二〇[{0}]{{2}}年)'.format(_KAN_SUJI), string)
    patterns += re.findall(r'(一九[{0}]{{2}}年)'.format(_KAN_SUJI), string)
    patterns += re.findall(r'([ぁ-ん、。 　].年)', string)
    patterns += re.findall(r'([ぁ-ん、。　 ].月)', string)
    patterns += re.findall(r'([ぁ-ん、。　 ].日)', string)
    patterns += re.findall(r'(^.年[間半ぁ-ん])', string)
    patterns += re.findall(r'(^.月[間半ぁ-ん])', string)
    patterns += re.findall(r'(^.日[間半ぁ-ん])', string)
    patterns += re.findall(r'(年[{0}]{{1,2}}月)'.format(_KAN_SUJI), string)
    patterns += re.findall(r'[{0}]{{1,2}}時[^も]'.format(_KAN_SUJI), string)

    for p in patterns:
        string = re.sub(p, kansuji2arabic.trans(p), string)
    return string


def convert_expr(string):
    '''Convert certain expressions.'''

    pattern = re.compile(r'([たるの])所([^為感期見作載在産詮蔵属長定得有与用論])')
    while re.search(pattern, string) is not None:
        string = re.sub(pattern, r'\1ところ\2', string)

    pattern = re.compile(r'([^安先友伊上下闊用熟先送速伝調通到配発不])達([^さしすせそ筆者人磨摩])')
    while re.search(pattern, string) is not None:
        string = re.sub(pattern, r'\1たち\2', string)

    pattern = re.compile(r'出来([あ-ん、。])')
    while re.search(pattern, string) is not None:
        string = re.sub(pattern, r'でき\1', string)

    pattern = re.compile(r'([あ-ん])為([^政書替])')
    while re.search(pattern, string) is not None:
        string = re.sub(pattern, r'\1ため\2', string)

    pattern = re.compile(r'又([あ-ん、])')
    while re.search(pattern, string) is not None:
        string = re.sub(pattern, r'また\1', string)

    pattern = re.compile(r'何故')
    while re.search(pattern, string) is not None:
        string = re.sub(pattern, r'なぜ', string)

    pattern = re.compile(r'殊更')
    while re.search(pattern, string) is not None:
        string = re.sub(pattern, r'ことさら', string)

    pattern = re.compile(r'更に')
    while re.search(pattern, string) is not None:
        string = re.sub(pattern, r'さらに', string)

    pattern = re.compile(r'子供')
    while re.search(pattern, string) is not None:
        string = re.sub(pattern, r'子ども', string)

    pattern = re.compile(r'と共に')
    while re.search(pattern, string) is not None:
        string = re.sub(pattern, r'とともに', string)

    pattern = re.compile(r'^共に')
    while re.search(pattern, string) is not None:
        string = re.sub(pattern, r'ともに', string)

    replace_list = (('如何程', 'いかほど'),
                    ('其程', 'それほど'),
                    ('露程', 'つゆほど'),
                    ('余っ程', 'よっぽど'),
                    ('余程', 'よほど'),
                    ('後程', 'のちほど'),
                    ('程々', 'ほどほど'),
                    ('余程', 'よほど'),
                    ('＜', '〈'),
                    ('＞', '〉'))

    for (source, target) in replace_list:
        string = re.sub(source, target, string)

    return string


def convert_two_digit(string):
    '''convert two full-width digit into half width digit.'''

    patterns = re.findall(r'[^０-９][０-９]{2}[^０-９]', string)
    patterns += re.findall(r'^[０-９]{2}[^０-９]', string)
    for p in patterns:
        string = re.sub(p, jctconv.z2h(p, digit=True), string)
    return string


class Keep(object):
    '''Keep strings that should not be transformed.'''

    def __init__(self, exprs):
        self.exprs = exprs
        self.pairs = []

        for i, expr in enumerate(exprs):
            # unused unicode region as key
            # TODO: Do this more cleverly
            key = chr(int("e000", 16) + i)
            self.pairs.append((expr, key))

    def encode(self, string):
        for (expr, key) in self.pairs:
            string = re.sub(r'{0}'.format(expr), '{0}'.format(key), string)
        return string

    def restore(self, string):
        for (expr, key) in self.pairs:
            string = re.sub(r'{0}'.format(key), '{0}'.format(expr), string)
        return string


decorated_chars = [chr(i) for i in range(9312, 9472)]
tildes = list('\uff5e\u301c')
expressions_keep = list('“”、。‥…') + tildes + decorated_chars


def normalize(string):
    string = convert_expr(string)

    keep = Keep(expressions_keep)
    string = keep.encode(string)
    string = preprocess(string)
    string = convert_digit(string)
    string = jctconv.normalize(string, 'NFKC')
    string = jctconv.h2z(string, digit=True, ascii=True)
    string = convert_two_digit(string)
    string = keep.restore(string)

    return string


def main(string):
    lines = string.splitlines()
    rstr = ''
    for line in lines:
        rstr += normalize(line) + '\n'

    return rstr
