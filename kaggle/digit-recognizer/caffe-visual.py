#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

import os
import sys
sys.path.append(os.path.join(os.environ['HOME'], 'repo/caffe/python'))
import caffe

import caffe.draw
from caffe.proto import caffe_pb2
from google.protobuf import text_format

net = caffe_pb2.NetParameter()
text_format.Merge(open('caffe-conf/train.prototxt').read(), net)
caffe.draw.draw_net_to_file(net, 'train.jpg', 'TB')

net = caffe_pb2.NetParameter()
text_format.Merge(open('caffe-conf/test.prototxt').read(), net)
caffe.draw.draw_net_to_file(net, 'test.jpg', 'TB')

caffe.set_mode_cpu()
net = caffe.Net('caffe-conf/test.prototxt',
                'uv_iter_9500.caffemodel',
                caffe.TEST)

from common import *
data = read_test(10)
start_timer()
data = data.reshape((-1, 1, 28, 28))
out = net.forward_all(**{'data': data})
blobs = net._blobs
for name in net._layer_names: print name

import pylab as plt
import matplotlib.cm as cm

def simple_plot(data, r0, c0):
    fig, axs = plt.subplots(r0, c0)
    for r in range(0, r0):
        for c in range(0, c0):
            ax = axs[r][c]
            ax.axes.get_xaxis().set_visible(False)
            ax.axes.get_yaxis().set_visible(False)
            im = data[r * c0 + c]
            ax.imshow(im, cmap = cm.Greys_r)
    plt.show()

nth = 2 # nth instance
print 'conv1...'
data = blobs[1].data[nth] # conv1
simple_plot(data, 4, 8)

print 'pool1...'
data = blobs[2].data[nth] # pool1
simple_plot(data, 4, 8)

print 'conv2...'
data = blobs[3].data[nth] # conv2
simple_plot(data, 8, 8)

print 'pool2...'
data = blobs[4].data[nth] # pool2
simple_plot(data, 8, 8)

