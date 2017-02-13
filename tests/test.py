#!/usr/bin/env python3
# -*- coding: utf-8 -*_

import unittest

import testpath
import simple_markdown.table
import simple_markdown.table as Table


class test_markdown_table(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_format_ascii(self):
        raw_table = """\
|   Tables        | Are       | Cool  |
|:-------------|-------------|-----:|
 | col 1 is      | left-aligned                                    | $1600 |  
col 2 is      | centered|   $12  
  | zebra stripes |       | are neat   $1 |  
|| |$hello
|    $2 |"""

        raw_table_expected_0_0 = """\
|Tables       |    Are     |         Cool|
|:------------|:----------:|------------:|
|col 1 is     |left-aligned|        $1600|
|col 2 is     |  centered  |          $12|
|zebra stripes|            |are neat   $1|
|             |            |       $hello|
|$2           |            |             |"""

        raw_table_expected_2_2 = """\
|  Tables           |      Are       |           Cool    |
|:------------------|:--------------:|------------------:|
|  col 1 is         |  left-aligned  |          $1600    |
|  col 2 is         |    centered    |            $12    |
|  zebra stripes    |                |  are neat   $1    |
|                   |                |         $hello    |
|  $2               |                |                   |"""
        print("\n\nformatted with no padding / no margin:\n")
        table = Table.format(raw_table, margin=0, padding=0,
                             default_justify=Table.Justify.CENTER)
        print(table)
        self.assertEqual(table, raw_table_expected_0_0)

        table = Table.format(raw_table, margin=2, padding=2,
                             default_justify=Table.Justify.CENTER)
        print("\n\nformatted with padding 2 / margin 2:\n")
        print(table)
        self.assertEqual(table, raw_table_expected_2_2)


    def test_format_fullwidth(self):
        raw_table = """\
|   Tables        | Are       | Cool  |
:-------------|:-------------:|:-----|
 | col 1 is      | left-aligned                                    | $1600 |  
col 2 is      | centered|   $12  
  | zebra str|       |            are neat   $1 |  
|| |$hello
|    $2 |
| 业务方向      | 线人  |线人2       |
| 运营后台 - 销售 | 雪、鹏、丽 | 雪、
| 智能商业部     | 瑞         |  雪、"""

# 1 fullwidth < 2 normal with sublime text (it's ok in a terminal)
# 2 fullwidth = 4 normal
#　　ddd
#dddddd
#
#------------------------------------------------------------------------------
#　-----------------------------------------------------------------------------
#　　---------------------------------------------------------------------------
        raw_table_expected_0_0 = """\

|Ｔａｂｌｅｓ　　　　　　　|　　　　Ａｒｅ　　　　　|Ｃｏｏｌ　　　　　　　　　|
|:-------------------------|:----------------------:|:-------------------------|
|ｃｏｌ　１　ｉｓ　　　　　|ｌｅｆｔ－ａｌｉｇｎｅｄ|＄１６００　　　　　　　　|
|ｃｏｌ　２　ｉｓ　　　　　|　　ｃｅｎｔｅｒｅｄ　　|＄１２　　　　　　　　　　|
|ｚｅｂｒａ　ｓｔｒｉｐｅｓ|　　　　　　　　　　　　|ａｒｅ　ｎｅａｔ　　　＄１|
|　　　　　　　　　　　　　|　　　　　　　　　　　　|＄ｈｅｌｌｏ　　　　　　　|
|＄２　　　　　　　　　　　|　　　　　　　　　　　　|　　　　　　　　　　　　　|
|业务方向　　　　　　　　　|　　　　　线人　　　　　|线人２　　　　　　　　　　|
|运营后台　－　销售　　　　|　　　雪、鹏、丽　　　　|雪、　　　　　　　　　　　|
|智能商业部　　　　　　　　|　　　　　瑞　　　　　　|雪、　　　　　　　　　　　|"""

        raw_table_expected_2_2 = """\
|  Ｔａｂｌｅｓ　　　　　　　    |  　　　　Ａｒｅ　　　　　  |  Ｃｏｏｌ　　　　　　　　　    |
|:-----------------------------------|:------------------------------:|:-----------------------------------|
|  ｃｏｌ　１　ｉｓ　　　　　    |  ｌｅｆｔ－ａｌｉｇｎｅｄ  |  ＄１６００　　　　　　　　    |
|  ｃｏｌ　２　ｉｓ　　　　　    |  　　ｃｅｎｔｅｒｅｄ　　  |  ＄１２　　　　　　　　　　    |
|  ｚｅｂｒａ　ｓｔｒｉｐｅｓ    |  　　　　　　　　　　　　  |  ａｒｅ　ｎｅａｔ　　　＄１    |
|  　　　　　　　　　　　　　    |  　　　　　　　　　　　　  |  ＄ｈｅｌｌｏ　　　　　　　    |
|  ＄２　　　　　　　　　　　    |  　　　　　　　　　　　　  |  　　　　　　　　　　　　　    |
|  业务方向　　　　　　　　　    |  　　　　　线人　　　　　  |  线人２　　　　　　　　　　    |
|  运营后台　－　销售　　　　    |  　　　雪、鹏、丽　　　　  |  雪、　　　　　　　　　　　    |
|  智能商业部　　　　　　　　    |  　　　　　瑞　　　　　　  |  雪、　　　　　　　　　　　    |"""
        print("\n\nfullwidth formatted with no padding / no margin:\n")
        table = Table.format(raw_table, margin=0, padding=0,
                             default_justify=Table.Justify.CENTER)
        print(table)
        #self.assertEqual(table, raw_table_expected_0_0)

        table = Table.format(raw_table, margin=2, padding=2,
                             default_justify=Table.Justify.CENTER)
        print("\n\nfullwidth formatted with padding 2 / margin 2:\n")
        print(table)
        #self.assertEqual(table, raw_table_expected_2_2)

    def test_find_all(self):
        junk_tables = """
|   Tables        | Are       | Cool #1  |
|-------------|:-------------:|:-----|
 | col 3 is      | right-aligned | $1600 |  
col 2 is      ||   $12  
  | zebra stripes|are neat|    $1 |  
|| |$hello
|    $2 |

hellobar
fooworld
and junk

|   Tables        | Are       | Cool #2 |
|-------------|:-------------:|:-----|
 | col 3 is      | right-aligned | $1600 |  
col 2 is      ||   $12  
  | zebra stripes | are neat                                |    $1 |  
|| |$hello
|    $2 |

| ok | more | col | and more | col
|----|-----|--|----|---|--|-|-|-|
|ok | still good

junk junk junk
and some | to test |
if it's still working ||||||
is it?
"""
        offsets = simple_markdown.table.find_all(junk_tables)
        self.assertEqual(len(offsets), 3)

if __name__ == '__main__':
    unittest.main()
