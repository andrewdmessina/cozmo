# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys
import time
import glob
import os

import numpy as np
import tensorflow as tf
import take_pictures

def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()

  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)

  return graph

def read_tensor_from_image_file(file_name, input_height=240, input_width=320,
				input_mean=0, input_std=255):
  input_name = "file_reader"
  output_name = "normalized"
  file_reader = tf.read_file(file_name, input_name)
  print(file_reader)
  if file_name.endswith(".png"):
    image_reader = tf.image.decode_png(file_reader, channels = 3,
                                       name='png_reader')
  elif file_name.endswith(".gif"):
    image_reader = tf.squeeze(tf.image.decode_gif(file_reader,
                                                  name='gif_reader'))
  elif file_name.endswith(".bmp"):
    image_reader = tf.image.decode_bmp(file_reader, name='bmp_reader')
  else:
    image_reader = tf.image.decode_jpeg(file_reader, channels = 3,
                                        name='jpeg_reader')
  float_caster = tf.cast(image_reader, tf.float32)
  dims_expander = tf.expand_dims(float_caster, 0)
  resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
  normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
  sess = tf.Session()
  result = sess.run(normalized)

  return result

def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label

async def label_cozmo_image(robot):
  rt_value = []
  input_height = 224
  input_width = 224
  input_mean = 128
  input_std = 128
  input_layer = "input"
  output_layer = "final_result"
  model_file = [] #'./tmp/output_graph.pb'
  label_file = [] #'./tmp/output_labels.txt'
  os.chdir('images')
  for f in os.listdir('.'):
    if f != 'junk' and f != 'label':
      model_file.append('images/' + f + '/output_graph.pb')
      label_file.append('images/' + f + '/output_labels.txt')
  while True:
    rt_value = []
    await take_pictures.tf_cozmo_program(robot)
    list_of_files = glob.glob('images/label/*') # * means all if need specific format then *.csv
    print(list_of_files)
    file_name = max(list_of_files, key=os.path.getctime)
    t = read_tensor_from_image_file(file_name,
                                input_height=input_height,
                                input_width=input_width,
                                input_mean=input_mean,
                                input_std=input_std)
    for model, label in zip(model_file, label_file):
      graph = load_graph(model)
      input_name = "import/" + input_layer
      output_name = "import/" + output_layer
      input_operation = graph.get_operation_by_name(input_name)
      output_operation = graph.get_operation_by_name(output_name)

      with tf.Session(graph=graph) as sess:
        results = sess.run(output_operation.outputs[0],
                          {input_operation.outputs[0]: t})
      results = np.squeeze(results)

      top_k = results.argsort()[-5:][::-1]
      labels = load_labels(label)
      rt_value.append([top_k, labels])
    for v in rt_value:
      print(v)


if __name__ == "__main__":
  model_file = []
  label_file = []
  os.chdir('./cozmo_game/images')
  for f in os.listdir('.'):
    if f != 'junk' and f != 'label':
      model_file.append('./cozmo_game/images/' + f + '/output_graph.pb')
      label_file.append('./cozmo_game/images/' + f + '/output_labels.txt')

  for model, label in zip(model_file, label_file):
    print(model, label)
  take_pictures.label_image()
  list_of_files = glob.glob('images/label/*') # * means all if need specific format then *.csv
  file_name = max(list_of_files, key=os.path.getctime)
  input_height = 224
  input_width = 224
  input_mean = 128
  input_std = 128
  input_layer = "input"
  output_layer = "final_result"

  parser = argparse.ArgumentParser()
  parser.add_argument("--image", help="image to be processed")
  parser.add_argument(
    "--graph",
    default='./tmp/output_graph.pb',
    help="graph/model to be executed"
  )
  parser.add_argument(
    "--labels", 
    default='./tmp/output_labels.txt',
    help="name of file containing labels"
  )
  parser.add_argument("--input_height", type=int, help="input height")
  parser.add_argument("--input_width", type=int, help="input width")
  parser.add_argument("--input_mean", type=int, help="input mean")
  parser.add_argument("--input_std", type=int, help="input std")
  parser.add_argument("--input_layer", help="name of input layer")
  parser.add_argument("--output_layer", help="name of output layer")
  args = parser.parse_args()

  if args.graph:
    model_file = args.graph
  if args.image:
    file_name = args.image
  if args.labels:
    label_file = args.labels
  if args.input_height:
    input_height = args.input_height
  if args.input_width:
    input_width = args.input_width
  if args.input_mean:
    input_mean = args.input_mean
  if args.input_std:
    input_std = args.input_std
  if args.input_layer:
    input_layer = args.input_layer
  if args.output_layer:
    output_layer = args.output_layer

  graph = load_graph(model_file)
  t = read_tensor_from_image_file(file_name,
                                  input_height=input_height,
                                  input_width=input_width,
                                  input_mean=input_mean,
                                  input_std=input_std)
  input_name = "import/" + input_layer
  output_name = "import/" + output_layer
  input_operation = graph.get_operation_by_name(input_name)
  output_operation = graph.get_operation_by_name(output_name)

  with tf.Session(graph=graph) as sess:
    start = time.time()
    results = sess.run(output_operation.outputs[0],
                      {input_operation.outputs[0]: t})
    end=time.time()
  results = np.squeeze(results)

  top_k = results.argsort()[-5:][::-1]
  labels = load_labels(label_file)

  print('\nEvaluation time (1-image): {:.3f}s\n'.format(end-start))

  for i in top_k:
    print(labels[i], results[i])
