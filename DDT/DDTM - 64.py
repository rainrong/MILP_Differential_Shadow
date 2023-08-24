import numpy as np
#from scipy.linalg import solve
np.set_printoptions(threshold=np.inf) # np.inf表示正无穷
f1 = open(r"C:\Users\BIXINJIE\Desktop\DDTM-Shadow-64.txt","a+")

#循环左移
def Rotateleft(a,x,l):
    temp=x%l
    temp1=(a<<temp)%int(np.exp2(l))
    temp2=(a<<temp)/int(np.exp2(l))
    temp3=temp1+temp2
    return int(temp3)

#创建S盒
S_BOX=np.zeros((65536), dtype=int)#创建全0 S盒
for i in range(65536):
    S_BOX[i]=(Rotateleft(i,1,16)&Rotateleft(i,7,16))^Rotateleft(i,2,16)
    #S_BOX[i]=Rotateleft(i,1,8)&Rotateleft(i,7,8)
'''
print('S盒：')
print('S盒：',file=f1)    #s盒
for i in range(65536):
    print('{:<5d}'.format(i),'{:<5d}'.format(S_BOX[i]))
    print('{:<5d}'.format(i),'{:<5d}'.format(S_BOX[i]),file=f1)
'''   
#    print('{:<5d}'.format(i),',','{:<5d}'.format(S_BOX[i],end=' '),file=f1)    #s盒
    


#DDT = [[0] * 65536 for _ in range(65536)]   #语法水平orz...

for i in range(0,16):
    i2 = int(np.exp2(i))
    print('输入差分:')
    print('输入差分:',file=f1)
    print(' {:016b}'.format(i2),':')
    print(' {:016b}'.format(i2),':',file=f1)
    DDT = np.zeros((65536), dtype=int)
    for j in range(0, 65536):
        c = S_BOX[j] ^ S_BOX[j ^ i2]                             
        DDT[c]= DDT[c] + 1
    print('输出差分，概率:')
    print('输出差分，概率:',file=f1)
    for j in range(0, 65536):
        if DDT[j]!=0:
            print(' {:016b}'.format(j),', 2^%d'%np.log2(DDT[j]/65536))
            print(' {:016b}'.format(j),', 2^%d'%np.log2(DDT[j]/65536),file=f1)
            
        


