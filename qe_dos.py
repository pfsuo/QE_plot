import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('Agg')

title = 'Density of States'
lw = 1.2
fontsize = 12

f = open('dos.dat')
l = f.readline()
efermi = float(l.split()[-2])

dos = np.loadtxt('dos.dat')
if len(dos[0,:]) == 3:
    p1=plt.subplot(1, 1, 1)
    F=plt.gcf()
    F.set_size_inches([6.1,4])

    plt.xlim([-5,5]) 
    plt.ylim(ymin=0)
    plt.xlabel('Energy (eV) ',fontsize=fontsize)
    plt.ylabel('DOS (States/eV) ',fontsize=fontsize)
    plt.title(title, fontsize=fontsize)  
    line1=plt.plot( dos[:,0]-efermi, dos[:,1] ,color='r',linewidth=lw ) 
    plt.axvline(x=0,lw=lw,ls='--')
    plt.fill_between(dos[:,0]-efermi,0,dos[:,1],where=dos[:,1]>=0,facecolor='silver',interpolate=True)
    plt.savefig('DOS.png',dpi=1000)
    
elif len(dos[0,:]) == 4:
    p1=plt.subplot(1, 1, 1)
    F=plt.gcf()
    F.set_size_inches([8.1,4])

    plt.xlim([-5,5]) 
    plt.ylim(ymin=0)
    plt.xlabel('Energy (eV) ',fontsize=fontsize)
    plt.ylabel('DOS (States/eV) ',fontsize=fontsize)
    plt.title(title, fontsize=fontsize)  
    line1=plt.plot( dos[:,0]-efermi, dos[:,1] ,color='r',linewidth=lw, label='spin up' ) 
    line2=plt.plot( dos[:,0]-efermi,-dos[:,2] ,color='k',linewidth=lw,ls='--',label='spin down') 
    plt.fill_between(dos[:,0]-efermi,0,dos[:,1],where=dos[:,1]>=0,facecolor='silver',interpolate=True)
    plt.fill_between(dos[:,0]-efermi,0,-dos[:,2],where=-dos[:,1]<=0,facecolor='silver',interpolate=True)
    plt.axhline(y=0,lw=lw,ls='--')
    plt.axvline(x=0,lw=lw,ls='--')
    plt.legend()
    plt.savefig('DOS.png',dpi=1000)
