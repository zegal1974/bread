import re
from lxml import etree


def get_number(text: str, default=0) -> int:
    """ 转化字符串为整型，忽略后缀的其它字符
    """
    m = re.search('([0-9]+)', text)
    if m:
        return int(m.group(1))
    return default


def get_date(text: str) -> str:
    m = re.search(r"([0-9-]+)", text)
    if m:
        return m.group(1)
    return ""


def get_id(link: str) -> str:
    """ Get the actor's gid or movie's code etc.
        :param link: BeautifulSoup document of the link
    """
    return link.split('/')[-1]


DEFAULT_IMAGE_FILENAME = 'nowprinting.gif'


def get_pic(link: str) -> str | None:
    """ Get the actor's gid or movie's code etc.
        :param link: BeautifulSoup document of the link
    """
    pic = link.split('/')[-1]
    if pic == DEFAULT_IMAGE_FILENAME:
        return None
    return pic


FORMAT_SETTINGS = {
    'id': get_id,
    'avatar': get_pic,
    'number': get_number,
    'date': get_date,
}

ns = etree.FunctionNamespace(None)


@ns
def match(context, regex):
    text = etree.tostring(context.context_node, encoding='unicode')
    # print(text)
    res = re.search(regex, text)
    if res:
        return res.group(1)
    return None


@ns
def get_id(context):
    link = context.context_node.get('href')
    return link.split('/')[-1]


def parse_html(doc, conf: dict) -> dict:
    ret = {}
    for key, config in conf:
        if key == 'model':
            result = parse_element(doc, config['fields'])
        elif key == 'models':
            result = parse_tree(doc, config['fields'])

        ret[config['name']] = result

    return ret


def parse_tree(doc, conf: dict):
    children = doc.xpath(conf['xpath'])
    # print(children)
    res = []
    if not 'fields' in conf:
        return None  # TODO：Arguments Error
    for child in children:
        node = parse_element(child, conf['fields'])
        # print(node)
        if len(node.items()) > 0:
            res.append(node)
    return res


def parse_element(doc, conf: list):
    node = {}
    for field in conf:
        find = etree.XPath(field['xpath'])
        res = find(doc)
        if len(res) == 0:
            continue

        print(field['name'], res[0])
        if 'select' in field:
            node[field['name']] = res[0].xpath(field['select']).strip()
        # elif 'modifier' in field:

        else:
            node[field['name']] = res[0].strip()

    return node
