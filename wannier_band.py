import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('Agg')

nbnd = 30
seedname='wannier90'
lw = 1.2
fontsize = 12
title='bandstructrue by wannier interpolation'
ymin = -4
ymax = 3

## read fermi level from dos.dat
with open('../DOS/DOSCAR') as f:
    for _ in range(6):
        l=f.readline()
fermi=float(l.split()[-2])

klabels=[]
knodes=[]
kx=[]
## read k points from labelinfo.dat file
with open(seedname+'_band.labelinfo.dat') as f:
    l=f.readlines()
for i in range(len(l)):
    knodes.append(int(l[i].split()[1]))
    kx.append(float(l[i].split()[2]))
    if i > 0 and kx[-1] == kx[-2]:
        klabels.append(l[i-1].split()[0] + '|' + l[i].split()[0])
    else:
        klabels.append(l[i].split()[0])

## read band data from _band.dat file
k_vector=np.zeros(knodes[-1],dtype=float)
eig=np.zeros((knodes[-1],nbnd),dtype=float)
f=open(seedname+'_band.dat')
for i in range(nbnd):
    for j in range(knodes[-1]):
        l=f.readline()
        k_vector[j]=l.split()[0]
        eig[j,i]=l.split()[1]
    l=f.readline()
f.close()

## plot the bandstructrue
p1=plt.subplot(111)
F=plt.gcf()
## get current axes
ax=plt.gca()
F.set_size_inches([4.1,4])

plt.xlim([0,kx[-1]]) 
plt.ylim([ymin,ymax])
plt.ylabel('$E-E{_F}$ (eV) ',fontsize=fontsize)

plt.title(title, fontsize=fontsize)  
for i in range(nbnd):
    line1=plt.plot(k_vector,eig[:,i]-fermi,color='r',linewidth=lw ) 

plt.axhline(xmin=0, xmax=knodes[-1], y=0 ,lw=lw,color='black',ls='--')
for i in range(len(kx)):
    plt.axvline(x=kx[i], ymin=ymin, ymax=ymax,linewidth=lw,color='black')

#plt.xticks( (0,60,90,150), ('Γ', 'K', 'M', 'Γ'), fontsize=fontsize )
ax.set_xticks(kx)
ax.set_xticklabels(klabels)

plt.savefig('wannier_band.png',dpi=1000)
