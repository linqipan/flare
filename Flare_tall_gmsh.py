#!/usr/bin/python

import json
import numpy as np
import math

with open('flaregeometry.oofem','r') as json_file:
    flare = json.load(json_file)
with open('model.dsgn') as wind_file:
    wind_data = json.load(wind_file)
    
mesh_level = {'refine_level':0,'second_order':2, 'min_ele': 5}

class flaregeo(object):
    
    
    def __init__(self):
        self.section_num = {}
        for i in flare['BeamElements']:
            if i['Section'] not in self.section_num:
                self.section_num[i['Section']] = [i['Label']]
            else:
                self.section_num[i['Section']].append(i['Label'])
        self.radius = [wind_data['elementArray'][0]['Af']/2]
        for i in wind_data['elementArray']:
            self.radius.append(i['Af']/2)
        self.thicktype = {}
        for i in flare['BeamSections']:
            if i['Label'] not in self.thicktype:
                self.thicktype[i['Label']] = i['Area']/3.14
        
        self.section_coord = []
        for i in flare['Nodes']:
            self.section_coord.append(i['Coords'][2])
            
### flare geometry ##        
    def flare_geo(self):
        gmshfile = open('flare.geo','w')
        circlenum=1
        for i in range(1,len(self.section_coord)+1):
            
            gmshfile.write('Point(%d) = {0,0,%d,1};\n'%(5*i-4,self.section_coord[i-1])+\
                          'Point(%d) = {%d,0,%d,1};\n'%(5*i-3,self.radius[i-1],self.section_coord[i-1])+\
                          'Point(%d) = {0,%d,%d,1};\n'%(5*i-2,self.radius[i-1],self.section_coord[i-1])+\
                          'Point(%d) = {-%d,0,%d,1};\n'%(5*i-1,self.radius[i-1],self.section_coord[i-1])+\
                          'Point(%d) = {0,-%d,%d,1};\n'%(5*i,self.radius[i-1],self.section_coord[i-1]))
            gmshfile.write('Circle(%d) = {%d, %d, %d};\n'%(circlenum,5*i-3,5*i-4,5*i-2)+\
                          'Circle(%d) = {%d, %d, %d};\n'%(circlenum+1,5*i-2,5*i-4,5*i-1)+\
                          'Circle(%d) = {%d, %d, %d};\n'%(circlenum+2,5*i-1,5*i-4,5*i)+\
                          'Circle(%d) = {%d, %d, %d};\n'%(circlenum+3,5*i,5*i-4,5*i-3))
            circlenum +=4
        for i in range(1,len(self.section_coord)):
            linenum = 4*len(self.section_coord)
            gmshfile.write('Line(%d) = {%d, %d};\n'%(linenum+4*i-3,5*i-3,5*i+2)+\
                          'Line(%d) = {%d, %d};\n'%(linenum+4*i-2,5*i-2,5*i+3)+\
                          'Line(%d) = {%d, %d};\n'%(linenum+4*i-1,5*i-1,5*i+4)+\
                          'Line(%d) = {%d, %d};\n'%(linenum+4*i,5*i,5*i+5))
            
        for i in range(1,len(self.section_coord)):
            linenum = 4*len(self.section_coord)
            gmshfile.write('Line Loop(%d) = {%d, %d, %d, %d};\n'%(4*i-3,4*i-3,linenum+4*i-2,-(4*i+1),-(linenum+4*i-3))+\
                           'Surface(%d) = {%d};\n'%(4*i-3,4*i-3)+\
                           'Line Loop(%d) = {%d, %d, %d, %d};\n'%(4*i-2,4*i-2,linenum+4*i-1,-(4*i+2),-(linenum+4*i-2))+\
                           'Surface(%d) = {%d};\n'%(4*i-2,4*i-2)+\
                           'Line Loop(%d) = {%d, %d, %d, %d};\n'%(4*i-1,4*i-1,linenum+4*i,-(4*i+3),-(linenum+4*i-1))+\
                           'Surface(%d) = {%d};\n'%(4*i-1,4*i-1)+\
                           'Line Loop(%d) = {%d, %d, %d, %d};\n'%(4*i,4*i,linenum+4*i-3,-(4*i+4),-(linenum+4*i))+\
                           'Surface(%d) = {%d};\n'%(4*i,4*i))
            
        ### Physical groups ####    
        for i in self.section_num:
            surface_num =[]
            for j in self.section_num[i]:
                surface_num.extend((4*j-3,4*j-2,4*j-1,4*j))
            surface_str = ", ".join(map(str,surface_num))
            gmshfile.write('Physical Surface("section%s") = {%s};\n'%(str(i),surface_str))
        gmshfile.write('Physical Line("inlet_end_1") = {1, 2, 3, 4};\n')
            
        ### wind surface ###
        
        for i in range(1,len(flare['BeamElements'])+1):
            gmshfile.write('Physical Surface("windsurf%s") = {%s};\n'%(str(i),str(i)))
        gmshfile.close()
        return 0
    def mesh_refine(self):
        gmshfile = open('flare.geo','a')
        """
        Mesh option:
        1=MeshAdapt, 2=Automatic, 5=Delaunay, 6=Frontal, 7=BAMG, 8=DelQuad

        """
        gmshfile.write('Mesh.SurfaceFaces = 1;\n'+\
                'Mesh.VolumeEdges = 0;\n'+\
                'Mesh.ElementOrder = %d;\n'%mesh_level['second_order'])
            
        if(mesh_level['refine_level'] == 1):
            gmshfile.write('Mesh.OptimizeNetgen = 1;\n'+\
            'Mesh.Algorithm = 2;\n'+\
            'Mesh.Smoothing = 30;\n'+\
            'Mesh.CharacteristicLengthFromCurvature = 0;\n'+\
            'Mesh.CharacteristicLengthFromPoints = 1;\n'+\
            'Mesh.CharacteristicLengthFactor =2;\n'+\
            'Mesh.CharacteristicLengthMax = %.3f;\n'%mesh_level['min_ele'])
        elif (mesh_level['refine_level'] ==2):
             gmshfile.write('Mesh.OptimizeNetgen = 1;\n'+\
            'Mesh.Algorithm = 2;\n'+\
            'Mesh.Smoothing = 50;\n'+\
            'Mesh.CharacteristicLengthFromCurvature = 0;\n'+\
            'Mesh.CharacteristicLengthFromPoints = 1;\n'+\
            'Mesh.CharacteristicLengthFactor =1;\n'+\
            'Mesh.CharacteristicLengthMax = %.3f;\n'%mesh_level['min_ele'])
        else:
            assert(mesh_level['refine_level'] == 0)
            gmshfile.write('Mesh.OptimizeNetgen = 1;\n'+\
            'Mesh.Algorithm = 2;\n'+\
            'Mesh.Smoothing = 50;\n'+\
            'Mesh.CharacteristicLengthFromCurvature = 1;\n'+\
            'Mesh.CharacteristicLengthFromPoints = 0;\n'+\
            'Mesh.CharacteristicLengthFactor =2;\n'+\
            'Mesh.CharacteristicLengthMax = %.3f;\n'%mesh_level['min_ele'])
        gmshfile.write('Mesh 2;\n'+\
                       'Print.Background = 1;\n'+\
                       'BoundingBox;\n'+\
                       'Print "ScreenMesh.png";\n')
        gmshfile.write('Mesh.SaveAll = 1;\n'+\
                       'Mesh.SaveGroupsOfNodes = 1;\n'+\
                       'Save "flare_gmsh_test.inp";\n'+\
                       'Save "flare_gmsh_test.stl";\n'+\
                       'Exit;\n')
        gmshfile.close()
        return

if __name__ == '__main__':
    flare_gmsh = flaregeo()
    flare_gmsh.flare_geo()
    flare_gmsh.mesh_refine()
    