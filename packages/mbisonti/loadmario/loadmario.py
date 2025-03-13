import vdb
import requests
from bs4 import BeautifulSoup
import re

USAGE = f"""Welcome to the Vector DB Loader.
Write text to insert in the DB.
Start with * to do a vector search in the DB.
Start with ! to remove text with a substring.
Start with ^ to drop the collection.
Start with https:// to import content from a webpage.
"""

def loadmario(args):
    collection = args.get("COLLECTION", "default")
    out = f"{USAGE}Current collection is {collection}"
    inp = str(args.get('input', ""))
    db = vdb.VectorDB(args)

    if inp.startswith("*"):
        if len(inp) == 1:
            out = "Please specify a search string"
        else:
            res = db.vector_search(inp[1:])
            if len(res) > 0:
                out = f"Found:\n"
                for i in res:
                    out += f"({i[0]:.2f}) {i[1]}\n"
            else:
                out = "Not found"
    elif inp.startswith("!"):
        count = db.remove_by_substring(inp[1:])
        out = f"Deleted {count} records."
    elif inp.startswith("https://"):
        try:
            response = requests.get(inp)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            sentences = re.split(r'(?<=[.!?])\s*', text)
            sentences = [s.strip() for s in sentences if s.strip() != '']
            for sentence in sentences:
                if len(sentence) <= 1024:
                    res = db.insert(sentence)
                    out += f"Inserted sentence: {sentence}\n"
                else:
                    out += f"Skipped sentence too long: {sentence[:50]}...\n"
        except Exception as e:
            out = f"Failed to import content: {e}"
    
    elif inp.startswith("^"):
        db.setup(drop=True)
        out = "Collection dropped!"
    elif inp != '':
        res = db.insert(inp)
        out = "Inserted "
        out += " ".join([str(x) for x in res.get("ids", [])])


    return {"output": out}

# Note: The tokenize function is not used in this example as we are dealing with sentences.
# However, if you want to tokenize sentences further, you can modify the code to use it.
