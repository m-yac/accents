import json
from pathlib import Path
import re
import requests
from tqdm import tqdm
from urllib.parse import quote

def sefaria(base, **kwargs):
  url = 'https://www.sefaria.org/api/' + quote(base, safe='/')
  if len(kwargs) > 0:
    url += '?' + "&".join(f'{quote(k)}={quote(v)}' for k, v in kwargs.items())
  headers = {"accept": "application/json"}
  return requests.get(url, headers=headers).json()

def process_book(book):
  chs = sefaria(f'v3/texts/{book}', version="hebrew", return_format="text_only")["versions"][0]["text"]
  return [ [ process_verse(v) for v in ch ] for ch in chs ]

def process_verse(v):
  v = re.sub(r'[^\s\u0591-\u05AE\u05BD\u05C0\u05C3]', '', v)
  v = re.sub(r'\s+([\u05C0\u05C3])', r'\1', v)
  return v

tanakh_books = [ bk["title"] for entry in sefaria("index") \
                             for cat in entry["contents"] if "contents" in cat \
                             for bk in cat["contents"] if "corpus" in bk \
                             if bk["corpus"] == "Tanakh" ]

tanakh = { book: process_book(book) for book in tqdm(tanakh_books) }

tanakh_accents = Path(__file__).parent.parent / 'json' / 'tanakh_accents.json'
with tanakh_accents.open('w') as file:
  json.dump(tanakh, file, ensure_ascii=False)
