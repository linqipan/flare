Width =784;
Height = 682;
scale = 2*10/ 60;
General.GraphicsWidth = General.MenuWidth + Width;
General.GraphicsHeight = Height;
General.Trackball = 0;
General.RotationX = 35; General.RotationY = -35; General.RotationZ = 0;
General.Orthographic = 0;
General.AxesMikado = 1;
General.AxesAutoPosition = 1;
General.Axes = 4; General.SmallAxes = 2;
General.ScaleX =scale;General.ScaleY =scale;General.ScaleZ =scale;
View.CenterGlyphs =1;
Point(1) = {0,0,0,1};
Point(2) = {10,0,0,1};
Point(3) = {0,10,0,1};
Point(4) = {-10,0,0,1};
Point(5) = {0,-10,0,1};
Circle(1) = {2,1,3};
Circle(2) = {3,1,4};
Circle(3) = {4,1,5};
Circle(4) = {5,1,2};
Line Loop(5) = {1,2,3,4};
// top circle // 
 
Point(6) = {0,0,60,1};
Point(7) = {10,0,60,1};
Point(8) = {0,10,60,1};
Point(9) = {-10,0,60,1};
Point(10) = {0,-10,60,1};
Circle(5) = {8, 6, 9};
Circle(6) = {9, 6, 10};
Circle(7) = {10, 6, 7};
Circle(8) = {7, 6, 8};
Line(9) = {2, 7};
Line(10) = {3, 8};
Line(11) = {4, 9};
Line(12) = {5, 10};
Line Loop(6) = {9, 8, -10, -1};
Surface(1) = {6};
Line Loop(7) = {9, -7, -12, 4};
Surface(2) = {7};
Line Loop(8) = {12, -6, -11, 3};
Surface(3) = {8};
Line Loop(9) = {11, -5, -10, 2};
Surface(4) = {9};
Physical Line("top") = {6, 5, 7, 8};
Physical Line("bot") = {3, 4, 1, 2};
Physical Surface("press") = {1};
// Mesh level // 
 
Mesh.SurfaceFaces = 1;
Mesh.VolumeEdges = 0;
Mesh.ElementOrder = 1;
Mesh.OptimizeNetgen = 1;
Mesh.Algorithm = 2;
Mesh.Smoothing = 50;
Mesh.CharacteristicLengthFromCurvature = 1;
Mesh.CharacteristicLengthFromPoints = 0;
Mesh.CharacteristicLengthFactor =2;
Mesh.CharacteristicLengthMax = 2.000;
Mesh 2;
Print.Background = 1;
BoundingBox;
Print "ScreenMesh.png";
Mesh.SaveAll = 1;
Mesh.SaveGroupsOfNodes = 1;
Save "flare_gmsh.inp";
Save "flare_gmsh.stl";
Exit;