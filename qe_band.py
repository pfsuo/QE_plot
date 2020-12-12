import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

## read band data from bd.dat
ymin=-5
ymax=5
dlines=[20, 40, 68, 103, 131]
xticks=(0,20, 40, 68, 103, 131 ,153)
xticklabels=('Γ', 'X', 'M', 'Γ', 'R', 'X|R', 'M')
with open('dos.dat') as dos:
    lines=dos.readline()
Efermi=float(lines.split()[-2])
lw=1.2 # line width
fontsize=12
title='Band structure of SmB${_6}$'

with open('bd.dat') as feig:
    l=feig.readline()
    nbnd=int(l.split(',')[0].split('=')[1])
    nks=int(l.split(',')[1].split('=')[1].split('/')[0])
    eig=np.zeros((nks,nbnd),dtype=float)
    for i in range(nks):
         l=feig.readline()
         count=0
         if nbnd%10==0:
             n=nbnd//10
         else:
             n=nbnd//10+1
         for j in range(n):
             l=feig.readline()
             for k in range(len(l.split())):
                 eig[i][count]=l.split()[k]
                 count+=1

p1=plt.subplot(1, 1, 1)
F=plt.gcf()
F.set_size_inches([4.1,4])

plt.xlim([0,nks-1]) 
plt.ylim([ymin,ymax])
plt.ylabel('$E-E{_F}$ (eV) ',fontsize=fontsize)

plt.title(title, fontsize=fontsize)  
for i in range(nbnd):
    line1=plt.plot( eig[:,i]-Efermi,color='r',linewidth=lw ) 

plt.axhline(xmin=0, xmax=nks, y=0 ,lw=lw,color='black',ls='--')
for i in range(len(dlines)):
    vline=dlines[i]
    plt.axvline(x=vline, ymin=ymin, ymax=ymax,linewidth=lw,color='black',ls='--')

plt.xticks(xticks,xticklables, fontsize=fontsize )

plt.savefig('pwband.png',dpi=1000)

