
COLS, ROWS, tbl, conjs = 4, 7, [
  ["pazer", "lgarmeh", "kadma-vazla", "kadma-vazla", "kadma-vazla", "kadma-vazla", "kadma-vazla"],
  [None,    "rvia",    "rvia",        "zarka",       "pashta",      "tvir",        "tvir"       ],
  [None,    None,      None,          "segol",       "zakef",       "tipcha",      "tipcha"     ],
  [None,    None,      None,          None,          None,          "etnachta",    "sof-pasuk"  ],
], {
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
  "sof-pasuk":   "sof-pasuk-mercha"
}

asterisks = [[2, 3], [3, 5]]

alone_subs = {
  "segol":       { "shalshalet" },
  "zakef":       { "zakef-gadol" },
  "pashta":      { "ytiv" },
  "tvir":        { "mercha-kfulah" },
  "pazer":       { "tlisha-gdolah", "galgal-karne-farah" },
  "kadma-vazla": { "gershayim", "azla-geresh", "kadma" }
}
special_alone_subs = {
  "pazer": { "alone": "tlisha-gdolah", "parents": ["kadma-vazla"], "children": ["pazer-munach"] }
}

colors = [
  "var(--past-accent-color)",
  "var(--future-accent-color)",
  "var(--next-accent-color)",
  [0,2],
  "var(--current-accent-color)",
]



parents_direct  = { d: { conjs[d] } for d in conjs } | { conjs[d]: set() for d in conjs } | { q: set() for d in alone_subs for q in alone_subs[d] }
children_direct = { d: set()        for d in conjs } | { conjs[d]: set() for d in conjs } | { q: set() for d in alone_subs for q in alone_subs[d] }
parents_jumps   = { d: set()        for d in conjs } | { conjs[d]: set() for d in conjs } | { q: set() for d in alone_subs for q in alone_subs[d] }

for d in conjs:
  children_direct[conjs[d]] |= { q for q in conjs if conjs[q] == conjs[d] }

for col in range(0, COLS):
  for row in range(0, ROWS):
    if tbl[col][row] is not None:
      if col < COLS-1 and tbl[col+1][row] is not None:
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
          for new_row in range(0, ROWS):
            if row < ROWS-1 and any(col >= ast_col and new_row == ast_row for [ast_col, ast_row] in asterisks):
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
for _ in range(0, COLS-1):
  for p in future_parents:
    future_parents[p].update(*(parents_direct[q] for q in future_parents[p]))

past_children = { p: set(children_direct[p]) for p in children_direct }
for _ in range(0, COLS-1):
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
