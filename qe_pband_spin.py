import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# plot range for y-axis
ymin=-5
ymax=5
dlines=[20, 40, 68, 103, 131]
xticks=(0,20, 40, 68, 103, 131 ,153)
xticklabels=('Γ', 'X', 'M', 'Γ', 'R', 'X|R', 'M')
lw=0.5 # line width
with open('dos.dat') as dos:
    lines=dos.readline()
efermi=float(lines.split()[-2])

elem=['B','Sm']
ielem=np.array([6,1],dtype=np.int32) # number of atoms for each element
orb=[['s','p'],['s', 's', 'p', 'p', 'd', 'd', 'f', 'f']]  # projectors for each element
# oo, orbital index for each kind of color, oo can be generated by the following commands
#grep '[a-zA-Z]' sno.projwfc_up |grep 'Li  2S'|awk '{printf( $1-1",")}'    for 2S of Li
#grep '[a-zA-Z]' sno.projwfc_up |grep 'C   2S'|awk '{printf( $1-1",")}'    for 2S of C
oo=[[32,36,40,44,48,52],
[33,34,35,37,38,39,41,42,43,45,46,47,49,50,51,53,54,55],
[8,9,10,11,12],
[18,19,20,21,22,23,24]]
color=['g','r','black', 'cyan']
label=['B s', 'B p', 'Sm 3d', 'Sm 4f']

feig_up=open('bd1.dat')
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
            count=count+1

feig_up.close()

F=plt.gcf()
F.set_size_inches([6,4.5])
p1=plt.subplot(1, 1, 1)

for i in range(nbnd):
    line1=plt.plot(np.arange(0,nks), eig_up[:,i]-efermi,color='grey',linewidth=lw )

for i in range(len(dlines)):
    vline=dlines[i]
    plt.axvline(x=vline, ymin=ymin, ymax=ymax,linewidth=lw,ls='--',color='black')
plt.axhline(xmin=0, xmax=nks, y=0, lw=lw,color='black',ls='--')

N=len(elem)
iorb=np.zeros([N,],dtype=np.int32)  # number of projectors for each element
for i in range(N):
    iorb[i]=len(orb[i])

lorb=np.zeros([N,],dtype=np.int32) # number of local orbital for each element
for i in range(N):
    for j in orb[i]:
        if j == 's':
            lorb[i]+=1
        elif j == 'p':
            lorb[i]+=3
        elif j == 'd':
            lorb[i]+=5
        elif j == 'f':
            lorb[i]+=7
        else:
            print("unexpect: ",j)
            assert False

nlorb=np.dot(ielem,lorb)

pjsum=np.zeros([nlorb, nks, nbnd], dtype=np.float32)

filproj=open('sno.projwfc_up')
nline_io_header=15 # line number at '    F    F'

for i in range(nline_io_header):
    filproj.readline()

for i in range(nlorb):
    filproj.readline()
    for j in range(nks):
        for k in range(nbnd):
            pjsum[i,j,k]=float(filproj.readline().split()[2])
filproj.close()
nplotline=np.sum(iorb)

s_of_o=np.zeros([nks,],dtype=np.float32)

scale=90.0
st=[]
for i in range(len(oo)):
    for k in range(nbnd):
        s_of_o=np.zeros([nks,],dtype=np.float32)
        for j in oo[i]:
            s_of_o[:]+=pjsum[j,:,k]
        if k == 0:
            st.append(plt.scatter(-1, ymin-1, 20, c=color[i], alpha=0.5, label=label[i],marker='.',edgecolor='none'))
        st.append(plt.scatter(np.arange(0,nks), eig_up[:,k]-efermi, s=scale*s_of_o, c=color[i], alpha=0.5, marker='.',edgecolor='none'))

plt.xlim([0,nks-1]) # 201 points
plt.ylabel('E-E${_F}$ (eV)',fontsize=12)
plt.xticks( xticks,xticklabels, fontsize=12 )
plt.title('bandstructure of SmB$_6$', fontsize=12)

plt.subplots_adjust(left=0.20, right=0.75, top=0.95, bottom=0.1)
p1.legend(scatterpoints =1, numpoints=1,markerscale=2.0, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

plt.ylim([-16,20])
plt.savefig('pband_whole_up.png',dpi=1000)
plt.ylim([ymin,ymax])
plt.savefig('pband_up.png',dpi=1000)
plt.close()


feig_down=open('bd2.dat')
l=feig_down.readline()
eig_down=np.zeros((nks,nbnd),dtype=float)
for i in range(nks):
    l=feig_down.readline()
    count=0
    if nbnd%10==0:
        n=nbnd//10
    else:
        n=nbnd//10+1
    for j in range(n):
        l=feig_down.readline()
        for k in range(len(l.split())):
            eig_down[i][count]=l.split()[k]
            count=count+1

feig_down.close()
F=plt.gcf()
F.set_size_inches([6,4.5])
p1=plt.subplot(1, 1, 1)
for i in range(nbnd):
    line1=plt.plot(np.arange(0,nks), eig_down[:,i]-efermi,color='grey',linewidth=lw )

for i in range(len(dlines)):
    vline=dlines[i]
    plt.axvline(x=vline, ymin=ymin, ymax=ymax,linewidth=lw,ls='--',color='black')
plt.axhline(xmin=0, xmax=nks, y=0, lw=lw,color='black',ls='--')

pjsum=np.zeros([nlorb, nks, nbnd], dtype=np.float32)

filproj=open('sno.projwfc_down')
nline_io_header=15 # line number at '    F    F'

for i in range(nline_io_header):
    filproj.readline()

for i in range(nlorb):
    filproj.readline()
    for j in range(nks):
        for k in range(nbnd):
            pjsum[i,j,k]=float(filproj.readline().split()[2])
filproj.close()

st=[]
for i in range(len(oo)):
    for k in range(nbnd):
        s_of_o=np.zeros([nks,],dtype=np.float32)
        for j in oo[i]:
            s_of_o[:]+=pjsum[j,:,k]
        if k == 0:
            st.append(plt.scatter(-1, ymin-1, 20, c=color[i], alpha=0.5, label=label[i],marker='.',edgecolor='none'))
        st.append(plt.scatter(np.arange(0,nks), eig_down[:,k]-efermi, s=scale*s_of_o, c=color[i], alpha=0.5, marker='.',edgecolor='none'))

plt.xlim([0,nks-1]) # 201 points
plt.ylabel('E-E${_F}$ (eV)',fontsize=12)
plt.xticks(xticks,xticklabels,fontsize=12 )
plt.title('bandstructure of SmB$_6$', fontsize=12)

plt.subplots_adjust(left=0.20, right=0.75, top=0.95, bottom=0.1)
p1.legend(scatterpoints =1, numpoints=1,markerscale=2.0, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

plt.ylim([-16,20])
plt.savefig('pband_whole_down.png',dpi=1000)
plt.ylim([ymin,ymax])
plt.savefig('pband_down.png',dpi=1000)
plt.close()
