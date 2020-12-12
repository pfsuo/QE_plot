import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('Agg')

nwan = 3
seedname='C2Li'
lw = 1.2
fontsize = 12
title='Wannier interpolation vs DFT'
ymin = -5
ymax = 5

## read fermi level from dos.dat
with open('../scf/dos.dat') as f:
    l=f.readline()
fermi=float(l.split()[-2])

klabels=[]
knodes=[]
kx=[]
## read k points from labelinfo.dat file
with open(seedname+'_band.labelinfo.dat') as f:
    l=f.readlines()
for i in range(len(l)):
    klabels.append(l[i].split()[0])
    knodes.append(int(l[i].split()[1]))
    kx.append(float(l[i].split()[2]))

## read band data from _band.dat file
k_vector=np.zeros(knodes[-1],dtype=float)
eig_wan=np.zeros((knodes[-1],nwan),dtype=float)
f=open(seedname+'_band.dat')
for i in range(nwan):
    for j in range(knodes[-1]):
        l=f.readline()
        k_vector[j]=l.split()[0]
        eig_wan[j,i]=l.split()[1]
    l=f.readline()
f.close()

## read DFT band structrue from bd.dat file
with open('bd.dat') as feig_DFT:
    l=feig_DFT.readline()
    nDFT=int(l.split(',')[0].split('=')[1])
    nks=int(l.split(',')[1].split('=')[1].split('/')[0])
    eig_DFT=np.zeros((nks,nDFT),dtype=float)
    for i in range(nks):
         l=feig_DFT.readline()
         count=0
         if nDFT%10==0:
             n=nDFT//10
         else:
             n=nDFT//10+1
         for j in range(n):
             l=feig_DFT.readline()
             for k in range(len(l.split())):
                 eig_DFT[i][count]=l.split()[k]
                 count+=1

## plot the bandstructrue
p1=plt.subplot(111)
F=plt.gcf()
## get current axes
ax=plt.gca()
F.set_size_inches([4.1,4])

plt.xlim([0,kx[-1]]) 
plt.ylabel('$E-E{_F}$ (eV) ',fontsize=fontsize)

plt.title(title, fontsize=fontsize)  
plt.plot(k_vector,eig_DFT[:,0]-fermi,color='r',label='DFT',linewidth=lw ) 
for i in range(1,nDFT):
    plt.plot(k_vector,eig_DFT[:,i]-fermi,color='r',linewidth=lw ) 
plt.plot(k_vector,eig_wan[:,0]-fermi,color='b',label='wannier90',linewidth=lw ) 
for i in range(1,nwan):
    plt.plot(k_vector,eig_wan[:,i]-fermi,color='b',linewidth=lw ) 

plt.axhline(xmin=0, xmax=knodes[-1], y=0 ,lw=lw,color='black',ls='--')
for i in range(len(kx)):
    plt.axvline(x=kx[i], ymin=ymin, ymax=ymax,linewidth=lw,color='black')

ax.set_xticks(kx)
ax.set_xticklabels(klabels)
plt.legend()

plt.ylim([-10,9.5])
plt.savefig('wannier_vs_DFT_whole.png',dpi=1000)
plt.ylim([ymin,ymax])
plt.savefig('wannier_vs_DFT_window.png',dpi=1000)
