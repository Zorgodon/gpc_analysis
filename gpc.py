#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob

def findlines():
    with open(filename, 'r',encoding="ISO-8859-1") as f:
        for i,row in enumerate(f):
            if row.rstrip() == 'ELUstart :':
                first=(i+1)
            elif row.rstrip() == 'ELUstop :':
                last=i
        return first,last

def doplot():
    df=pd.read_csv(filename,encoding='latin1',
            sep='\t',index_col=False,skipinitialspace=True,
            skiprows=first,nrows=(last-first-2))
    
    df=df.astype(float) # important as we had strings in our columns which throws python off
    
    df['normalized']=df['I1: RID 1, RI Signal']/df['I1: RID 1, RI Signal'].max()
    
    df.plot.line(x='Molar mass',y='normalized',legend=None)
    plt.xlabel('Mw/gmol$^{-1}$')
    plt.ylabel('Relative Intensity (normalized)')
    plt.xscale('log')
    figname=filename[slice(21,-8)]
    figname=figname.lstrip(' ')
    plt.savefig(figname)

    # get max Mw values
    #maxrow=df.loc[[df['normalized'].idxmax()]]
    #print(maxrow['Molar mass'])
    #plt.show()

files=glob.glob('./* - 1.TXT')
for filename in files:
    first,last=findlines()
    doplot()

