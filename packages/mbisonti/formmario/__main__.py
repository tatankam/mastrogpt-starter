#--kind python:default
#--web true
#--param OLLAMA_HOST $OLLAMA_HOST
#--param AUTH $AUTH

import formmario
def main(args):
  return { "body": formmario.formmario(args) }
