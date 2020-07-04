from rubik import perm_apply, quarter_twists, perm_inverse


def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves.

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """
    if start == end:
        return []

    fs = {start: []}
    bs = {end: []}

    fseen = set([start])
    bseen = set([end])

    def next_perms(d, ds):
        res = {}
        for t in quarter_twists:
            for k in d.keys():
                nk = perm_apply(t, k)
                if nk not in ds:
                    res[nk] = d[k] + [t]
                    ds.add(nk)
        return res

    def find_match(fs, bs):
        for k in fs.keys():
            if k in bs:
                return fs[k] + list(map(lambda x: perm_inverse(x), reversed(bs[k])))

    for i in range(7):
        fs = next_perms(fs, fseen)
        m = find_match(fs, bs)
        if m:
            return m
        bs = next_perms(bs, bseen)
        m = find_match(fs, bs)
        if m:
            return m
