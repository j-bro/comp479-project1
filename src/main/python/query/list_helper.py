

def merge_lists(lists):
    if lists:
        return sorted(set.union(*[set(l) for l in lists]))
    else:
        return list()


def intersect_lists(lists):
    if lists:
        return sorted(set.intersection(*[set(l) for l in lists]))
    else:
        return list()
