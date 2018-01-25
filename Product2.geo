SetFactory("OpenCASCADE");
Include "Product2_geo.par";          // parameter input
Width =784;
Height = 682;
r_inlet = inlet_dia/2; r_nozzle = nozzle_dia/2; r_pad = r_nozzle+pad_width; 
l_inlet = inlet_length; l_nozzle = nozzle_length;
n_pad = Ceil(pad_width/el_size)+1;

scale = 3*r_inlet/ l_inlet;
General.GraphicsWidth = General.MenuWidth + Width;  // graphics size
General.GraphicsHeight = Height;                     // graphics size
SetFactory("OpenCASCADE");
Mesh.Algorithm = 2; //1=MeshAdapt, 2=Automatic, 5=Delaunay, 6=Frontal, 7=BAMG, 8=DelQuad
General.Trackball = 0;
General.RotationX = 35; General.RotationY = -35; General.RotationZ = 0;
General.Orthographic = 0;
General.AxesMikado = 1;
General.AxesAutoPosition = 1; //Position the axes automatically   Default value: 1
General.Axes = 4; General.SmallAxes = 2;  //Axes (0=none, 1=simple axes, 2=box, 3=full grid, 4=open grid, 5=ruler)
General.ScaleX =scale;General.ScaleY =scale;General.ScaleZ =scale;


centerp = newp; Point(centerp) = {0, 0, 0};

Circle(1) = {0,centerp,0,r_inlet};

Extrude {0,0,l_inlet} {Line{1};}


// points-3, lines-3, surface-1

Circle(4) = {0,centerp,0,r_pad};
Rotate {{0,1,0}, {0,0,0}, Pi/2} {Line{4};}
Translate {0, 0, l_inlet/2} {Line{4};}
Extrude {2*r_inlet,0,0} {Line{4};}

BooleanDifference{ Surface{1}; Delete; }{ Surface{2}; Delete; }


// points-5, lines-7, surface-3

Circle(8) = {0,centerp,0,r_nozzle};
Rotate {{0,1,0}, {0,0,0}, Pi/2} {Line{8};}
Translate {0, 0, l_inlet/2} {Line{8};}
Extrude {(r_inlet+l_nozzle),0,0} {Line{8};}

BooleanDifference{ Surface{2}; Surface{3}; Delete; }{Surface{4}; Delete; }

// points-7, lines-11, surface-5

Circle(12) = {0,centerp,0,r_nozzle};
Rotate {{0,1,0}, {0,0,0}, Pi/2} {Line{12};}
Translate {0, 0, l_inlet/2} {Line{12};}
Extrude {(r_inlet+l_nozzle),0,0} {Line{12};}
Geometry.AutoCoherence = 1;

BooleanDifference{ Surface{6}; Delete; }{Surface{3}; Surface{5};Delete; }

Recursive Delete {Surface{5};}

//Recombine Surface {1, 2, 4, 6};

Rectangle(7) = {-r_inlet, 0, 0, r_inlet, l_inlet, 0};
Rotate {{1,0,0}, {0,0,0}, Pi/2} {Surface{7};}
BooleanDifference{ Surface{1}; Delete; }{Surface{7}; Delete; }

// points-10, lines-5, surface-8
Rectangle(9) = {-1.1*r_inlet, -1.1*r_inlet, l_inlet/2, 2*1.1*r_inlet+l_nozzle, 2*1.1*r_inlet, 0};
BooleanDifference{ Surface{2,4,6,7,8}; Delete; }{Surface{9}; Delete; }


Physical Surface("inlet") = {8, 9, 10, 11};
Physical Surface("nozzle") = {5, 6, 7};
Physical Surface("pad") = {1, 2, 3, 4};

Physical Line("inlet_end_1") = {22, 26};
Physical Line("inlet_end_2") = {24, 28};
Physical Line("nozzle_end") = {14, 17, 18};


Transfinite Line {2, 4, 6, 9} = n_pad Using Progression 1;  // division number of pad
Mesh.SurfaceFaces = 1;                            // shade mode for surface plotting
Mesh.CharacteristicLengthFromCurvature = 1;
Mesh.CharacteristicLengthFromPoints = 0;
Mesh.CharacteristicLengthFactor = el_size; 
Mesh.CharacteristicLengthExtendFromBoundary = 1;
Mesh.CharacteristicLengthMax = 1e22;
Mesh.FlexibleTransfinite = 1;
Mesh.LightTwoSide = 1;
Mesh.Algorithm = 2; //1=MeshAdapt, 2=Automatic, 5=Delaunay, 6=Frontal, 7=BAMG, 8=DelQuad
Recursive Delete {
  Point{1}; 
}
Mesh 2;
Print.Background = 1;
BoundingBox;
Print "ScreenMesh.png";

Mesh.SaveAll = 1;
Mesh.SaveGroupsOfNodes = 1;

Save "Product2_gmsh.inp";
Save "Product2_gmsh.stl";

Exit;

