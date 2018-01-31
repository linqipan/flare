#!/usr/bin/python

"""
gen_cgxfbd.py generates fbd file for ccx\n
It pre-processes the inp by cgx\n
INPUT: flare_gmsh.inp
OUTPUT: flare_gmsh.fbd

set up entities

"""


import json
import numpy as np

#========== fbd file =========#

"""
In the 2D geometry, we need to remove the 1D elements
In the 3D geometry, we need to remove the 2D elements

command zap 

"""
with open('flare_json.json','r') as json_file:
    data_store = json.load(json_file)

with open('flare_gmsh.inp','r') as msh_file:
#    header_content = msh_file.readlines()
    msh_content = msh_file.read()
    head = msh_file.readlines()
#    header_content = [d.strip() for d in header_content if d[0] == '*']
    if(data_store['shell_ele'] == 1):
        msh_content = msh_content.replace('CPS3', 'S3')
        with open('flare_gmsh.inp', 'w') as newfile:
            newfile.write(msh_content)

with open("flare_gmsh.fbd",'wb') as fbd_file:
    fbd_file.write('read flare_gmsh.inp\n')
    if('+T3D2' in i for i in msh_content):
        fbd_file.write('zap +T3D2\n')
    
    fbd_file.write('send all abq\n')

    if(data_store['Pressure_load']['Area'] != None):
        fbd_file.write('comp %s do\n' % (data_store['Pressure_load']['Area']))
        fbd_file.write('send %s abq sur\n' %(data_store['Pressure_load']['Area']))
        fbd_file.write('send top abq nam\n')
        fbd_file.write('send bot abq nam\n')

