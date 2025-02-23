#--kind python:default
#--web true
#--param OLLAMA_HOST $OLLAMA_HOST
#--param AUTH $AUTH
import puzzlemario
def main(args):
  return { "body": puzzlemario.puz(args) }
