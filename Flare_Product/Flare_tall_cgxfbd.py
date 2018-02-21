#!/usr/bin/python

import json
import numpy as np

with open('flaregeometry.oofem', 'r') as json_file:
    flare = json.load(json_file)
with open('model.dsgn') as wind_file:
    wind_data = json.load(wind_file)

with open('flare_gmsh_test.inp','r') as msh_file:
    msh_content = msh_file.read()


with open('flare_tall_gmsh.fbd','wb') as fbd_file:
    fbd_file.write('read flare_gmsh_test.inp\n')
    if('+T3D2' in msh_content):
        fbd_file.write('zap +T3D2\n')

    fbd_file.write('send all abq\n')

    for i in range(len(flare['BeamSections'])):
        fbd_file.write('send section%s abq\n'%str(i+1))

    ### default bottom fix #####
    fbd_file.write('send inlet_end_1 abq nam\n')
    ### wind file

    for i in range(1, len(wind_data['elementArray'])+1):
        fbd_file.write('comp windsurf%s do\n' % (str(i)))
        fbd_file.write('send windsurf%s abq sur\n'%(str(i)))


