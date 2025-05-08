import json
from pathlib import Path

accent_names = {
                           '\u05A0': "T'lisha-g'dolah", '\u05C0': "Paseq",
  '\u0591': "Etnachta",    '\u05A1': "Pazer",
  '\u0592': "Segol",       '\u05A2': "Atnach-hafuk",
  '\u0593': "Shalshelet",  '\u05A3': "Munach",          '\u05C3': "Sof-pasuk",
  '\u0594': "Zaqef",       '\u05A4': "Mahpach",
  '\u0595': "Zaqef-gadol", '\u05A5': "Mercha",
  '\u0596': "Tipcha",      '\u05A6': "Mercha-k'fulah",
  '\u0597': "R'via",       '\u05A7': "Darga",
  '\u0598': "Tzinorit",    '\u05A8': "Kadma",
  '\u0599': "Pashta",      '\u05A9': "T'lisha",
  '\u059A': "T'tiv",       '\u05AA': "Galgal",
  '\u059B': "T'vir",       '\u05AB': "Ole",
  '\u059C': "Azla",        '\u05AC': "Illui",
  '\u059D': "Mukdam",      '\u05AD': "Dehi",            '\u05BD': "Meteg",
  '\u059E': "Gershayim",   '\u05AE': "Zarka",
  '\u059F': "Karne-farah",
}

def fmt_verse(v):
  for c, s in accent_names.items():
    v = v.replace(c, s)
  return v

tanakh_accents = Path(__file__).parent.parent / 'json' / 'tanakh_accents.json'
with tanakh_accents.open() as file:
  tanakh = json.load(file)

print(fmt_verse(tanakh["Numbers"][35-1][5-1]))
