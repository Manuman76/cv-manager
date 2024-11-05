def get_dict_from_string_array(a: str, type: str) -> list[dict]:
    arr = []
    lst = a.split(', ')
    for b in lst:
        d = {}
        d[type] = b
        arr.append(d)
    return arr
