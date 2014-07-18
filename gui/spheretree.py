#!/usr/bin/env python

from optparse import OptionParser
from subprocess import Popen, PIPE
import os, sys

import numpy as np

from mayavi import mlab


class TreeData():
    def __init__(self, filename):
        # spheres[tree level] = list of spheres for that level
        self.spheres = list()
        # Number of levels in the sphere-tree including root node
        self.n_levels = 0
        # Branching factor of the sphere-tree
        self.branching_factor = 0

        print ("Loading %s" % filename)
        inputfile = open(filename)

        # Load sizes
        lines = inputfile.readlines()
        sizes = lines[0].split()
        self.n_levels = int(sizes[0])
        self.branching_factor = int(sizes[1])

        # Load spheres
        level = 0
        counter = 0
        self.spheres.append(list())
        for line in lines[1:]:
            # Load 4 first elements (x, y, z, radius)
            data = line.split()
            if (len(data) != 5):
                break
            x = float(data[0])
            y = float(data[1])
            z = float(data[2])
            r = float(data[3])
            # Yes that happens...
            if r < 0:
                r = 0
            self.spheres[level].append(np.array([x, y, z, r]))
            counter += 1
            if counter == self.branching_factor ** level:
                if level == self.n_levels:
                    break
                level += 1
                counter = 0
                self.spheres.append(list())

    def xyzr(self, level):
      if level >= self.n_levels:
          level = self.n_levels-1
      n_spheres = self.branching_factor ** level
      xyzr = np.zeros((n_spheres,4))
      print ("Displaying %i spheres" % n_spheres)
      for i, sphere in enumerate(self.spheres[level]):
          xyzr[i,:] = sphere

      return xyzr[:,0], xyzr[:,1], xyzr[:,2], xyzr[:,3]

def algo_list():
    """
    Return the list of supported algorithms.
    """
    return {"spawn", "grid"}

def create_sch(dae_file, algo):
    assert (algo in algo_list)

    # First: convert DAE to OBJ
    # FIXME: change name for multithreading
    name = os.path.splitext(os.path.basename(dae_file))[0]
    tmp_file = "/tmp/" + name + ".obj"
    if not os.path.exists(tmp_file):
        command = "meshlabserver -i " + dae_file + " -o " + tmp_file
        p = Popen(command, shell = True, stdin = sys.stdin, stdout = PIPE, stderr = PIPE, bufsize = 1)

        while p.poll() is None:
            out = p.stdout.read(1)
            sys.stdout.write(out)
            sys.stdout.flush()

    # Second: process OBJ with spheretree
    result_file = "/tmp/%s-%s.sph" % (name, algo)
    exec_name = "makeTree%s" % algo.capitalize()
    if not os.path.exists(result_file):
        command = exec_name + " -nopause " + tmp_file
        p = Popen(command, shell = True, stdin = sys.stdin, stdout = PIPE, stderr = PIPE, bufsize = 1)

        while p.poll() is None:
            out = p.stdout.read(1)
            sys.stdout.write(out)
            sys.stdout.flush()

    # Return resulting SCH file
    return result_file

################################################################################

# Default parameters
default_algo = "spawn"
algo_list = algo_list()

parser = OptionParser(description='Load and process a SPH file')
parser.add_option('-l', '--level', default=0, type=int, metavar='level',
                  help='Tree level')
parser.add_option('--from-dae', metavar='from_dae',
                  action='store_true', default=False,
                  help='Compute sphere-tree from DAE file')
parser.add_option('-a', '--algo', default=default_algo, type=str,
                  metavar='algo', help='Construction algorithm')

options, args = parser.parse_args()
input_file = args[0]
sph_level = options.level
algo = options.algo

if not algo in algo_list:
    print("WARNING: %s is not a valid algorithm. Using %s instead."
          % (algo, default_algo))
    algo = default_algo

if options.from_dae:
    # Compute SCH result from DAE file
    sph_file = create_sch(dae_file=input_file, algo=algo)
else:
    sph_file = input_file

# Disable the rendering, to get bring up the figure quicker:
figure = mlab.gcf()
mlab.clf()
figure.scene.disable_render = True

data = TreeData(filename=sph_file)

# Creates a set of points using mlab.points3d
x, y, z, r = data.xyzr(sph_level)
display_spheres = mlab.points3d(x, y, z, 2*r, scale_factor=1,
                                resolution=20)

# Every object has been created, we can reenable the rendering.
figure.scene.disable_render = False

mlab.title('Sphere-Tree Viewer')

mlab.show()
