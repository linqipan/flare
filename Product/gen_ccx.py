#!/usr/bin/python
"""
gen_ccx.py generates the input file for ccx\n

INPUT: all.msh.
OUTPUT: flare_ccx.inp

computation file

"""


import json



#=========== inp file =============##

with open('flare_json.json','r') as json_file:
    data_store = json.load(json_file)

with open('flare_ccx.inp','wb') as inp_file:
    inp_file.write('*INCLUDE, INPUT=all.msh\n')
    inp_file.write('*INCLUDE, INPUT= top.nam\n'+\
                    '*INCLUDE, INPUT= bot.nam\n')
    if(data_store['Pressure_load']['Area'] != None):
        inp_file.write('*INCLUDE, INPUT= %s.sur\n'%(data_store['Pressure_load']['Area']))
    inp_file.write('*BOUNDARY\n'+\
                    'Ntop,1,6,0\n')
    inp_file.write('*MATERIAL, NAME=material_1\n'+\
                    '*Elastic\n'+\
                    '%.3f,%.3f,%.3f\n'%(data_store['inlet_material']['young'],data_store['inlet_material']['nu'],data_store['Temp'])+\
                    '*DENSITY\n'+\
                    '%.3f\n'%(data_store['inlet_material']['density'])+\
                    '*EXPANSION\n'+\
                    '%f\n'%(data_store['inlet_material']['expansion']))

    inp_file.write('*SOLID SECTION,MATERIAL=material_1,ELSET=Eall\n'+\
                    '%f\n'%(data_store['inlet_thick']))
    inp_file.write('*INITIAL CONDITIONS,TYPE=TEMPERATURE\n'+\
                    'Nall, %f\n' %(data_store['Temp']))

    inp_file.write('*STEP\n'+\
                    '*STATIC\n')
    inp_file.write('*DLOAD\n')
    inp_file.write('Eall,GRAV,9.81,0.,0.,-1.\n')
    if(data_store['Pressure_load']['Area'] != None):
        inp_file.write('S%s, %.3f\n'%(data_store['Pressure_load']['Area']),data_store['Pressure_load']['mag'])




    #============== OUTPUT =================####
    inp_file.write('*NODE FILE,OUTPUT=3D\n'+\
                    'RF,U,NT\n'+\
                    '*EL FILE\n'+\
                    'S,E\n'+\
                    '*END STEP')



