# from lxml import etree
#
# XML = """
# <store>
#   <book id=1>Book 1</book>
#   <book id=2>Book 2</book>
# </store>
# <store>
#   <book id=3>Book 3</book>
#   <book id=4>Book 4</book>
# </store>
# """
#
#
# def test_xpath_index():
#     doc = etree.HTML(XML)
#     node = doc.xpath('//store')[0]
#     print(node.xpath('./book'))
#     print(node.xpath('./book[1]'))
#     print(node.xpath('./book[2]'))
#     print(node.xpath('./book[1]/@id'))
#     print(node.xpath('./book[2]/@id'))
#     print(node.xpath('./book[1]/text()'))
#     print(node.xpath('./book[2]/text()'))
#     assert 1 == 2
#
#
# MHTML = """
# <tr>
#   <td><a href='http://test.com/abc'>ABC</a></td>
#   <td><a href='http://test.com/abc1'>ABC1</a></td>
#   <td><a href='http://test.com/abc2'>ABC2</a></td>
# </tr>
# <tr>
#   <td><a href='http://test.com/def'>DEF</a></td>
#   <td><a href='http://test.com/def1'>DEF1</a></td>
#   <td><a href='http://test.com/def2'>DEF2</a></td>
# </tr>
# """
#
#
# def test_parse_tree_test():
#     doc = etree.HTML(MHTML)
#     node = doc.xpath('.//tr')[0]
#     link = node.xpath('/td[1]/a/@href')
#     link1 = node.xpath('/td/a[2]/@href')
#     name = node.xpath('/td/a[1]/text()')
#     name1 = node.xpath('/td/a[2]/text()')
#     name2 = node.xpath('/td/a[3]/text()')
#     assert link == 'http://test.com/abc'
#     assert link1 == 'http://test.com/abc1'
#     assert name == 'ABC'
#     assert name1 == 'ABC1'
#     assert name2 == 'ABC2'
#     assert 1 == 2
