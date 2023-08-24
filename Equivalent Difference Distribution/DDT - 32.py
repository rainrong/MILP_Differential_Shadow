import numpy as np
#from scipy.linalg import solve
np.set_printoptions(threshold=np.inf) # np.inf表示正无穷
f1 = open(r"C:\Users\BIXINJIE\Desktop\Sbox&DDT-Shadow-32.txt","a+")

#循环左移
def Rotateleft(a,x,l):
    temp=x%l
    temp1=(a<<temp)%int(np.exp2(l))
    temp2=(a<<temp)/int(np.exp2(l))
    temp3=temp1+temp2
    return int(temp3)

#创建S盒
S_BOX=np.zeros((256), dtype=int)#创建全0 S盒
for i in range(256):
    #S_BOX[i]=(Rotateleft(i,1,16)&Rotateleft(i,7,16))^Rotateleft(i,2,16)
    S_BOX[i]=Rotateleft(i,1,8)&Rotateleft(i,7,8)^Rotateleft(i,2,8)

print('S盒：')
print('S盒：',file=f1)    #s盒
for i in range(256):
    print('{:<3d}'.format(i),'{:<3d}'.format(S_BOX[i]))
    print('{:<3d}'.format(i),'{:<3d}'.format(S_BOX[i]),file=f1)
    
#    print('{:<16d}'.format(i),',','{:<16d}'.format(S_BOX[i],end=' '),file=f1)    #s盒
    


#DDT = [[0] * 256 for _ in range(256)]   #语法水平orz...
           
        
print('差分分布表：')
print('差分分布表：',file=f1)    
'''  
It is important to note that the function that outputs the differential distribution here is not universal.
'''
DD = np.zeros((256), dtype=int)#创建全0差分分布表-单行
DD[0]=256;
print('α=0\n')
print('α=0\n',file=f1)    #s盒
print('[')
print('[',file=f1)
print('256',':')
print('256',':',file=f1)
print('0',':')
print('0',':',file=f1)
print(']')  
print(']',file=f1) 


#a=1;b=1;#1行1列不计算。错！非双射S盒需计算输入差分非0输出差分为0情况
number_final = 0;#差分均匀度
for a in range(1,256):
    print('α=',a)
    print('α=',a,file=f1)    #输入差分α      
    DD = np.zeros((256), dtype=int)#创建全0差分分布表-单行
    for i in range(256):
            b = S_BOX[i]^S_BOX[i^a]
            DD[b]+=1;
    temp = np.max(DD)
    if number_final<temp:
            number_final=temp;
            
    print('[')
    print('[',file=f1)
    print(temp,':')
    print(temp,':',file=f1)
    for j in range(256):        
        if DD[j] == temp:
            print(j,end=' ')
            print(j,end=' ',file=f1)
    print(']')  
    print(']',file=f1) 

print("差分均匀度：",int(number_final))#输出差分均匀度
print("差分均匀度：",int(number_final),file=f1)#输出差分均匀度
