#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import rewrite_sql

__author__ = 'ishii.y'


class RewriteSQLTest(unittest.TestCase):
    def test_ope_num(self):
        f = rewrite_sql.get_replace_ope_num()
        self.assertEqual(f('- col1'), '- col1')
        self.assertEqual(f('+ col1'), '+ col1')
        self.assertEqual(f('- 6'), '-6')
        self.assertEqual(f('+ 0'), '+0')
        self.assertEqual(f('* 6'), '* 6')
        self.assertEqual(f('/ 0'), '/ 0')
        self.assertEqual(f('abc + 9 - 3'), 'abc +9 -3')
        self.assertEqual(f('- + 9 - 3'), '- +9 -3')
        self.assertEqual(f('- * 9 / 3'), '- * 9 / 3')
        self.assertEqual(f('+9 -3'), '+9 -3')
        self.assertEqual(f('abc * + 12.6 - - 0.1 aaa'), 'abc * +12.6 - -0.1 aaa')
        self.assertEqual(f('SELECT DISTINCT + MAX(DISTINCT - + 68) AS col0, - MIN(- 50) AS col0'), 'SELECT DISTINCT + MAX(DISTINCT - +68) AS col0, - MIN(-50) AS col0')

    def test_add_dw(self):
        self.assertEqual(rewrite_sql.add_dw('SELECT col1 + col2'), 'SELECT col1 + col2 FROM __dw__')
        self.assertEqual(rewrite_sql.add_dw('SELECT col1 + col2 FROM x WHERE z=2'), 'SELECT col1 + col2 FROM x WHERE z=2')

    def test_get_statement(self):
        s = ['SELECT CAST ( NULL AS REAL ) * + 16',
             '----',
             'NULL',
             ]

        res = []
        for item in rewrite_sql.get_statement(s):
            res.append(item)
        self.assertEqual(len(res), 3)
        self.assertEqual(res[0], 'SELECT CAST ( NULL AS REAL ) * + 16')
        self.assertEqual(res[1], '----')
        self.assertEqual(res[2], 'NULL')

        s = [
             'SELECT a+b*2+c*3+d*4+e*5',
             '  FROM t1',
             ' WHERE (a>b-2 AND a<b+2)',
             '    OR d NOT BETWEEN 110 AND 150',
             '    OR EXISTS(SELECT 1 FROM t1 AS x WHERE x.b<t1.b)',
             '----',
             '29 values hashing to 67079c1a773f2fc4382618135f2e0719']

        res = []
        for item in rewrite_sql.get_statement(s):
            res.append(item)
        self.assertEqual(len(res), 3)
        self.assertEqual(res[0],
                         'SELECT a+b*2+c*3+d*4+e*5  FROM t1 WHERE (a>b-2 AND a<b+2)    OR d NOT BETWEEN 110 AND 150    OR EXISTS(SELECT 1 FROM t1 AS x WHERE x.b<t1.b)')
        self.assertEqual(res[1], '----')
        self.assertEqual(res[2], '29 values hashing to 67079c1a773f2fc4382618135f2e0719')

        s = ['skipif mysql # not compatible',
             'query I rowsort label-9996',
             'SELECT CAST ( NULL AS REAL ) * + 16',
             '----',
             'NULL',
             '',
             'SELECT a+b*2+c*3+d*4+e*5',
             '  FROM t1',
             ' WHERE (a>b-2 AND a<b+2)',
             '    OR d NOT BETWEEN 110 AND 150',
             '    OR EXISTS(SELECT 1 FROM t1 AS x WHERE x.b<t1.b)',
             '----',
             '29 values hashing to 67079c1a773f2fc4382618135f2e0719',
             'SELECT * test']
        res = []
        for item in rewrite_sql.get_statement(s):
            res.append(item)
        self.assertEqual(len(res), 10)
        self.assertEqual(res[0], 'skipif mysql # not compatible')
        self.assertEqual(res[1], 'query I rowsort label-9996')
        self.assertEqual(res[2], 'SELECT CAST ( NULL AS REAL ) * + 16')
        self.assertEqual(res[3], '----')
        self.assertEqual(res[4], 'NULL')
        self.assertEqual(res[5], '')
        self.assertEqual(res[6], 'SELECT a+b*2+c*3+d*4+e*5  FROM t1 WHERE (a>b-2 AND a<b+2)    OR d NOT BETWEEN 110 AND 150    OR EXISTS(SELECT 1 FROM t1 AS x WHERE x.b<t1.b)')
        self.assertEqual(res[7], '----')
        self.assertEqual(res[8], '29 values hashing to 67079c1a773f2fc4382618135f2e0719')
        self.assertEqual(res[9], 'SELECT * test')

    def test_rewrite_stmt(self):
        f = rewrite_sql.get_replace_ope_num()
        self.assertEqual(rewrite_sql.rewrite_stmt('SELECT 9 + 2', f), 'SELECT 9 +2 FROM __dw__')
        self.assertEqual(rewrite_sql.rewrite_stmt('SELECT 9 + 2 FROM t1', f), 'SELECT 9 +2 FROM t1')
        self.assertEqual(rewrite_sql.rewrite_stmt('SELECT 9 + 2, (SELECT 1) AS a', f), 'SELECT 9 +2, (SELECT 1) AS a')

        self.assertEqual(rewrite_sql.rewrite_stmt('SELECT 9 + 2\n', f), 'SELECT 9 +2 FROM __dw__\n')
        self.assertEqual(rewrite_sql.rewrite_stmt('SELECT 9 + 2\n IN(a,b,c) \n', f), 'SELECT 9 +2\n IN(a,b,c)  FROM __dw__\n')

if __name__ == '__main__':
    unittest.main()
