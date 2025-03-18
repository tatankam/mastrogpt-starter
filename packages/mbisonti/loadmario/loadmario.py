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
            out = ""
            response = requests.get(inp)
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract text from all paragraphs
            paragraphs = soup.find_all('p')
            #print(paragraphs)
            for paragraph in paragraphs:
                text = paragraph.get_text()
                sentences = text.split(".")
                for sentence in sentences:
                    sentence = sentence.strip()  # Remove leading/trailing whitespace
                    if sentence:  # Avoid empty sentences
                        res = db.insert(sentence)
                        out += f"Frase Inserita: {sentence} \n"
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


