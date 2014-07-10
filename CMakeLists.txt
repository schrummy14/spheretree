PROJECT (spheretree)

CMAKE_MINIMUM_REQUIRED (VERSION 2.8)

INCLUDE_DIRECTORIES (
  ${CMAKE_CURRENT_SOURCE_DIR}/src
  ${CMAKE_CURRENT_SOURCE_DIR}/src/Geometry/pcube
  )

SET (PROJECT_VERSION 1.0.0)

SET (SPHERETREE_HEADERS
  src/API/DomainSampler.h
  src/API/Hybrid.h
  src/API/MSBase.h
  src/API/MSGrid.h
  src/API/MSRelaxation.h
  src/API/MergeHubbard.h
  src/API/REBase.h
  src/API/REDiscard.h
  src/API/RELargest.h
  src/API/RELargestLM.h
  src/API/REMaxElim.h
  src/API/RESelect.h
  src/API/SEBase.h
  src/API/SEConvex.h
  src/API/SEPoint.h
  src/API/SESphPt.h
  src/API/SFBase.h
  src/API/SFMinErr.h
  src/API/SFRitter.h
  src/API/SFWhite.h
  src/API/SFWhite/ball.h
  src/API/SFWhite/complex.h
  src/API/SFWhite/nrutil.h
  # src/API/SFWhite/origbits/ball.h
  src/API/SFWhite/svd.h
  src/API/SOBalance.h
  src/API/SOBase.h
  src/API/SOPerSphere.h
  src/API/SOSimplex.h
  src/API/SRBase.h
  src/API/SRBurst.h
  src/API/SRComposite.h
  src/API/SRExpand.h
  src/API/SRGrid.h
  src/API/SRMerge.h
  src/API/SRQuickBurst.h
  src/API/SRSpawn.h
  src/API/SRStandOff.h
  src/API/SRVoronoi.h
  src/API/SSBase.h
  src/API/SSIsohedron.h
  src/API/SSRings.h
  src/API/STGBase.h
  src/API/STGGeneric.h
  src/API/STGHubbard.h
  src/API/STGOctree.h
  src/API/SurfaceDiv.h
  src/API/VFAdaptive.h
  src/API/VFBase.h
  src/API/VFGapCross.h
  src/BBox/BBox.h
  src/BBox/MVBB/gdiam.h
  src/BBox/eigen.h
  src/BBox/qHull/geom.h
  src/BBox/qHull/mem.h
  src/BBox/qHull/merge.h
  src/BBox/qHull/poly.h
  src/BBox/qHull/qhull.h
  src/BBox/qHull/qhull_a.h
  src/BBox/qHull/set.h
  src/BBox/qHull/stat.h
  src/BBox/qHull/user.h
  src/Base/Defs.h
  src/Base/ProcMon.h
  src/Base/Types.h
  src/DecodeParam.h
  src/EvalTree.h
  # src/Exceptions/CallStack.h
  src/Exceptions/CheckAlways.h
  src/Exceptions/CheckDebug.h
  src/Exceptions/CheckMemory.h
  src/Exceptions/ErrorLog.h
  src/Exceptions/ErrorsInc.h
  src/Exceptions/Exception.h
  src/Exceptions/MemoryException.h
  src/Exceptions/ValidPointer.h
  src/Export/POV.h
  src/Export/VRML.h
  src/Geometry/Angles.h
  src/Geometry/Circle.h
  src/Geometry/CubeTri.h
  src/Geometry/Geometry.h
  src/Geometry/Line2D.h
  src/Geometry/LineSeg.h
  src/Geometry/Plane.h
  src/Geometry/Point2D.h
  src/Geometry/Point3D.h
  src/Geometry/Ray.h
  src/Geometry/RayBox.h
  src/Geometry/Sphere.h
  src/Geometry/Transform2D.h
  src/Geometry/Transform3D.h
  src/Geometry/TriTri.h
  src/Geometry/Vector2D.h
  src/Geometry/Vector3D.h
  src/Geometry/pcube/pcube.h
  src/Geometry/pcube/vec.h
  src/LinearAlgebra/Matrix.h
  src/MedialAxis/Clusters.h
  src/MedialAxis/MedialTester.h
  src/MedialAxis/Voronoi3D.h
  src/MedialAxis/VoronoiFace.h
  src/MinMax/Simplex.h
  src/SphereTree/SphereTree.h
  src/Storage/Array.h
  src/Storage/Array2D.h
  src/Storage/FreeArray.h
  src/Storage/LinkedList.h
  src/Storage/Queue.h
  src/Storage/Storage.h
  src/Storage/kTree.h
  src/Surface/Internal.h
  src/Surface/InternalGem.h
  src/Surface/OBJLoader.h
  src/Surface/SpacialHash.h
  src/Surface/Surface.h
  src/Surface/SurfaceRep.h
  src/Surface/SurfaceTester.h
  src/Surface/VolInt.h
  src/Surface/Voxel.h
  src/VerifyModel.h
  )

SET (SPHERETREE_SOURCES
  src/API/DomainSampler.cpp
  src/API/Hybrid.cpp
  src/API/MSBase.cpp
  src/API/MSGrid.cpp
  src/API/MSRelaxation.cpp
  src/API/MergeHubbard.cpp
  src/API/REBase.cpp
  src/API/REDiscard.cpp
  src/API/RELargest.cpp
  src/API/RELargestLM.cpp
  src/API/REMaxElim.cpp
  src/API/RESelect.cpp
  src/API/SEConvex.cpp
  src/API/SEPoint.cpp
  src/API/SESphPt.cpp
  src/API/SFBase.cpp
  src/API/SFMinErr.cpp
  src/API/SFRitter.cpp
  src/API/SFWhite.cpp
  src/API/SFWhite/ball.cpp
  src/API/SFWhite/complex.c
  src/API/SFWhite/nrutil.c
  # src/API/SFWhite/origbits/ball.cpp
  # src/API/SFWhite/origbits/tball.cpp
  src/API/SFWhite/svd.cpp
  src/API/SOBalance.cpp
  src/API/SOBase.cpp
  src/API/SOPerSphere.cpp
  src/API/SOSimplex.cpp
  src/API/SRBurst.cpp
  src/API/SRComposite.cpp
  src/API/SRExpand.cpp
  src/API/SRGrid.cpp
  src/API/SRMerge.cpp
  src/API/SRQuickBurst.cpp
  src/API/SRSpawn.cpp
  src/API/SRStandOff.cpp
  src/API/SRVoronoi.cpp
  src/API/SSIsohedron.cpp
  src/API/SSRings.cpp
  src/API/STGGeneric.cpp
  src/API/STGHubbard.cpp
  src/API/STGOctree.cpp
  src/API/SurfaceDiv.cpp
  src/API/VFAdaptive.cpp
  src/API/VFGapCross.cpp
  src/BBox/BBox.cpp
  src/BBox/MVBB/gdiam.cpp
  # src/BBox/MVBB/origbits/examples.cpp
  src/BBox/eigen.cpp
  src/BBox/qHull/geom.cpp
  src/BBox/qHull/geom2.cpp
  src/BBox/qHull/global.cpp
  src/BBox/qHull/mem.cpp
  src/BBox/qHull/merge.cpp
  src/BBox/qHull/poly.cpp
  src/BBox/qHull/poly2.cpp
  src/BBox/qHull/qhull.cpp
  src/BBox/qHull/set.cpp
  src/BBox/qHull/stat.cpp
  src/BBox/qHull/user.cpp
  src/Base/ProcMon.cpp
  src/DecodeParam.cpp
  src/EvalTree.cpp
  # src/Exceptions/CallStack.cpp
  src/Exceptions/ErrorLog.cpp
  src/Exceptions/Exception.cpp
  src/Exceptions/MemoryException.cpp
  src/Export/POV.cpp
  src/Export/VRML.cpp
  src/Geometry/Circle.cpp
  src/Geometry/CubeTri.cpp
  src/Geometry/Line2D.cpp
  src/Geometry/LineSeg.cpp
  src/Geometry/Plane.cpp
  src/Geometry/Point2D.cpp
  src/Geometry/Point3D.cpp
  src/Geometry/Ray.cpp
  src/Geometry/RayBox.c
  src/Geometry/Sphere.cpp
  src/Geometry/Transform2D.cpp
  src/Geometry/Transform3D.cpp
  src/Geometry/TriTri.cpp
  src/Geometry/Vector2D.cpp
  src/Geometry/Vector3D.cpp
  src/Geometry/pcube/fpcube.cpp
  # src/Geometry/pcube/origbits/test.c
  src/Geometry/pcube/pcube.cpp
  src/LinearAlgebra/Matrix.cpp
  src/MedialAxis/Clusters.cpp
  src/MedialAxis/MedialTester.cpp
  src/MedialAxis/Voronoi3D.cpp
  src/MedialAxis/VoronoiFace.cpp
  src/MinMax/Simplex.cpp
  src/SphereTree/SphereTree.cpp
  src/Surface/Internal.cpp
  src/Surface/InternalGem.cpp
  src/Surface/OBJLoader.cpp
  src/Surface/SpacialHash.cpp
  src/Surface/Surface.cpp
  src/Surface/SurfaceRep.cpp
  src/Surface/SurfaceTester.cpp
  src/Surface/VolInt.cpp
  src/Surface/Voxel.cpp
  src/VerifyModel.cpp
  src/null.c
)

ADD_LIBRARY (spheretree SHARED ${SPHERETREE_SOURCES} ${SPHERETREE_HEADERS})
SET_TARGET_PROPERTIES (spheretree PROPERTIES
  VERSION ${PROJECT_VERSION}
  SOVERSION 1.0
)

MACRO (BUILD_PROGRAM FILENAME)
  ADD_EXECUTABLE (${FILENAME} src/${FILENAME}.cpp ${SPHERETREE_HEADERS})
  TARGET_LINK_LIBRARIES (${FILENAME} spheretree)
ENDMACRO ()

BUILD_PROGRAM (makeTreeGrid)
BUILD_PROGRAM (makeTreeHubbard)
BUILD_PROGRAM (makeTreeMedial)
BUILD_PROGRAM (makeTreeOctree)
BUILD_PROGRAM (makeTreeSpawn)
