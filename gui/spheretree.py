#!/usr/bin/env python2

from optparse import OptionParser
from subprocess import Popen, PIPE
import os, sys, shutil

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
    return {"grid", "hubbard", "medial", "octree", "spawn"}

def create_sch(dae_file=None, obj_file=None, algo="grid", depth=3, branch=8):
    """
    Create a SCH file from a DAE (Collada) or OBJ (Wavefront) file.
    Requires meshlab for DAE to OBJ conversion.
    """
    assert (algo in algo_list)
    assert (dae_file or obj_file)

    tmp_file = ""
    name = ""

    if dae_file and os.path.isfile(dae_file):
        # First: convert DAE to OBJ
        # FIXME: change name for multithreading
        name = os.path.splitext(os.path.basename(dae_file))[0]
        tmp_file = "/tmp/" + name + ".obj"
        if not os.path.exists(tmp_file):
            command = "meshlabserver -i " + dae_file + " -o " + tmp_file
            p = Popen(command, shell = True, stdin = sys.stdin, stdout = PIPE,
                      stderr = PIPE, bufsize = 1)

            while p.poll() is None:
                out = p.stdout.read(1)
                sys.stdout.write(out)
                sys.stdout.flush()

    elif obj_file and os.path.isfile(obj_file):
        name = os.path.splitext(os.path.basename(obj_file))[0]
        tmp_file = "/tmp/" + name + ".obj"
        if not os.path.exists(tmp_file):
            shutil.copy(obj_file, tmp_file)

    else:
        print("Error: no valid DAE/OBJ file given.")
        sys.exit(2)

    # Second: process OBJ with spheretree
    result_file = "/tmp/%s-%s.sph" % (name, algo)
    exec_name = "makeTree%s" % algo.capitalize()
    if not os.path.exists(result_file):
        command = "%s -nopause -branch %i -depth %i %s" \
                  % (exec_name, branch, depth, tmp_file)
        p = Popen(command, shell = True, stdin = sys.stdin, stdout = PIPE, stderr = PIPE, bufsize = 1)

        while p.poll() is None:
            out = p.stdout.read(1)
            sys.stdout.write(out)
            sys.stdout.flush()

    # Return resulting SCH file
    return result_file


def display_collada(dae_file):
    """
    Display the DAE mesh. Requires pycollada.
    """
    print("Displaying %s" % dae_file)

    from collada import Collada, DaeUnsupportedError, DaeBrokenRefError
    mesh = Collada(dae_file, ignore=[DaeUnsupportedError, DaeBrokenRefError])

    for node in mesh.scene.nodes:
        print(node.transforms)

    for geometry in mesh.scene.objects('geometry'):
        for prim in geometry.primitives():
            # use primitive-specific ways to get triangles
            prim_type = type(prim).__name__
            if prim_type == 'BoundTriangleSet':
                triangles = prim
            elif prim_type == 'BoundPolylist':
                triangles = prim.triangleset()
            else:
                print ("Unsupported mesh type used: %s" % prim_type)
                triangles = None

            if triangles is not None:
                x = triangles.vertex[:,0]
                y = triangles.vertex[:,1]
                z = triangles.vertex[:,2]

                mlab.triangular_mesh(x, y, z, triangles.vertex_index,
                                     color=(0, 0, 1))

def display_obj(obj_file):
    """
    Display the OBJ mesh. Code adapted from: http://www.nandnor.net/?p=86
    """
    print("Displaying %s" % obj_file)
    verts = np.array([]).reshape(0,3)
    indices = []
    for line in open(obj_file, "r"):
        vals = line.split()
        if len(vals) > 0:
            if vals[0] == "v":
                verts = np.vstack([verts, map(float, vals[1:4])])
            if vals[0] == "f":
                face_indices = []
                for f in vals[1:]:
                    w = f.split("/")
                    if len(w) > 0:
                        a = int(w[0])
                    else:
                        a = int(f)
                    # OBJ Files are 1-indexed so we must subtract 1 below
                    face_indices.append(a-1)
                indices.append(face_indices)
    x = verts[:,0]
    y = verts[:,1]
    z = verts[:,2]
    return mlab.triangular_mesh(x, y, z, indices, color=(0, 0, 1))

################################################################################

# Default parameters
default_algo = "spawn"
algo_list = algo_list()

parser = OptionParser(description='Load and process a SPH file')
parser.add_option('-l', '--level', default=0, type=int, metavar='level',
                  help='Tree level that will be displayed.')
parser.add_option('-d', '--depth', default=3, type=int, metavar='depth',
                  help='Depth of the sphere-tree.')
parser.add_option('-b', '--branch', default=8, type=int, metavar='branch',
                  help='Branching factor of the sphere-tree.')
parser.add_option('-a', '--algo', default=default_algo, type=str,
                  metavar='algo', help='Construction algorithm.')

options, args = parser.parse_args()
input_file = args[0]
sph_depth = options.depth
sph_branch = options.branch
sph_level = min(options.level, sph_depth)
algo = options.algo

if not algo in algo_list:
    print("WARNING: %s is not a valid algorithm. Using %s instead."
          % (algo, default_algo))
    algo = default_algo

from_dae = False
from_obj = False
if input_file.lower().endswith(".dae"):
    from_dae = True
elif input_file.lower().endswith(".obj"):
    from_obj = True

# Default sphere opacity
sphere_opacity = 0.5

if from_dae:
    # Compute SCH result from DAE file
    sph_file = create_sch(dae_file=input_file, algo=algo,
                          depth=sph_depth, branch=sph_branch)
elif from_obj:
    # Compute SCH result from OBJ file
    sph_file = create_sch(obj_file=input_file, algo=algo,
                          depth=sph_depth, branch=sph_branch)
else:
    sph_file = input_file
    sphere_opacity = 1.0

data = TreeData(filename=sph_file)

# Disable the rendering, to get bring up the figure quicker:
figure = mlab.gcf()
mlab.clf()
figure.scene.disable_render = True

if from_dae:
    # Display initial mesh
    display_collada(input_file)

if from_obj:
    # Display initial mesh
    display_obj(input_file)

# Creates a set of points using mlab.points3d
x, y, z, r = data.xyzr(sph_level)
display_spheres = mlab.points3d(x, y, z, 2*r, scale_factor=1,
                                resolution=20, opacity=sphere_opacity,
                                color=(1, 0, 0))

# Every object has been created, we can reenable the rendering.
figure.scene.disable_render = False

mlab.title('Sphere-Tree Viewer', height=0.05, size=0.5)

mlab.show()
