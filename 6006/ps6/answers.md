# Problem Set 6 Answers


## 6-1. I can haz moar frendz

u_0 (u) -> u_1 -> u_2 -> u_k (k)

where k - vagueness
strength - product of ER(u_i-1, u_i)

where ER(u, v) - edge rank based on u interest in v

```text

dfs(g, n, k, p, d, v):
  if n in v:
    return

  v.add(n)

  if n not in d or d[n] < p:
    d[n] = p

  if k > 0:
    for c in g[n]:
      dfs(g, c, k - 1, p * er(n, c), d, v)

  v.remove(n)

strength(g, s, k):
  let d = {}
  let v = {}
  dfs(g, s, k, 1, d, v)
  return d
```

## RenBook competitor

### a installation order

```text
# ls is a dict of ls[l] = [d1, d2, ..., dn]
dfs(ls, l, o, v):
  if l in v:
    return
  for d in ls[l]:
    dfs(ls, d, o, v)
  v.add(l)
  o.push(l)

installation_order(ls):
  o = []
  for k in ls.keys():
    dfs(ls, k, o, {})
  return o
```

### b installation order for non-installed packages

```text
non_installed_package_order(ls):
  return installation_order(filter_non_installed(ls))
```

