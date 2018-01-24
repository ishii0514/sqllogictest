#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import fnmatch
import re

__author__ = 'ishii.y'


def main():
    target_dir = r'd:\sqllogictest\test_ea'
    # target_dir = r'd:\sqllogictest\test_ea\select2.test'
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    output_dir = r'd:\sqllogictest\test_ea2'
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]

    for file_name in get_file_list(target_dir, '*.test'):
        rewrite(file_name, get_output_file(file_name, target_dir, output_dir))


def get_output_file(file_name, target_dir, output_dir):
    if os.path.isfile(target_dir):
        # ファイルの場合、ディレクトリ全体を差し替える
        return os.path.join(output_dir, os.path.basename(target_dir))
    # ディレクトリの場合、rootディレクトリ部分を差し替える
    return file_name.replace(target_dir, output_dir)


def rewrite(file_name, output_file_name):
    """
    指定されたファイルのSQLをリライトして書き出す
    :param file_name:
    :param output_file_name
    :return:
    """
    replace_ope_num = get_replace_ope_num()

    # なければ作る
    output_dir = os.path.dirname(output_file_name)
    if os.path.isdir(output_dir) is False:
        os.makedirs(output_dir)

    wf = open(output_file_name, 'w')
    with open(file_name, 'r') as rf:
        for s in get_statement(rf):
            wf.write(rewrite_stmt(s, replace_ope_num))
    wf.close()


def rewrite_stmt(stmt, replace_ope_num):
    """
    渡されたステートメントを書き換える
    :param stmt:
    :param replace_ope_num:
    :return:
    """
    res = replace_ope_num(stmt)
    res = add_dw(res)
    return res


def get_statement(f):
    """
    ステートメントを取得する。
    SELECTが複数行にまたがるため。
    :param f:
    :return:
    """
    tmp = ''
    end_stmt = '----'
    for buff in f:
        if len(tmp) == 0 and buff.find('SELECT') != 0:
            yield buff
            continue
        if buff.find(end_stmt) == 0:
            yield tmp
            yield buff
            tmp = ''
            continue
        tmp += buff
    if len(tmp) > 0:
        yield tmp


def get_replace_ope_num():
    """
    +-符号と数値の間にある空白を除去する関数を返す
    :return:
    """
    p = re.compile('[+-] [0-9]')
    return lambda stmt: p.sub(lambda m: m.group().replace(' ', ''), stmt)


def add_dw(stmt):
    """
    from句のないselect文に from __dw__を追加する。
    サブクエリーなどselectが2つ以上ある場合は対応しない。
    :param stmt:
    :return:
    """
    if stmt.find('SELECT') == 0 and stmt.count('SELECT') == 1 and stmt.count('FROM') == 0:
        from_dw = ' FROM __dw__'
        # 末尾の改行を付け替える
        if stmt[len(stmt)-1] == '\n':
            return stmt[:len(stmt)-1] + from_dw + '\n'
        return stmt + from_dw
    return stmt


def get_file_list(target_dir, pattern):
    """
    指定ディレクトリから指定パターンのファイルリストを再帰的に取得。
    :param target_dir:ターゲットディレクトリまたはファイル
    :param pattern:ファイルパターン
    :return:
    """
    # ファイル名の場合は、そのまま返す
    if os.path.isfile(target_dir):
        yield target_dir

    # ディレクトリ内を再帰的に探索
    for root, dirs, files in os.walk(target_dir):
        for file_name in files:
            if fnmatch.fnmatch(file_name, pattern):
                yield os.path.join(root, file_name)

if __name__ == '__main__':
    main()
