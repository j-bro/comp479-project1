

def merge_lists(lists):
    """
    Merge the specified lists (OR of a set).
    :param lists: the lists to be merged.
    :return: a list that is the result of merging the specified lists.
    """
    if lists:
        return sorted(set.union(*[set(l) for l in lists]))
        # TODO order by number of matching terms
    else:
        return list()


def intersect_lists(lists):
    """
    Intersect the specified lists (AND of a set).
    :param lists: the lists to be intersected.
    :return: a list that is the result of intersecting the specified lists.
    """
    if lists:
        return sorted(set.intersection(*[set(l) for l in lists]))
    else:
        return list()
