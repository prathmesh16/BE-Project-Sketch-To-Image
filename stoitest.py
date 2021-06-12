# [2016-08-05] Modifications for Completion: Brandon Amos (http://bamos.github.io)
#   + License: MIT
# [2017-07] Modifications for sText2Image: Shangzhe Wu
#   + License: MIT

import argparse
import os
#import tensorflow as tf
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
from model2 import GAN


def runModel(args,f):
    parser = argparse.ArgumentParser()
    parser.add_argument('--lr', type=float, default=0.01)
    parser.add_argument('--momentum', type=float, default=0.9)
    parser.add_argument('--nIter', type=int, default=1000)
    parser.add_argument('--imgSize', type=int, default=64)
    parser.add_argument('--batchSize', type=int, default=64)
    parser.add_argument('--text_vector_dim', type=int, default=100)
    parser.add_argument('--lam1', type=float, default=0.1) # Hyperparameter for contextual loss [0.1]
    parser.add_argument('--lam2', type=float, default=0.1) # Hyperparameter for perceptual loss [0.1]
    parser.add_argument('--lam3', type=float, default=0.1) # Hyperparameter for wrong example [0.1]
    parser.add_argument('--checkpointDir', type=str, default='checkpoint')
    parser.add_argument('--outDir', type=str, default='results')
    parser.add_argument('--text_path', type=str, default='text_embeddings.pkl')
    parser.add_argument('--maskType', type=str,
                        choices=['random', 'center', 'left', 'right', 'full'],
                        default='right')
    parser.add_argument('--attributes', nargs='+', type=int, default=[None])
    parser.add_argument('imgs', type=str, nargs='+')

    #args = parser.parse_args()
    # print(args["imgSize"])
    #assert(os.path.exists(args.checkpointDir))

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    with tf.Session(config=config) as sess:
        model = GAN(sess, 
                    image_size=args["imgSize"], 
                    batch_size=args["batchSize"], 
                    text_vector_dim=args["text_vector_dim"],
                    checkpoint_dir=args["checkpointDir"], 
                    lam1=args["lam1"], 
                    lam2=args["lam2"],
                )
        msgs = model.test(args,f)
        for msg in msgs:
          yield msg
