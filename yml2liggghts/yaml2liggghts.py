import glob
import yaml
import numpy as np

def find(cur_str,ch):
    return [k for k, ids in enumerate(cur_str) if ids == ch]

class TreeData():
    def __init__(self, filename):
        # spheres[tree level] = list of spheres for that level
        self.spheres = list()
        # Number of levels in the sphere-tree including root node
        self.n_levels = 0
        # Branching factor of the sphere-tree
        self.branching_factor = 0

        print ("Loading %s" % filename)
        self.load_yaml(filename)

    def load_yaml(self, filename):
        with open(filename, 'r') as f:
            doc = yaml.load(f,Loader=yaml.SafeLoader)
            self.n_levels = doc["levels"]
            self.branching_factor = doc["degree"]
            self.spheres = dict()

            for data in doc["data"]:
                level = data["level"]
                self.spheres[level] = list()
                for sphere in data["spheres"]:
                    if sphere["radius"] > 0:
                        self.spheres[level].append \
                            (np.array([sphere["center"][0],
                                       sphere["center"][1],
                                       sphere["center"][2],
                                       sphere["radius"]]))

def convert2liggghts(fname):
    td = TreeData(fname)
    ids = find(fname,'.')
    for lev in range(td.n_levels):
        newFile = fname[:ids[-1]]+'-level-%i.liggghts'%(lev)
        makeLIGGGHTS(newFile, td.spheres[lev])

def makeLIGGGHTS(newFile, spheres):

    with open(newFile,'w') as fOut:
        fOut.write("ITEM: TIMESTEP\n10000\n")
        fOut.write("ITEM: NUMBER OF ATOMS\n%i\n"%(len(spheres)))
        fOut.write("ITEM: BOX BOUNDS ff ff ff\n")
        fOut.write("%e %e\n" % (-1, 1))
        fOut.write("%e %e\n" % (-1, 1))
        fOut.write("%e %e\n" % (-1, 1))
        fOut.write("ITEM: ATOMS id x y z radius \n")
        for curId, s in enumerate(spheres):
            fOut.write("%i %f %f %f %f \n" % (curId+1,s[0],s[1],s[2],s[3]))

    return

if __name__ == "__main__":
    fileNames = glob.glob('*.yml')
    for f in fileNames:
        convert2liggghts(f)
