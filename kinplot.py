#!/usr/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob
import re

# extract D and Mn from GPC output files
def findvals():
    lines = [line.strip() for line in open(filename,encoding="ISO-8859-1")]
    for x in lines:
        match=re.search(r'^D:.*$',x)
        if match:
            D=x.lstrip('D:\t ')
            D=D.rstrip('\t')
            D=float(D)
        match=re.search(r'^Mn:.*$',x)
        if match:
            Mn=x.lstrip('Mn:\t ')
            Mn=Mn.rstrip('\tg/mol')
            Mn=float(Mn)
    return D,Mn

Dlist=[]
Mnlist=[]
tlist=[]
files=glob.glob('./* - 1.TXT')

# populate lists with values from GPC output files
for filename in files:
    D,Mn=findvals()
    t=filename[slice(21,-8)]
    t=t.rstrip('min')
    t=int(t)
    Dlist.append(D)
    Mnlist.append(Mn)
    tlist.append(t)

# plot scatter of points
plt.scatter(tlist,Mnlist)
x=np.array(tlist)
y=Mnlist
m, b = np.polyfit(x, y, 1)

# if not extrapolating:
#plt.plot(x, m*x + b)

# plot line of (x,y) points based on polyfit equation
x_out = np.linspace(0, 120, 20)   # 20 x values from 0 to 120
y_pred = np.polyval([m, b], x_out)
plt.plot(x_out, y_pred, label="y={:.3f}x+{:3.3f}".format(m,b))

# find R^2
correlation_matrix = np.corrcoef(x, y)
correlation_xy = correlation_matrix[0,1]
r_squared = correlation_xy**2

# fake line to add R^2 to legend
plt.plot([], [], color="w", label='R$^2$={:3.5f}'.format(r_squared))

# plot parameters
plt.ylim(0,50000)
plt.ylabel('Mn/gmol$^{-1}$')
plt.xlabel('Time/min')
plt.legend()
plt.savefig('kinplot.png')

# make latex table
Mnlist4=(f/1E4 for f in Mnlist)
data = pd.DataFrame(
    {'Time/m': tlist,
     'Mn/gmol$^{-1}$ (x10$^4$)': Mnlist4,
     'D': Dlist
    })
data = data.sort_values(by=['Time/m'])
with open('kintable.tex', 'w') as tf:
    tf.write(data.to_latex(index=False,escape=False,column_format='rcc').replace('\\begin{tabular}','\\begin{tabular}[b]'))

