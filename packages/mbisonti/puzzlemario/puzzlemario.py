import re, os, requests as req
#MODEL = "llama3.1:8b"
MODEL = "phi4:14b"

USAGE = """I will generate a chessboard with the pieces you choose!"""

FORM = [
  {
    "name": "queen",
    "label": "With a queen",
    "required": "optional",
    "type": "checkbox",
  },
    {
    "name": "rook",
    "label": "With a rook",
    "required": "optional",
    "type": "checkbox",
  },
    {
    "name": "knight",
    "label": "With a knight",
    "required": "optional",
    "type": "checkbox",
  },
    {
    "name": "bishop",
    "label": "With a bishop",
    "required": "optional",
    "type": "checkbox",
  }
]

def chat(args, inp):
  host = args.get("OLLAMA_HOST", os.getenv("OLLAMA_HOST"))
  auth = args.get("AUTH", os.getenv("AUTH"))
  url = f"https://{auth}@{host}/api/generate"
  msg = { "model": MODEL, "prompt": inp, "stream": False}
  res = req.post(url, json=msg).json()
  out = res.get("response", "error")
  return  out
 
def extract_fen(out):
  pattern = r"([rnbqkpRNBQKP1-8]+\/){7}[rnbqkpRNBQKP1-8]+"
  fen = None
  m = re.search(pattern, out, re.MULTILINE)
  if m:
    fen = m.group(0)
  return fen

def puz(args):
  out = "If you want to see a chess puzzle, type 'puz'. To display a fen position, type 'fen <fen string>'."
  inp = args.get("input", "")
  res = {}
  if inp == "puz":
    out = USAGE
    res['form'] = FORM
  
  elif type(inp) is dict and "form" in inp:
    data = inp["form"]
    for field in data.keys():
      print(field,data[field])
    inp = f"""generate a chess puzzle in FEN format.Use ONLY pieces if the value of the piece is true:ONE queen={data['queen']}, ONE rook={data['rook']}, ONE knight={data['knight']},ONE bishop={data['bishop']}.
    """
    print(f"questo è l'inp:{inp}")
    #inp = f"""generate a chess puzzle in FEN format with ONLY this pieces:queen rook.
    #"""
    # inp = "generate a chess puzzle in FEN format"
    out = chat(args, inp)
    fen = extract_fen(out)
    if fen:
       print(fen)
       res['chess'] = fen
    else:
      out = "Bad FEN position."
  elif inp.startswith("fen"):
    fen = extract_fen(inp)
    if fen:
       out = "Here you go."
       res['chess'] = fen
  elif inp != "":
    out = chat(args, inp)
    fen = extract_fen(out)
    print(out, fen)
    if fen:
      res['chess'] = fen

  res["output"] = out
  return res
