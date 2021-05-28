import compas_energyplus
import subprocess
import os

for i in range(50): print('')


data = compas_energyplus.DATA

idf = os.path.join(data, 'tomas.idf')
wea = os.path.join(data, 'USA_WA_Seattle-Tacoma.Intl.AP.727930_TMY3.epw')
eplus = 'energyplus'
out = os.path.join(compas_energyplus.TEMP, 'eplus_output')

subprocess.call([eplus, '-w', wea,'--output-directory', out, idf])
# subprocess.call([eplus, '-w', wea, idf])




