import os
from os.path import expanduser, basename
import subprocess
import numpy as np
import sys
import pandas as pd
import random


if len(sys.argv)!=2:
 print("Usage:\ anapy simulateNF_lshr.py paramFN")
paramFN=sys.argv[1]
paramContents = open(paramFN, 'r').readlines()
for line in paramContents:
    if line.startswith('SeedFile'):
        SeedFile = line.split()[1]
    if line.startswith('percent'):
        percent = float(line.split()[1])
    if line.startswith('SeedFolder'):
        AnalyStem = line.split()[1]
    if line.startswith('Iteration'):
        Iteration = int(line.split()[1])
    if line.startswith('a '):
        a = float(line.split()[1])
    if line.startswith('b '):
        b = float(line.split()[1])
    if line.startswith('c '):
        c = float(line.split()[1])
    if line.startswith('alpha'):
        alpha = float(line.split()[1])
    if line.startswith('beta'):
        beta = float(line.split()[1])
    if line.startswith('gamma'):
        gamma = float(line.split()[1])
    if line.startswith('radius'):
        radius = float(line.split()[1])
    if line.startswith('height'):
        height = float(line.split()[1])
    if line.startswith('SeedParam'):
        SeedParam = (line.split()[1])
    
            
df=pd.read_csv(SeedFile)
print(df.shape[0])
TotalNOrientation=df.shape[0]

'''
df.columns=['O11','O12','O13','O21','O22','O23','O31','O32','O33']
df['a']=a
df['b']=b
df['c']=c
df['alpha']=alpha
df['beta']=beta
df['gamma']=gamma

stilldo=TotalNOrientation
Orientation=0
while stilldo>0:
 #for Orientation in range(0,TotalNOrientation):
  
  test_Z=random.uniform(-0.5*height,0.5*height)
  test_X=random.uniform(-radius,radius)
  test_Y=random.uniform(-radius,radius)
  if (test_Y*test_Y+test_X*test_X)>(radius*radius):
    continue
  else:
   stilldo=stilldo-1
   
  df.loc[Orientation,'Z']=test_Z
  df.loc[Orientation,'Y']=test_Y
  df.loc[Orientation,'X']=test_X
  Orientation=Orientation+1
  #print(Orientation)
#baseFN = basename(SeedFile)
OutFile = f'{OutFolder}/Grain_number_{CurrentNOrientation}.csv'
df.to_csv('random_orien_num10000000_with_ran_position.csv',index=True,header=True)

'''

for fileNr in range(1,Iteration):
  CurrentNOrientation=int(TotalNOrientation*pow(percent,fileNr))
  
  OutFolder = f'{AnalyStem}/Grain_number_{CurrentNOrientation}'
  os.makedirs(OutFolder,exist_ok=True)
  
  OutFolder_ge3 = f'{AnalyStem}/ge3'
  os.makedirs(OutFolder_ge3,exist_ok=True)
  
  
  OutFile_temp = f'{OutFolder}/Grain_number_{CurrentNOrientation}_t.csv'
  OutFile = f'{OutFolder}/Grain_number_{CurrentNOrientation}.csv'
  param=f'{OutFolder}/ps_Grain_number_{CurrentNOrientation}.txt'
  paramFN = open(f'{OutFolder}/ps_Grain_number_{CurrentNOrientation}.txt', 'w')
  
  paramContents = open(SeedParam, 'r').readlines()
  for line in paramContents:
    paramFN.write(line)
  paramFN.write(f'InFileName {OutFolder}/Grain_number_{CurrentNOrientation}.csv\n')
  paramFN.write(f'OutFileName {OutFolder_ge3}/Grain_number_ff_{str(fileNr).zfill(6)}.ge3\n')
  paramFN.close()
  Currentlist=[]
  '''
  if CurrentNOrientation<(TotalNOrientation/2):
   while(len(Currentlist)<CurrentNOrientation):
    x=random.randint(0,CurrentNOrientation-1)
    if x not in Currentlist:
       Currentlist.append(x)
   df_current=df[df.index.isin(Currentlist)]
   df_current.to_csv(OutFile_temp,index=False,header=True)
  else:
   while(len(Currentlist)<(TotalNOrientation-CurrentNOrientation)):
    x=random.randint(0,(TotalNOrientation-CurrentNOrientation)-1)
    if x not in Currentlist:
       Currentlist.append(x)
       print(len(Currentlist))
   df_current=df[~df.index.isin(Currentlist)]
   df_current.to_csv(OutFile_temp,index=False,header=True)
  '''
  
  Currentlist=random.sample(range(0,TotalNOrientation),CurrentNOrientation)
  df_current=df[df.index.isin(Currentlist)]
  df_current.to_csv(OutFile_temp,index=False,header=True)
  ls=open(OutFile_temp).readlines()
  newTxt=""
  for line in ls:
   newTxt=newTxt+" ".join(line.split(","))
  fo=open(OutFile,"x")
  fo.write(newTxt)
  fo.close()
  os.remove(OutFile_temp)
  
  with open(OutFile,'r+') as f:
      content=f.read()
      f.seek(0,0)
      f.write(f'%NumGrains {CurrentNOrientation}\n%BeamCenter 2.079157\n%BeamThickness 500.000000\n%GlobalPosition 0.000000\n%NumPhases 1\n%PhaseInfo \n%SpaceGroup:225\n%Lattice Parameter: 3.593500 3.593500 3.593500 90.000000 90.000000 90.000000\n'+content)
  cmd1 = f'{expanduser("~/opt/MIDAS/FF_HEDM/bin/ForwardSimulation")} {param}'
  subprocess.call(cmd1,shell=True)




