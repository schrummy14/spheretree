/*************************************************************************\

                             C O P Y R I G H T

  Copyright 2003 Image Synthesis Group, Trinity College Dublin, Ireland.
                        All Rights Reserved.

  Permission to use, copy, modify and distribute this software and its
  documentation for educational, research and non-profit purposes, without
  fee, and without a written agreement is hereby granted, provided that the
  above copyright notice and the following paragraphs appear in all copies.


                             D I S C L A I M E R

  IN NO EVENT SHALL TRININTY COLLEGE DUBLIN BE LIABLE TO ANY PARTY FOR
  DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING,
  BUT NOT LIMITED TO, LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE
  AND ITS DOCUMENTATION, EVEN IF TRINITY COLLEGE DUBLIN HAS BEEN ADVISED OF
  THE POSSIBILITY OF SUCH DAMAGES.

  TRINITY COLLEGE DUBLIN DISCLAIM ANY WARRANTIES, INCLUDING, BUT NOT LIMITED
  TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
  PURPOSE.  THE SOFTWARE PROVIDED HEREIN IS ON AN "AS IS" BASIS, AND TRINITY
  COLLEGE DUBLIN HAS NO OBLIGATIONS TO PROVIDE MAINTENANCE, SUPPORT, UPDATES,
  ENHANCEMENTS, OR MODIFICATIONS.

  The authors may be contacted at the following e-mail addresses:

          Gareth_Bradshaw@yahoo.co.uk    isg@cs.tcd.ie

  Further information about the ISG and it's project can be found at the ISG
  web site :

          isg.cs.tcd.ie

\**************************************************************************/

/*
    tests sphere trees generated with various methods
*/
#include <stdio.h>
#include <string.h>

#include <string>

#include <boost/filesystem.hpp>
#include <boost/algorithm/string.hpp>

#include "Surface/Surface.h"
#include "Surface/OBJLoader.h"
#include "API/MSGrid.h"
#include "API/SEConvex.h"
#include "API/SESphPt.h"
#include "API/SSIsohedron.h"
#include "API/SRGrid.h"
#include "API/STGGeneric.h"
#include "EvalTree.h"
#include "VerifyModel.h"
#include "DecodeParam.h"

/*
    options and their default values
*/
int testerLevels = -1;      //  number of levels for NON-CONVEX, -1 uses CONVEX tester
int branch = 8;             //  branching factor of the sphere-tree
int depth = 3;              //  depth of the sphere-tree
int numCoverPts = 5000;     //  number of test points to put on surface for coverage
int minCoverPts = 5;        //  minimum number of points per triangle for coverage
bool verify = false;        //  verify model before construction
bool nopause = false;       //  will we pause before starting
bool eval = false;          //  do we evaluate the sphere-tree after construction
bool yaml = false;          //  do we export to YAML

/*
    info for decoding parameters
*/
const IntParam intParams[] = {{"testerLevels", &testerLevels},
                              {"branch", &branch},
                              {"depth", &depth},
                              {"numCover", &numCoverPts},
                              {"minCover", &minCoverPts},
                              {NULL, NULL}};

const BoolParam boolParams[] = {{"verify", &verify, TRUE},
                                {"nopause", &nopause, TRUE},
                                {"eval", &eval, TRUE},
                                {"yaml", &yaml, TRUE},
                                {NULL, NULL}};

/*
    forward declarations
*/
void waitForKey();
int error(const char *errorMsg, const char *errorMsg1 = NULL);
bool constructTree(const boost::filesystem::path& input_file,
                   bool toYAML = false);

/*
    MAINLINE
*/
int main(int argc, const char *argv[]){
  printf("MakeTreeGrid - Gareth Bradshaw Feb 2003\n");

  /*
     parse command line
  */
  decodeIntParam(argc, argv, intParams);
  decodeBoolParam(argc, argv, boolParams);
  printf("Options : \n");
  writeParam(stdout, intParams);
  writeParam(stdout, boolParams);

  /*
     look for filenames and construct trees
  */
  int numFiles = 0;
  for (int i = 1; i < argc; i++){
    if (argv[i] != NULL){
      constructTree(argv[i], yaml);
      numFiles++;
      }
    }

  /*
     check we had a file name
  */
  if (numFiles == 0)
    error("no files given :(");

  waitForKey();
}

/*
    construct sphere-tree for the model
*/
bool constructTree(const boost::filesystem::path& input_file,
                   bool toYAML)
{
  boost::filesystem::path output_file
    = input_file.parent_path () / boost::filesystem::basename (input_file);

  if (toYAML)
    output_file += "-grid.yml";
  else
    output_file += "-grid.sph";

  printf("Input file: %s\n", input_file.c_str ());
  printf("Output file: %s\n\n", output_file.c_str ());

  /*
      load the surface model
  */
  Surface sur;

  bool loaded = false;
  std::string extension = boost::algorithm::to_lower_copy (input_file.extension ().string ());
  if (extension == ".obj")
    loaded = loadOBJ(&sur, input_file.c_str ());
  else
    loaded = sur.loadSurface(input_file.c_str ());

  if (!loaded){
    printf("ERROR : Unable to load input file (%s)\n\n", input_file.c_str ());
    return false;
    }

  /*
      scale box
  */
  // FIXME: Disable scaling for now (wrong result if a transformation is applied after)
  //float boxScale = sur.fitIntoBox(1000);
  float boxScale = 1.;

  /*
      make medial tester
  */
  MedialTester mt;
  mt.setSurface(sur);
  mt.useLargeCover = true;

  /*
      setup evaluator
  */
  SEConvex convEval;
  convEval.setTester(mt);
  SEBase *eval = &convEval;

  Array<Point3D> sphPts;
  SESphPt sphEval;
  if (testerLevels > 0){   //  <= 0 will use convex tester
    SSIsohedron::generateSamples(&sphPts, testerLevels-1);
    sphEval.setup(mt, sphPts);
    eval = &sphEval;
    printf("Using concave tester (%d)\n\n", sphPts.getSize());
    }

  /*
      verify model
  */
  if (verify){
    bool ok = verifyModel(sur);
    if (!ok){
      printf("ERROR : model is not usable\n\n");
      return false;
      }
    }

  /*
      setup for the set of cover points
  */
  Array<Surface::Point> coverPts;
  MSGrid::generateSamples(&coverPts, numCoverPts, sur, TRUE, minCoverPts);
  printf("%d cover points\n", coverPts.getSize());

  /*
      setup GRID algorithm
  */
  SRGrid grid;
  grid.optimise = FALSE;
  grid.sphereEval = eval;
  grid.useQuickTest = true;

  /*
      setup SphereTree constructor - using dynamic construction
  */
  STGGeneric treegen;
  treegen.eval = eval;
  treegen.useRefit = true;
  treegen.setSamples(coverPts);
  treegen.reducer = &grid;

  /*
      make sphere-tree
  */
  SphereTree tree;
  tree.setupTree(branch, depth+1);

  waitForKey();
  treegen.constructTree(&tree);

  /*
     save sphere-tree
  */
  if (tree.saveSphereTree(output_file, 1.0f/boxScale)){
    Array<LevelEval> evals;
    if (eval){
      evaluateTree(&evals, tree, eval);
      writeEvaluation(stdout, evals);
      }

    if (!yaml)
    {
      FILE *f = fopen(output_file.c_str (), "a");
      if (f){
        fprintf(f, "\n\n");
        fprintf(f, "Options : \n");
        writeParam(stdout, intParams);
        writeParam(stdout, boolParams);
        fprintf(f, "\n\n");
        writeEvaluation(f, evals);
        fclose(f);
      }
    }

    return true;
    }
  else{
    return false;
    }
}

/*
    error handler
*/
int error(const char *errorMsg, const char *errorMsg1){
  if (errorMsg1)
    printf("ERROR : %s (%s)\n", errorMsg, errorMsg1);
  else
    printf("ERROR : %s\n", errorMsg);

  waitForKey();
  exit(-1);
}

void waitForKey(){
  if (!nopause){
    printf("Press ENTER to continue....\n");
    char buffer[2];
    fread(buffer, 1, 1, stdin);
    }
}
