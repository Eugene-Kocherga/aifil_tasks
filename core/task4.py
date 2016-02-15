class SimpleList:
    def __init__(self, value):
        self.value = value
        self.next = None

    def append(self, node):
        if self.next:
            self.next.append(node)
        else:
            self.next = node

def simple_range(start, end=None):
    if end is None:
        end = start
        start = 0
    head = SimpleList(start)
    for i in range(start+1, end):
        head.append(SimpleList(i))
    return head

def simple_to_list(simple_list):
    node = simple_list
    result = list()
    if node:
        result.append(node.value)
        while node.next:
            node = node.next
            result.append(node.value)
    return result

def list_to_simple(normal_list):
    if not normal_list:
        return None
    head = SimpleList(normal_list[0])
    for val in normal_list[1:]:
        head.append(SimpleList(val))
    return head

def repack_recursive(simple_list):
    def pop(simple_list):
        if not simple_list.next:
            return simple_list, True
        node = simple_list
        while node.next.next:
            node = node.next
        last = node.next
        node.next = None
        return last, False
    first = simple_list
    if not first.next:
        return first
    last, end = pop(simple_list.next)
    middle = simple_list.next
    first.next = last
    if not end:
        last.next = repack_recursive(middle)
    return first

def repack_from_list(simple_list):
    normal_list = simple_to_list(simple_list)
    keys = list(range(len(normal_list)))
    shuffled_keys = zip(keys[:len(keys)/2], keys[len(keys):len(keys)/2:-1])
    shuffled_keys = sum(shuffled_keys, ())
    if len(keys)%2:
        shuffled_keys += (len(keys)/2,)
    shuffled_list = [normal_list[k] for k in shuffled_keys]
    return list_to_simple(shuffled_list)

def test(simple_list, repack):
    print(simple_to_list(simple_list))
    print(simple_to_list(repack(simple_list)))
    print('')

if __name__ == "__main__":
    test(simple_range(1, 9), repack_recursive)
    test(simple_range(9), repack_recursive)
    test(simple_range(9), repack_from_list)