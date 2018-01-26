#!/usr/bin/python
"""
gen_gmsh.py generates files for gmsh\n
INPUT: "flare_json.json"\n
OUTPUT: "Product.geo"\n
Param:\n
top_dia, bottom_dia,height\n
material property\n
point load, pressure load, temperature\n
mesh level, oerder, min_size\n

"""
import json




#============== Reading JSON File ============#

with open('flare_json.json','r') as json_file:
    data_store = json.load(json_file)

top_rad = data_store['top_dia']/2
bottom_rad = data_store['bottom_dia']/2
height = data_store['height']

#============= Writing geo File  ============#

with open('Product.geo','wb') as geo_file:
    geo_file.write('Width =784;\n'+\
    'Height = 682;\n'+\
    'scale = 2*%d/ %d;\n'%(bottom_rad,height) +\
    'General.GraphicsWidth = General.MenuWidth + Width;\n'+\
    'General.GraphicsHeight = Height;\n' +\
    'General.Trackball = 0;\n' +\
    'General.RotationX = 35; General.RotationY = -35; General.RotationZ = 0;\n'+\
    'General.Orthographic = 0;\n'+\
    'General.AxesMikado = 1;\n'+\
    'General.AxesAutoPosition = 1;\n'+\
    'General.Axes = 4; General.SmallAxes = 2;\n'+\
    'General.ScaleX =scale;General.ScaleY =scale;General.ScaleZ =scale;\n'+\
    'View.CenterGlyphs =1;\n')

    geo_file.write("Point(1) = {0,0,0,1};\n")
    geo_file.write("Point(2) = {%d,0,0,1};\n\
Point(3) = {0,%d,0,1};\n\
Point(4) = {-%d,0,0,1};\n\
Point(5) = {0,-%d,0,1};\n"%(bottom_rad,bottom_rad,bottom_rad,bottom_rad))

    geo_file.write("Circle(1) = {2,1,3};\n\
Circle(2) = {3,1,4};\n\
Circle(3) = {4,1,5};\n\
Circle(4) = {5,1,2};\n")

    geo_file.write("Line Loop(5) = {1,2,3,4};\n")

    geo_file.write("// top circle // \n \n")
    geo_file.write("Point(6) = {0,0,%d,1};\n"%(height))
    geo_file.write("Point(7) = {%d,0,%d,1};\n\
Point(8) = {0,%d,%d,1};\n\
Point(9) = {-%d,0,%d,1};\n\
Point(10) = {0,-%d,%d,1};\n"%(bottom_rad,height,bottom_rad,height,bottom_rad,height,bottom_rad,height))


    geo_file.write("Circle(5) = {8, 6, 9};\n\
Circle(6) = {9, 6, 10};\n\
Circle(7) = {10, 6, 7};\n\
Circle(8) = {7, 6, 8};\n")

    geo_file.write("Line(9) = {2, 7};\n\
Line(10) = {3, 8};\n\
Line(11) = {4, 9};\n\
Line(12) = {5, 10};\n")

    geo_file.write("Line Loop(6) = {9, 8, -10, -1};\n\
Surface(1) = {6};\n\
Line Loop(7) = {9, -7, -12, 4};\n\
Surface(2) = {7};\n\
Line Loop(8) = {12, -6, -11, 3};\n\
Surface(3) = {8};\n\
Line Loop(9) = {11, -5, -10, 2};\n\
Surface(4) = {9};\n")

    geo_file.write('Physical Line("top") = {6, 5, 7, 8};\n'+\
    'Physical Line("bot") = {3, 4, 1, 2};\n'+\
    'Physical Surface("press") = {1};\n')
    

    geo_file.write("// Mesh level // \n \n")
    """
    Mesh option:
    1=MeshAdapt, 2=Automatic, 5=Delaunay, 6=Frontal, 7=BAMG, 8=DelQuad

    """
    geo_file.write('Mesh.SurfaceFaces = 1;\n'+\
            'Mesh.VolumeEdges = 0;\n'+\
            'Mesh.ElementOrder = %d;\n'%data_store['second_order'])
            
    if(data_store['refine_level'] == 1):
        geo_file.write('Mesh.OptimizeNetgen = 1;\n'+\
        'Mesh.Algorithm = 2;\n'+\
        'Mesh.Smoothing = 30;\n'+\
        'Mesh.CharacteristicLengthFromCurvature = 0;\n'+\
        'Mesh.CharacteristicLengthFromPoints = 1;\n'+\
        'Mesh.CharacteristicLengthFactor =2;\n'+\
        'Mesh.CharacteristicLengthMax = %.3f;\n'%data_store['min_ele'])
    elif (data_store['refine_level'] ==2):
         geo_file.write('Mesh.OptimizeNetgen = 1;\n'+\
        'Mesh.Algorithm = 2;\n'+\
        'Mesh.Smoothing = 50;\n'+\
        'Mesh.CharacteristicLengthFromCurvature = 0;\n'+\
        'Mesh.CharacteristicLengthFromPoints = 1;\n'+\
        'Mesh.CharacteristicLengthFactor =1;\n'+\
        'Mesh.CharacteristicLengthMax = %.3f;\n'%data_store['min_ele'])
    else:
        assert(data_store['refine_level'] == 0)
        geo_file.write('Mesh.OptimizeNetgen = 1;\n'+\
        'Mesh.Algorithm = 2;\n'+\
        'Mesh.Smoothing = 50;\n'+\
        'Mesh.CharacteristicLengthFromCurvature = 1;\n'+\
        'Mesh.CharacteristicLengthFromPoints = 0;\n'+\
        'Mesh.CharacteristicLengthFactor =2;\n'+\
        'Mesh.CharacteristicLengthMax = %.3f;\n'%data_store['min_ele'])
    
    #========== OUTPUT FILE =============#

    geo_file.write('Mesh 2;\n'+\
    'Print.Background = 1;\n'+\
    'BoundingBox;\n'+\
    'Print "ScreenMesh.png";\n')

    geo_file.write('Mesh.SaveAll = 1;\n'+\
    'Mesh.SaveGroupsOfNodes = 1;\n'+\
    'Save "flare_gmsh.inp";\n'+\
    'Save "flare_gmsh.stl";\n'+\
    'Exit;\n')


