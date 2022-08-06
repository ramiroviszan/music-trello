

def insert_sorted(collection:list, element) -> list:
    i = 0
    while i < len(collection):
        if element < collection[i]:
            return collection[:i] + [element] + collection[i:]
        i += 1
    return collection + [element]