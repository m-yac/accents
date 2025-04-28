
tbls = [[
  ["pazer", "lgarmeh", "kadma-vazla", "kadma-vazla", "kadma-vazla", "kadma-vazla", "kadma-vazla"],
  [None,    "rvia",    "rvia",        "zarka",       "pashta",      "tvir",        "tvir"       ],
  [None,    None,      None,          "segol",       "zakef",       "tipcha",      "tipcha"     ],
  [None,    None,      None,          None,          None,          "etnachta",    "sof-pasuk"  ],
], [
  ["pazer-3", "lgarmeh-3",    "lgarmeh-3",    "lgarmeh-3",  "lgarmeh-3"     ],
  [None,      "rvia-gadol-3", "tzinor-3",     "dechi-3",    "dechi-3"       ],
  [None,      None,           "ole-vyored-3", "etnachta-3", "rvia-mugrash-3"],
  [None,      None,           None,           None,         "sof-pasuk-3"   ],
]]

conjs = {
  "pazer":       "pazer-munach",       "galgal-karne-farah": "pazer-munach",
  "lgarmeh":     "lgarmeh-mercha",
  "kadma-vazla": "kadma-vazla-tlisha", "kadma": "kadma-vazla-tlisha",
  "rvia":        "rvia-munach",
  "zarka":       "zarka-munach",
  "pashta":      "pashta-mapach",
  "tvir":        "tvir-darga",         "mercha-kfulah": "tvir-darga",
  "segol":       "segol-munach",
  "zakef":       "zakef-munach",
  "tipcha":      "tipcha-mercha",
  "etnachta":    "etnachta-munach",
  "sof-pasuk":   "sof-pasuk-mercha",
  "pazer-3":        "pazer-galgal-3",
  "rvia-gadol-3":   "rvia-gadol-ilui-3",
  "tzinor-3":       "tzinor-munach-3",
  "dechi-3":        "dechi-munach-3",
  "ole-vyored-3":   "ole-vyored-etnach-hafuch-3",
  "etnachta-3":     "etnachta-munach-3",
  "rvia-mugrash-3": "rvia-mugrash-mercha-3", "shalshalet-gadol-3": "rvia-mugrash-mercha-3",
}

asterisks = [[[2, 3], [3, 5]],
             [[2, 2], [2, 3]]]
def asterisk_applies(ix, col, row, new_row):
  for [ast_col, ast_row] in asterisks[ix]:
    if col >= ast_col and new_row == ast_row and row >= new_row: return True
  return False

alone_subs = {
  "segol":       { "shalshalet" },
  "zakef":       { "zakef-gadol" },
  "pashta":      { "ytiv" },
  "tvir":        { "mercha-kfulah" },
  "pazer":       { "tlisha-gdolah", "galgal-karne-farah" },
  "kadma-vazla": { "gershayim", "azla-geresh", "kadma" },
  "rvia-mugrash-3": { "shalshalet-gadol-3" },
  "tzinor-3":       { "rvia-3" },
}
special_alone_subs = {
  "pazer": { "alone": "tlisha-gdolah", "parents": ["kadma-vazla"], "children": ["pazer-munach"] },
}

colors = [
  "var(--past-accent-color)",
  "var(--future-accent-color)",
  "var(--next-accent-color)",
  [0,2],
  "var(--current-accent-color)",
]


all_disj = { d for ix in range(0, len(tbls)) \
               for col in range(0, len(tbls[ix])) \
               for d in tbls[ix][col] if d is not None }

parents_direct  = { d: set() for d in all_disj } | { d: { conjs[d] } for d in conjs } | { conjs[d]: set() for d in conjs } | { q: set() for d in alone_subs for q in alone_subs[d] }
children_direct = { d: set() for d in all_disj } | { d: set()        for d in conjs } | { conjs[d]: set() for d in conjs } | { q: set() for d in alone_subs for q in alone_subs[d] }
parents_jumps   = { d: set() for d in all_disj } | { d: set()        for d in conjs } | { conjs[d]: set() for d in conjs } | { q: set() for d in alone_subs for q in alone_subs[d] }

for d in conjs:
  children_direct[conjs[d]] |= { q for q in conjs if conjs[q] == conjs[d] }

for ix in range(0, len(tbls)):
  tbl = tbls[ix]

  for col in range(0, len(tbl)):
    for row in range(0, len(tbl[col])):
      if tbl[col][row] is not None:
        if col < len(tbl)-1 and tbl[col+1][row] is not None:
          d = tbl[col+1][row]
          parents_direct[d].add(tbl[col][row])
          if d in conjs: parents_direct[conjs[d]].add(tbl[col][row])
          if tbl[col][row] in alone_subs:
            parents_direct[d] |= alone_subs[tbl[col][row]]
            if d in conjs: parents_direct[conjs[d]] |= alone_subs[tbl[col][row]]
          children_direct[tbl[col][row]].add(d)
          if d in conjs: children_direct[tbl[col][row]].add(conjs[d])
        else:
          for new_col in range(0, col+1):
            for new_row in range(0, len(tbl[new_col])):
              if row < len(tbl[new_col])-1 and asterisk_applies(ix, col, row, new_row):
                continue;
              if tbl[new_col][new_row] is not None:
                d = tbl[new_col][new_row]
                parents_jumps[d].add(tbl[col][row])
                if d in conjs: parents_jumps[conjs[d]].add(tbl[col][row])
                if d in alone_subs:
                  for q in alone_subs[d]:
                    parents_jumps[q].add(tbl[col][row])
                if tbl[col][row] in alone_subs and tbl[col][row] not in special_alone_subs:
                  parents_jumps[d] |= alone_subs[tbl[col][row]]
                  if d in conjs: parents_jumps[conjs[d]] |= alone_subs[tbl[col][row]]

  future_parents = { p: set(parents_direct[p]) for p in parents_direct }
  for _ in range(0, len(tbl)-1):
    for p in future_parents:
      future_parents[p].update(*(parents_direct[q] for q in future_parents[p]))

  past_children = { p: set(children_direct[p]) for p in children_direct }
  for _ in range(0, len(tbl)-1):
    for p in past_children:
      past_children[p].update(*(children_direct[q] for q in past_children[p]))

for p in special_alone_subs:
  for q in special_alone_subs[p]["parents"]:
    parents_jumps[q].add(special_alone_subs[p]["alone"])
  for q in special_alone_subs[p]["children"]:
    past_children[q].add(special_alone_subs[p]["alone"])

strictly_future_parents = { p: future_parents[p] - parents_direct[p] for p in future_parents }
parents = { p: parents_direct[p] | parents_jumps[p] for p in parents_direct }
parents_which_are_also_past_children = { p: parents_jumps[p] & past_children[p] for p in parents_direct if p in past_children }

equated = { p: { p } for p in parents_direct }
for p in alone_subs:
  equated[p] |= alone_subs[p]
  for q in alone_subs[p]:
    equated[q] = { p, q }

# The example - unrelated to cantillation
num_words = [[4, 2, 3, 2, 4, 3],
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
  return f'html:has({", ".join([f'#{c}:hover, #{c}:active' for c in m[p]])}) #{p}'
def css(m):
  return ", ".join([ selector(m, p) for p in m if len(m[p]) > 0 ])

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
