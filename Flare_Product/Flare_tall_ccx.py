#!/usr/bin/python

import json
import numpy as np

with open('flaregeometry.oofem', 'r') as json_file:
    flare = json.load(json_file)
with open('model.dsgn') as wind_file:
    wind_data = json.load(wind_file)

section_num = {}
for i in flare['BeamElements']:
    if i['Section'] not in section_num:
        section_num[i['Section']] = [i['Label']]
    else:
        section_num[i['Section']].append(i['Label'])

thick_list = []
for i in flare['BeamSections']:
    thick = i['Area']/3.14/wind_data['elementArray'][section_num[i['Label']][0]]['Af']
    thick_list.append(thick)

with open('flare_tall_ccx.inp','wb') as inp_file:
    inp_file.write('*INCLUDE, INPUT=all.msh\n')
    inp_file.write('*INCLUDE, INPUT= inlet_end_1.nam\n')

    for i in range(len(flare['BeamSections'])):
        inp_file.write('*INCLUDE,INPUT= section%s.nam\n' % str(i+1))

    for i in range(1, len(wind_data['elementArray'])+1):
        inp_file.write('*INCLUDE, INPUT= windsurf%s.sur\n' % str(i))
    
    inp_file.write('*BOUNDARY\n' +
                   'Ninlet_end_1,1,6,0\n')
    
    for i in flare['BeamSections']:
        inp_file.write('*MATERIAL, NAME=material_%s\n'%str(i['Label']) +\
                       '*Elastic\n' +\
                       '%.3f,%.3f\n' % (i['YoungModulus'], i['PoissonRatio']) +\
                       '*DENSITY\n' +\
                       '%.3f\n' % (i['Density']) +\
                       '*EXPANSION\n' +\
                       '%.3f\n' % (i['ThermalExpansionCoeff']))
    ### solid section ####

    for i in flare['BeamSections']:
        inp_file.write('*SHELL SECTION,MATERIAL=material_%s,ELSET=Esection%s\n' % (str(i['Label']), str(i['Label'])) +\
                       '%d\n' %thick_list[int(i['Label']-1)])

    inp_file.write('*INITIAL CONDITIONS,TYPE=TEMPERATURE\n' +\
                   'Nall, %d\n' % (flare['StructuralTemperatureLoad'][0]['Components'][0]))

    inp_file.write('*STEP\n' +\
                   '*STATIC\n')
    inp_file.write('*DLOAD\n')
    inp_file.write('Eall,GRAV,9.81,0.,0.,-1.\n')

    #### pressure ######
    j =1
    inp_file.write('*DSLOAD\n')
    for i in wind_data['elementArray']:
        inp_file.write('Swindsurf%s, P, %.2f\n'%(str(j),i['F']))
        j +=1 

        #============== OUTPUT =================####
    inp_file.write('*NODE FILE,OUTPUT=3D\n'+\
                    'RF,U,NT\n'+\
                    '*EL FILE\n'+\
                    'S,E\n'+\
                    '*END STEP')

