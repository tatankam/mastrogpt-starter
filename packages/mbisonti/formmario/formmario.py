import os, requests as req
import vision
import bucket
import base64
import time

USAGE = "Please upload a picture and I will tell you what I see"
FORM = [
  {
    "label": "carica immagine",
    "name": "pic",
    "required": "true",
    "type": "file"
  },
]

def formmario(args):
  res = {}
  out = USAGE
  inp = args.get("input", "")

  if type(inp) is dict and "form" in inp:
    img = inp.get("form", {}).get("pic", "")
    
    # Decode base64 image
    decoded_img = base64.b64decode(img)
    
    # Create a Bucket instance
    bucket_instance = bucket.Bucket(args)
    
    # Generate a unique filename using timestamp
    filename = f"formmarioimage_{int(time.time())}.jpg"
    
    # Save the image to S3
    result = bucket_instance.write(filename, decoded_img)
    
    if result == "OK":
      print(f"Image saved successfully as {filename}")
      
      # Generate a presigned URL for the image
      presigned_url = bucket_instance.exturl(filename, 3600)  # 1 hour expiration
      
      # Process the image using vision module
      vis = vision.Vision(args)
      out = vis.decode(img)
      
      # Update the response with the presigned URL
      res['html'] = f'<img src="{presigned_url}">'
    else:
      print(f"Failed to save image: {result}")
      out = "Failed to save image"
  
  res['form'] = FORM
  res['output'] = out
  return res
