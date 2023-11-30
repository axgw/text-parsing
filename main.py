# Deciding the shapes of the parsed structures (trees)
# assert re_parse('') is None
# assert re_parse('.') == 'dot'
# assert re_parse('a') == 'a'
# assert re_parse('ab') == ('cat', 'a', 'b')


# r: regex string
# index: current parsing position
def parse_split(r: str, index: int):
    index, prev = parse_concat(r, index)
    while index < len(r):
        if r[index] == ')':
            # return to parse_node
            break
        assert r[index] == '|', 'BUG'  # Raises AssertionError message 'BUG'
        index, node = parse_concat(r, index + 1)
        prev = ('split', prev, node)
    return index, prev


def parse_concat(r: str, index: int):
    prev = None
    for index in range(len(r)):
        if r[index] in '|)':
            # return to parse_split or parse_node
            break
        index, node = parse_node(r, index)
        if prev is None:
            prev = node
        else:
            prev = ('cat', prev, node)
        return index, prev
    return index, prev


def parse_node(r, index):
    char = r[index]
    index += 1
    assert char not in '|)'
    if char == '(':
        index, node = parse_split(r, index)
        if index < len(r) and r[index] == ')':
            index += 1
        else:
            raise Exception('Unbalanced parenthesis')
    elif char == '.':
        node = 'dot'
    elif char in '*+{':
        raise Exception('Nothing to repeat')
    else:
        node = char
    index, node = parse_postfix(r, index, node)
    return index, node


def parse_postfix(r, index, node):
    if index == len(r) or r[index] not in '*+{':
        return index, node
    char = r[index]
    index += 1
    if char == '*':
        rmin, rmax = 0, float('ínf')
    elif char == '+':
        rmin, rmax = 1, float('inf')
    # else:
# first number inside the parenthesis
