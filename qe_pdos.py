import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('Agg')

lw = 1.2
fontsize = 12
dos = [line for line in open('dos.dat') if line.strip()]
efermi = float(dos[0].split()[-2])

## the information of elements and orbitals
elem=['Sm','B']
ielem=np.array([1,6],dtype=np.int32) # number of atoms for each element
orb=[['s', 's', 'p', 'p', 'd', 'd', 'f', 'f'],['s','p']]  # projectors for each element
color=['g','r','black', 'cyan']
label=['B s', 'B p', 'Sm 3d', 'Sm 4f']
odos=[[8,10,12,14,16,18],
[9,11,13,15,17,19],
[4],
[6]]

N=len(elem)
iorb=np.zeros([N,],dtype=np.int32)  # number of projectors for each element
for i in range(N):
    iorb[i]=len(orb[i])
num_file=np.dot(ielem,iorb)
nat=np.sum(ielem)
D=[]

#scf ATOMIC_POSITIONS should be sorted in the same order as above
count=0
count_at=0
for n in range(N):
    for i in range(ielem[n]):
        for j in range(iorb[n]):
            print(n,i,j,count_at+1,elem[n],j+1,orb[n][j])
            fname='sno.pdos_atm#{}({})_wfc#{}({})'.format(count_at+1,elem[n],j+1,orb[n][j])
            D.append(np.loadtxt(fname,dtype=np.float32))
            count+=1
        count_at+=1

F = plt.gcf()
F.set_size_inches([4.1,4])
p1 = plt.subplot(111)

for i in range(len(odos)):
    pdos = np.zeros([len(D[0][:,0]),])
    for j in odos[i]:
        pdos += D[j][:,1]
    line1 = plt.plot(D[0][:,0]-efermi,pdos,color=color[i],lw=lw,label=label[i])

plt.xlim([-15,15])
plt.ylim(ymin=0,ymax=5)
plt.ylabel(r'DOS (a.u.)',fontsize=fontsize)
plt.xlabel(r'E (eV) ',fontsize=fontsize)
plt.legend()
plt.savefig('pdos.png',dpi=1000)
