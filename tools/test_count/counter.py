#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ishii.y'

import os
import sys
import fnmatch
import csv
import datetime


def main():
    #target_dir = r'C:\sqllogictest\test2\evidence\in1.test'
    #target_dir = r'C:\sqllogictest\test2\evidence\in2.test'
    #target_dir = r'C:\sqllogictest\test\select2.test'
    target_dir = r'C:\sqllogictest\test2'
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    target_db = 'drsum'
    if len(sys.argv) > 2:
        target_db = sys.argv[2]
    output_dir = '.'
    if len(sys.argv) > 3:
        output_dir = sys.argv[3]

    get_file_info(target_dir, target_db, output_dir)


def get_file_info(target_dir, target_db, output_dir):
    """
    対象ファイル群のステートメント情報を取得する
    :param target_dir:
    :return:
    """
    total = 0
    count = 0
    res = []
    for file_name in get_file_list(target_dir, '*.test'):
        test = TestFile(file_name)
        test.write_csv(target_db, make_output_file_name(target_dir, file_name, output_dir))
        case_sum = test.case_summary(target_db)
        res.append((file_name, case_sum))
        #for s in test.statements:
        #    print s.file_name, s.row_num, s.type + ',' + s.skipif + ',' + s.onlyif + ',' + str(s.is_valid(target_db)) + ',' + s.test_result + ','+ s.test_msg
        count += 1
        total += case_sum['valid_case']
        print count, file_name, case_sum

    write_summary_csv(output_dir, res)
    print count, total


def make_output_file_name(target_dir, file_name, output_dir):
    #出力するCSV名の生成
    #target_dirをルートとするパスを'_'でつなぐ
    root_dir = target_dir
    if os.path.isfile(target_dir):
        root_dir = os.path.dirname(target_dir)
    rel_path = file_name.replace(root_dir + '\\', '')
    rel_path = rel_path.replace('\\', '-')
    return output_dir + '/' + rel_path + '.csv'


def write_summary_csv(output_dir, res, encode='cp932'):
    """
    テスト全体のサマリーを出力
    :param output_dir:
    :param res:
    :param encode:
    :return:
    """
    output_file_name = output_dir + '\summary.csv'
    date = datetime.datetime.today()
    date_str = '%04d/%02d/%02d' % (date.year, date.month, date.day)

    with open(output_file_name, 'w') as f:
        write_csv = csv.writer(f, lineterminator='\n', quotechar='"', quoting=csv.QUOTE_ALL)
        write_csv.writerow(['day', 'file_name', 'total', 'skip_case', 'valid_case', 'ok_case', 'ng_case'])
        for r in res:
            write_csv.writerow(
                [date_str,
                 r[0].encode(encode),
                 r[1]['total'],
                 r[1]['skip_case'],
                 r[1]['valid_case'],
                 r[1]['ok_case'],
                 r[1]['ng_case']
                 ]
            )


def get_file_list(target_dir, pattern):
    """
    指定ディレクトリから指定パターンのファイルリストを再帰的に取得。
    :param target_dir:ターゲットディレクトリまたはファイル
    :param pattern:ファイルパターン
    :return:
    """
    #ファイル名の場合は、そのまま返す
    if os.path.isfile(target_dir):
        yield target_dir

    #ディレクトリ内を再帰的に探索
    for root, dirs, files in os.walk(target_dir):
        for file_name in files:
            if fnmatch.fnmatch(file_name, pattern):
                yield os.path.join(root, file_name)


class TestFile:
    def __init__(self, file_name):
        self.file_name = file_name

        #テスト実行結果ファイルの有無
        result_file_name = file_name + '_res'
        tested = os.path.exists(result_file_name)
        test_results = self.get_test_result(result_file_name)

        self.statements = self.get_statements(file_name, tested, test_results)

    @classmethod
    def get_statements(cls, file_name, tested, test_results):
        """
        ファイルを読み込んでステートメント毎に分割して取得する。
        """
        statements = []
        halt = []
        with open(file_name, 'r') as f:
            started = False
            block = []
            for i, line in enumerate(f, 1):
                if cls.is_comment(line):
                    #コメント行は無条件でスキップ
                    continue
                if started is False and cls.is_blank(line):
                    #未スタートで、空行の場合はスキップ
                    continue
                if started and cls.is_blank(line):
                    #1ブロック終了
                    s = Statement(file_name, block, tested, test_results, halt)
                    statements.append(s)
                    if s.type == 'halt':
                        if s.skipif != '':
                            halt.append(('s', s.skipif))
                        if s.onlyif != '':
                            halt.append(('o', s.onlyif))
                    block = []
                    started = False
                    continue
                started = True
                block.append((i, line))

            if len(block) > 0:
                statements.append(Statement(file_name, block, tested, test_results, halt))
        return statements

    @classmethod
    def is_blank(cls, line):
        return len(line.strip()) == 0

    @classmethod
    def is_comment(cls, line):
        return line.find('#') == 0

    @classmethod
    def get_test_result(cls, file_name):
        """
        エラー情報を取得して、行数をインデックスとした連想配列で返す。
        """
        res = {}
        if os.path.exists(file_name) is False:
            return res
        with open(file_name, 'r') as f:
            for line in f:
                row, msg = cls.get_err_info(line)
                if row < 0:
                    continue
                res[row] = msg
        return res

    @classmethod
    def get_err_info(cls, line):
        """
        トークンからエラー情報を返す。
        エラー情報じゃない場合は行数に-1を入れる。
        :param tokens:
        :return:(行数, 内容)
        """

        #':'で分割して3つに分かれていて、かつ2番目が数値ならエラー情報とみなす。
        tokens = [x.strip() for x in line.strip().split(':')]
        if len(tokens) == 3 and tokens[1].isdigit():
            return int(tokens[1]), tokens[2]

        if len(tokens) == 4:
            #絶対パスの場合、（:)がずれる可能性あり。
            if len(tokens[0]) == 1 and tokens[1].find('\\') == 0:
                if tokens[2].isdigit():
                    return int(tokens[2]), tokens[3]
        return -1, ''

    def case_summary(self, db_name=''):
        """
        テストケースのサマリーを返す。
        :param db_name:
        :return:
        """
        valid_case = 0
        skip_case = 0
        ok_case = 0
        ng_case = 0
        for x in self.statements:
            if x.is_valid(db_name) is False:
                skip_case += 1
                continue
            valid_case += 1
            if x.test_result == 'x':
                ng_case += 1
            elif x.test_result == 'o':
                ok_case += 1
        total = skip_case + valid_case
        return {'total': total,
                'valid_case': valid_case,
                'skip_case': skip_case,
                'ok_case': ok_case,
                'ng_case': ng_case}

    def write_csv(self, db_name, output_file_name, encode='cp932'):
        """
        ファイル内のステートメント情報をCSVに出力する。
        """
        with open(output_file_name, 'w') as f:
            write_csv = csv.writer(f, lineterminator='\n', quotechar='"', quoting=csv.QUOTE_ALL)
            write_csv.writerow(Statement.get_csv_header())
            for s in self.statements:
                write_csv.writerow(s.get_result_as_list(db_name, encode))


class Statement:
    """
    ステートメント情報を格納する
    """
    def __init__(self, file_name, block, tested, test_results, halt):
        if len(block) == 0:
            raise ValueError("no statement block.")
        self.file_name = file_name
        self.halt = list(halt)

        self.row_num = 0
        self.end_row_num = 0
        self.type = ''
        self.skipif = []
        self.onlyif = []
        self.statement = ''
        self.test_result = '-'
        self.test_msg = ''

        #ステートメント情報を取得
        self.set_param(block)

        #テスト結果がある場合は結果を取得
        if tested:
            self.set_test_result(test_results)

    def set_param(self, block):
        """
        blockから、テスト情報を各メンバーにセットする。
        :param block:ステートメントの1ブロック
        :param test_results:対象ファイルのテスト結果の一覧
        :return:
        """
        self.row_num = block[0][0]
        self.end_row_num = block[len(block)-1][0]

        #スキップ情報を取得
        cur = 0
        s = block[cur][1].strip()
        while s.find('onlyif') == 0 or s.find('skipif') == 0:
            if s.find('onlyif') == 0:
                self.onlyif.append(s.split(' ')[1])
            elif s.find('skipif') == 0:
                self.skipif.append(s.split(' ')[1])
            cur += 1
            s = block[cur][1].strip()

        #ステートメントのタイプを取得
        if s.find('statement') == 0:
            self.type = 'statement'
        elif s.find('query') == 0:
            self.type = 'query'
        elif s.find('halt') == 0:
            self.type = 'halt'
        elif s.find('hash-threshold') == 0:
            self.type = 'hash'
        else:
            self.type = 'unknown'

        #ステートメントを格納
        cur += 1
        for x in block[cur:]:
            self.statement += x[1]

    def set_test_result(self, test_results):
        #テスト実施結果
        self.test_result = 'o'  # とりあえず全ケースOKとする。
        #エラー情報取得
        for i in range(self.row_num, self.end_row_num+1):
            if i in test_results:
                self.test_result = 'x'
                self.test_msg = test_results[i]
                break

    def get_test_result(self, db_name=''):
        """
        テスト結果を返す。スキップしたものを判別するため、DB名を引数に取る。
        :param db_name:空の場合は全ケースを実施したとみなす。
        :return:
        """
        if self.is_valid(db_name):
            return self.test_result
        return '-'

    def is_valid(self, db_name=''):
        """
        本ステートメントがDB名に対して有効なケースか否かの判定
        :param db_name: 空の場合は全ケースが有効
        :return:
        """
        if self.type != 'query' and self.type != 'statement':
            #query, statement以外はFalse
            return False

        if db_name == '':
            #db_nameが空なら全てのケースをvalidとする。
            return True

        #haltの判定
        if self.is_halt(db_name):
            return False

        if len(self.skipif) == 0 and len(self.onlyif) == 0:
            #skip/onlyifが両方なければ有効
            return True
        if len(self.onlyif) > 0 and db_name in self.onlyif:
            #onlyifが対象DB名なら有効
            return True
        if len(self.skipif) > 0 and db_name not in self.skipif:
            #skipifが対象DBじゃなければ有効
            return True

        return False

    def is_halt(self, db_name):
        for h in self.halt:
            if h[0] == 'o' and db_name in h[1]:
                return True
            if h[0] == 's' and db_name not in h[1]:
                return True
        return False

    def statement_one_line(self):
        #ステートメントの改行を半角スペースに置き換えて1行にする。
        return self.statement.replace('\n', ' ')

    @classmethod
    def get_csv_header(cls):
        """
        ヘッダーをリストで返す。CSV出力用。
        :return:
        """
        return [
            'day',
            'file_name',
            'row_num',
            'type',
            'skipif',
            'onlyif',
            'test_result',
            'test_msg',
            'statement'
        ]

    def get_result_as_list(self, db_name, encode):
        """
        メンバー情報をリストで返す。CSV出力用。
        :param encode:
        :return:
        """
        date = datetime.datetime.today()
        date_str = '%04d/%02d/%02d' % (date.year, date.month, date.day)
        return [
            date_str,
            self.file_name.encode(encode),
            str(self.row_num),
            self.type.encode(encode),
            ','.join(self.skipif).encode(encode),
            ','.join(self.onlyif).encode(encode),
            self.get_test_result(db_name),
            self.test_msg.encode(encode),
            self.statement_one_line().encode(encode)
        ]


if __name__ == '__main__':
    main()