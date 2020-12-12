import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

ymin=-5
ymax=5
dlines=[20, 40, 68, 103, 131]
xticks=(0,20, 40, 68, 103, 131 ,153)
xticklabels=('Γ', 'X', 'M', 'Γ', 'R', 'X|R', 'M')
## read fermi level from dos.dat file
with open('dos.dat') as dos:
    lines=dos.readline()
Efermi=float(lines.split()[-2])
lw=1.2 # line width
fontsize=12
title='Band structure of SmB${_6}$'

## read spin_up band data from bd1.dat file
with open('bd1.dat') as feig_up:
    l=feig_up.readline()
    nbnd=int(l.split(',')[0].split('=')[1])
    nks=int(l.split(',')[1].split('=')[1].split('/')[0])
    eig_up=np.zeros((nks,nbnd),dtype=float)
    for i in range(nks):
         l=feig_up.readline()
         count=0
         if nbnd%10==0:
             n=nbnd//10
         else:
             n=nbnd//10+1
         for j in range(n):
             l=feig_up.readline()
             for k in range(len(l.split())):
                 eig_up[i][count]=l.split()[k]
                 count+=1

## read spin_up band data from bd2.dat file
with open('bd2.dat') as feig_dn:
    l=feig_dn.readline()
    nbnd=int(l.split(',')[0].split('=')[1])
    nks=int(l.split(',')[1].split('=')[1].split('/')[0])
    eig_dn=np.zeros((nks,nbnd),dtype=float)
    for i in range(nks):
         l=feig_dn.readline()
         count=0
         if nbnd%10==0:
             n=nbnd//10
         else:
             n=nbnd//10+1
         for j in range(n):
             l=feig_dn.readline()
             for k in range(len(l.split())):
                 eig_dn[i][count]=l.split()[k]
                 count+=1

p1=plt.subplot(1, 1, 1)
F=plt.gcf()
F.set_size_inches([4.1,4])

plt.xlim([0,nks-1]) 
plt.ylim([ymin,ymax])
plt.ylabel('$E-E{_F}$ (eV) ',fontsize=fontsize)

plt.title(title, fontsize=fontsize)  
line1=plt.plot( eig_up[:,0]-Efermi,color='r',lw=lw, label='spin up' ) 
for i in range(1,nbnd):
    line1=plt.plot( eig_up[:,i]-Efermi,color='r',lw=lw ) 
line1=plt.plot( eig_dn[:,0]-Efermi,color='b',lw=lw, ls='--',label='spin down' ) 
for i in range(1,nbnd):
    line1=plt.plot( eig_dn[:,i]-Efermi,color='b',lw=lw,ls='--' ) 

plt.axhline(xmin=0, xmax=nks, y=0 ,lw=lw,color='black',ls='--')
for i in range(len(dlines)):
    vline=dlines[i]
    plt.axvline(x=vline, ymin=ymin, ymax=ymax,lw=lw,color='black',ls='--')

plt.xticks(xticks,xticklabels, fontsize=fontsize )
plt.legend()
plt.savefig('pwband_spin.png',dpi=1000)

