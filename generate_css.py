
tbls = [[
  ["pazer", "lgarmeh", "kadma-vazla", "kadma-vazla", "kadma-vazla", "kadma-vazla", "kadma-vazla"],
  [None,    "rvia",    "rvia",        "zarka",       "pashta",      "tvir",        "tvir"       ],
  [None,    None,      None,          "segol",       "zakef",       "tipcha",      "tipcha"     ],
  [None,    None,      None,          None,          None,          "etnachta",    "sof-pasuk"  ],
], [
  ["pazer-3", "mahpach-lgarmeh-3", "azla-lgarmeh-3", "azla-lgarmeh-3", "azla-lgarmeh-3", "azla-lgarmeh-3"],
  [None,      "rvia-3",            "rvia-3",         "tzinor-3",       "dechi-3",        "dechi-3"       ],
  [None,      None,                None,             "ole-vyored-3",   "etnachta-3",     "rvia-mugrash-3"],
  [None,      None,                None,             None,             None,             "sof-pasuk-3"   ],
]]
extra_jumps = \
  [ ["kadma-vazla", "lgarmeh"] ] + \
  [ [d, "mahpach-lgarmeh-3"] for col in tbls[1] for d in col if d is not None and d != "mahpach-lgarmeh-3" ]
extra_parents = \
  [ ["mahpach-lgarmeh-3", d] for col in tbls[1] for d in col if d is not None and d != "mahpach-lgarmeh-3" ]

conjs = {
  "pazer":       { "pazer-munach" },
  "lgarmeh":     { "lgarmeh-mercha" },
  "kadma-vazla": { "kadma-vazla-tlisha" },
  "rvia":        { "rvia-munach" },
  "zarka":       { "zarka-munach", "sub-mercha" },
  "pashta":      { "pashta-mahpach", "sub-mercha" },
  "tvir":        { "tvir-darga", "sub-mercha" },
  "segol":       { "segol-munach" },
  "zakef":       { "zakef-munach" },
  "tipcha":      { "tipcha-mercha" },
  "etnachta":    { "etnachta-munach" },
  "sof-pasuk":   { "sof-pasuk-mercha" },
  "pazer-3":        { "pazer-galgal-3" },
  "azla-lgarmeh-3": { "azla-lgarmeh-mahpach-3", "ilui-3", "tzinorit-mahpach-3" },
  "rvia-3":         { "rvia-mahpach-3", "ilui-3", "tzinorit-mahpach-3" },
  "tzinor-3":       { "tzinor-munach-3" },
  "dechi-3":        { "dechi-munach-3" },
  "ole-vyored-3":   { "ole-vyored-etnach-hafuch-3" },
  "etnachta-3":     { "etnachta-munach-3" },
  "rvia-mugrash-3": { "rvia-mugrash-mercha-3", "tarcha-3", "tzinorit-mercha-3" },
  "sof-pasuk-3":    { "sof-pasuk-mercha-3", "tzinorit-mercha-3" },
}

asterisks = [[[2, 3], [3, 5]],
             [[2, 2], [2, 3]]]
def asterisk_applies(ix, col, row, new_row):
  for [ast_col, ast_row] in asterisks[ix]:
    if col >= ast_col and new_row == ast_row and row >= new_row: return True
  return False

subs = {
  "segol":          { "shalshelet":          { "parents": set() } },
  "zakef":          { "zakef-gadol":         { "parents": set() } },
  "pashta":         { "ytiv":                { "parents": set() } },
  "tvir":           { "mercha-kfulah":       { "parents": { "tvir-darga" }, "children": { "tipcha" }, "parents_jumps": set(),
                                               "equated": { "tipcha-mercha" } } },
  "kadma-vazla":    { "kadma":               {},
                      "gershayim":           { "parents": set() },
                      "azla-geresh":         { "parents": set() } },
  "pazer":          { "tlisha-gdolah":       { "children_jumps": { "kadma-vazla" },
                                               "equated": { "kadma-vazla-tlisha" } },
                      "galgal-karne-farah":  {} },
  "rvia-mugrash-3": { "shalshelet-3":        {} },
  "tzinor-3":       { "rvia-katan-3":        { "parents": set() } },
  "azla-lgarmeh-3": { "shalshelet-ktanah-3": {} },
}


colors = [
  "var(--past-accent-color)",
  "var(--future-accent-color)",
  "var(--next-accent-color)",
  [0,2],
  "var(--current-accent-color)",
]


all_accents = { d for ix in range(0, len(tbls)) \
                  for col in range(0, len(tbls[ix])) \
                  for d in tbls[ix][col] if d is not None }
all_accents |= { d for d in conjs }
all_accents |= { c for d in conjs for c in conjs[d] }
all_accents |= { s for d in subs for s in subs[d] }

parents_direct  = { p: set() for p in all_accents }
children_direct = { p: set() for p in all_accents }
parents_jumps   = { p: set() for p in all_accents }

for d in conjs:
  for c in conjs[d]:
    parents_direct[d].add(c)
    children_direct[c] |= { d1 for d1 in conjs if c in conjs[d1] }

for ix in range(0, len(tbls)):
  tbl = tbls[ix]

  for col in range(0, len(tbl)):
    for row in range(0, len(tbl[col])):
      d = tbl[col][row]
      if d is None:
        continue
      if col < len(tbl)-1 and tbl[col+1][row] is not None:
        d1 = tbl[col+1][row]
        parents_direct[d1].add(d)
        for c in conjs.get(d1, set()):
          parents_direct[c].add(d)
        children_direct[d].add(d1)
        for c in conjs.get(d1, set()):
          children_direct[d].add(c)
      else:
        for new_col in range(0, col+1):
          for new_row in range(0, len(tbl[new_col])):
            if row < len(tbl[new_col])-1 and asterisk_applies(ix, col, row, new_row):
              continue;
            if tbl[new_col][new_row] is not None:
              d1 = tbl[new_col][new_row]
              parents_jumps[d1].add(d)
              for c in conjs.get(d1, set()):
                parents_jumps[c].add(d)

  for [d1, d2] in extra_jumps:
    parents_jumps[d2].add(d1)
    for c in conjs.get(d2, set()):
      parents_jumps[c].add(d1)
  for [d1, d2] in extra_parents:
    parents_direct[d2].add(d1)
    for c in conjs.get(d2, set()):
      parents_direct[c].add(d1)
    children_direct[d1].add(d2)
    for c in conjs.get(d2, set()):
      children_direct[d1].add(c)

  for d in subs:
    for s in subs[d]:
      parents_direct[s] = subs[d][s].get("parents", parents_direct[d])
      children_direct[s] = subs[d][s].get("children", children_direct[d])
      parents_jumps[s] = subs[d][s].get("parents_jumps", parents_jumps[d])
  for p in parents_direct:
    parents_direct[p] |= { s for d in subs if d in parents_direct[p] for s in subs[d] if p in subs[d][s].get("children", {p}) }
  for p in children_direct:
    children_direct[p] |= { s for d in subs if d in children_direct[p] for s in subs[d] if p in subs[d][s].get("parents", {p}) }
  for p in parents_jumps:
    parents_jumps[p] |= { s for d in subs if d in parents_jumps[p] for s in subs[d] if p in subs[d][s].get("children_jumps", {p}) }

  future_parents = { p: set(parents_direct[p]) for p in parents_direct }
  for _ in range(0, len(tbl)-1):
    for p in future_parents:
      future_parents[p].update(*(parents_direct[q] for q in future_parents[p]))

  past_children = { p: set(children_direct[p]) for p in children_direct }
  for _ in range(0, len(tbl)-1):
    for p in past_children:
      past_children[p].update(*(children_direct[q] for q in past_children[p]))

strictly_future_parents = { p: future_parents[p] - parents_direct[p] for p in future_parents }
parents = { p: parents_direct[p] | parents_jumps[p] for p in parents_direct }
parents_which_are_also_past_children = { p: parents_jumps[p] & past_children[p] for p in parents_direct if p in past_children }

equated = { p: { p } for p in parents_direct }
for d in conjs:
  for c in conjs[d]:
    equated[c] |= conjs[d]
for d in subs:
  for s in subs[d]:
    equated[d] |= { s }
    equated[s] |= { d }
    for q in subs[d][s].get("equated", set()):
      equated[q] |= { s }
      equated[s] |= { q }


# The example - unrelated to cantillation
num_words = [[2, 3, 1, 2, 3, 3, 2], # [4, 2, 3, 2, 4, 3],
             [3, 2, 2, 3, 7, 3, 2],
             [2, 1, 3, 2, 2],
             [1, 5, 4, 4],
             [9], [7], [4, 2, 1], [4, 2, 1]]
for i in range(0, len(num_words)):
  for j in range(0, len(num_words[i])):
    for k in range(0, num_words[i][j]):
      p = f'he{100 * i + 10 * j + k + 1}'
      if len(num_words[i]) > 1:
        past_children[p] = { f'he{100 * i + 10 * j + k1 + 1}' for k1 in range(k, num_words[i][j]) }
        strictly_future_parents[p] = { f'he{100 * i + 10 * j + k1 + 1}' for k1 in range(0, k-1) }
        if k < num_words[i][j]-1:
          parents[f'he{100 * i + 10 * j + k + 2}'] = { p }
        elif j < len(num_words[i])-1:
          parents[f'he{100 * i + 10 * (j + 1) + 1}'] = { p }
      equated[p] = { p }
for x in ['a', 'b']:
  for i in range(0, len(num_words)):
    for j in range(0, len(num_words[i])):
      for k in range(0, num_words[i][j]):
        p, q = f'he{100 * i + 10 * j + k + 1}', f'en{100 * i + 10 * j + k + 1}{x}'
        if len(num_words[i]) > 1:
          past_children[p] |= { s.replace('he', 'en') + x for s in past_children[p] }
          past_children[q] = past_children[p]
          strictly_future_parents[p] |= { s.replace('he', 'en') + x for s in strictly_future_parents[p] }
          strictly_future_parents[q] = strictly_future_parents[p]
          if p in parents:
            parents[p] |= { s.replace('he', 'en') + x for s in parents[p] }
            parents[q] = parents[p]
        equated[p] |= { s.replace('he', 'en') + x for s in equated[p] }
        equated[q] = equated[p]

precedence = [past_children, strictly_future_parents, parents, parents_which_are_also_past_children, equated]

def selector(m, p):
  return f'html:has({", ".join([f'#{c}:hover, #{c}:active' for c in sorted(m[p])])}) #{p}'
def css(m):
  return ", ".join([ selector(m, p) for p in sorted(m) if len(m[p]) > 0 ])

with open('generated.css', 'w') as f:
  for i in range(0, len(precedence)):
    if len(precedence[i]) == 0: continue;
    f.write(css(precedence[i]) + '{\n')
    if isinstance(colors[i], str):
      f.write(f'  background-color: {colors[i]};\n')
    else:
      c1, c2 = colors[colors[i][0]], colors[colors[i][1]]
      # f.write(f'  background: repeating-linear-gradient(45deg, {c1}, {c1} 2px, {c2} 2px, {c2} 21px);\n')
      f.write(f'  background: linear-gradient(-90deg, {c1} 2px, {c2} 12px);\n')
    f.write('}\n')
