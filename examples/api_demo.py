#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

This file is part of **python-openzwave** project http://code.google.com/p/python-openzwave.
    :platform: Unix, Windows, MacOS X
    :sinopsis: openzwave wrapper

.. moduleauthor:: bibi21000 aka Sébastien GALLET <bibi21000@gmail.com>

License : GPL(v3)

**python-openzwave** is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

**python-openzwave** is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with python-openzwave. If not, see http://www.gnu.org/licenses.

"""

import logging
import sys, os

#logging.getLogger('openzwave').addHandler(logging.NullHandler())
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger('openzwave')

#Insert your build directory here (it depends of your python distribution)
#To get one, run the make_doc.sh command
sys.path.insert(0, os.path.abspath('../build/tmp/usr/local/lib/python2.6/dist-packages'))
sys.path.insert(0, os.path.abspath('../build/tmp/usr/local/lib/python2.7/dist-packages'))
sys.path.insert(0, os.path.abspath('build/tmp/usr/local/lib/python2.6/dist-packages'))
sys.path.insert(0, os.path.abspath('build/tmp/usr/local/lib/python2.7/dist-packages'))
import openzwave
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
import time

#Define some manager options
options = ZWaveOption(device="/tmp/zwave", \
  config_path="openzwave/config", \
  user_path=".", cmd_line="")
options.set_log_file("OZW_Log.log")
options.set_append_log_file(False)
options.set_console_output(False)
options.set_save_log_level('Debug')
options.set_logging(True)
options.lock()

#Create a network object
network = ZWaveNetwork(options, log=None)

print "Waiting for driver : "
for i in range(0,20):
    if network.state>=network.STATE_INITIALISED:
        print " done"
        break
    else:
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(1.0)
if network.state<network.STATE_INITIALISED:
    print "."
    print "Can't initialise driver! Look at the logs in OZW_Log.log"
    quit(1)
print "Use python library : %s" % network.controller.python_library_version
print "Use openzwave library : %s" % network.controller.library_description
print "Network home_id : %s" % network.home_id
print "Controller node_id : %s" % network.controller.node.node_id
print "Waiting for network to come ready : "
for i in range(0,30):
    if network.state>=network.STATE_READY:
        print " done"
        break
    else:
        sys.stdout.write(".")
        sys.stdout.write(network.state)
        sys.stdout.write("(")
        sys.stdout.write(network.nodes_count)
        sys.stdout.write(")")
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(1.0)
if not network.ready:
    print "."
    print "Can't start network! Look at the logs in OZW_Log.log"
    quit(2)
print "Nodes in network : %s" % network.nodes_count
print "Driver statistics : %s" % network.controller.stats

for node in network.nodes:
	print "%s:%s" % (node.node_id,node.name)
