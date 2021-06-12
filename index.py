from flask_ngrok import run_with_ngrok
import numpy as np
import time
from flask import Flask, request,send_file, stream_with_context, jsonify, render_template, Response
import pickle
import stoitest
import threading 
from PIL import Image
import io
import base64
from utils import *
import cv2
import imageio

app = Flask(__name__)
run_with_ngrok(app)   

def stream_template(template_name, **context):
  # http://flask.pocoo.org/docs/patterns/streaming/#streaming-from-templates
  app.update_template_context(context)
  t = app.jinja_env.get_template(template_name)
  rv = t.stream(context)
  # uncomment if you don't need immediate reaction
  ##rv.enable_buffering(5)
  return rv
def serve_pil_image(pil_img):
  img_io = BytesIO()
  pil_img.save(img_io, 'PNG', quality=70)
  img_io.seek(0)
  return send_file(img_io, mimetype='image/png')

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/runModel',methods=['POST'])
def home():
    f = request.files['image'] ## byte file
    f = imageio.imread(f,format='.png').astype(np.float)
    attr = request.form.get('attributes', [])
    attr = attr.split(',')
    map_object = map(float, attr)

    attr = list(map_object)
    print()
    args = {
        "imgSize":64,
        "checkpointDir":"drive/MyDrive/beproject/checkpoints_face_pretrained",
        "maskType":"right",
        "text_vector_dim":18,
        "batchSize":64,
        "lam1":100,
        "lam2":1,
        "lr":0.001,
        "nIter":1000,
        "outDir":"results_face_now5",
        "text_path":"drive/MyDrive/beproject/imAttrs.pkl",
        "momentum":0.9,
        "attributes": attr,
    }
    def sendres():
      msgs = stoitest.runModel(args,f)
      for msg in msgs:
        arr = np.array(msg)
        img = Image.fromarray((arr*255).astype('uint8'))
        file_object = io.BytesIO()
        img.save(file_object, 'PNG')
        file_object.seek(0)
        img_base64 = base64.b64encode(file_object.getvalue()).decode('ascii')
        mime = "image/png"
        uri = "data:%s;base64,%s"%(mime, img_base64)
        yield uri
        # yield serve_pil_image(Image.fromarray(np.uint8(msg)))
    return Response(stream_with_context(sendres()))
    #return Response(stream_template('result.html',data=sendres()))

app.run()