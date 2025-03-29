import os, json, requests as req


MODEL = "llama3.2-vision:11b"

def collect(lines):
  out = ""
  for line in lines:
    #line = next(lines)
    chunk = json.loads(line.decode("UTF-8"))
    out +=  chunk.get("message", {}).get("content", "")
  return out

class Vision:
  def __init__(self, args):
    host = args.get("OLLAMA_HOST", os.getenv("OLLAMA_HOST"))
    auth = args.get("AUTH", os.getenv("AUTH"))
    self.url = f"https://{auth}@{host}/api/chat"

  def decode(self, img):
    msg = {
      "model": MODEL,
      "messages": [ {
        "role": "user",
        "content": "Is there a perfect circle in this image? Answer ONLY 'There is a circle' if yes, 'No circle' if not.",
        #"Please analyze the image and describe its content in both English and Italian. Ensure that each description is complete and includes all relevant details. Format the descriptions as a bullet list with the exact prefixes 'EN:' for the English description and 'IT:' for the Italian description. Make sure each description is fully contained within its respective bullet point. Conclude your description with the text: 'My description is suuuupercomplete' and add two emoticons.",
        #"content": "Please describe shortly, both in english than italian language, what is in this image, and conclude your description with the following text: 'My description is suuuupercomplete' and add two emoticons.",
        "images": [img]
      }]
    }
    lines = req.post(self.url, json=msg, stream=True).iter_lines()
    return collect(lines)
