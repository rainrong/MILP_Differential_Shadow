import numpy as np
#from scipy.linalg import solve
np.set_printoptions(threshold=np.inf) # np.inf表示正无穷
f1 = open(r"C:\Users\BIXINJIE\Desktop\Sbox&DDT-Shadow-64.txt","a+")

'''
#创建s盒法1
#bit转字节_s盒
def text_bit_halfbyte(A,S):
    for i in range(256):
        for j in range(8):
            S[i]+=A[i][j]*np.exp2(j)

X = np.zeros((256, 8), dtype=int)#创建全0二进制s盒
Y = np.zeros((256, 8), dtype=int)#创建全0二进制s盒
for i in range(256):
    str=bin(i);
    l=len(str)
    for j in range(2,l):
        X[i][j-2]=str[l+1-j];#低位在前
    for j in range(8):
        Y[i][j]=X[i][(j+6)%8]^(X[i][(j+7)%8]&X[i][(j+1)%8])
#创建S盒
S_BOX=np.zeros((256), dtype=int)#创建全0 S盒
text_bit_halfbyte(Y,S_BOX)

'''
#创建s盒法2
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

print('S盒：')
print('S盒：',file=f1)    #s盒
for i in range(65536):
    print('{:<5d}'.format(i),'{:<5d}'.format(S_BOX[i]))
    print('{:<5d}'.format(i),'{:<5d}'.format(S_BOX[i]),file=f1)



print('差分分布表：')
print('差分分布表：',file=f1)    
#求解差分均匀度
DD = np.zeros((65536), dtype=int)#创建全0差分分布表-单行
DD[0]=65536;
print('α=0\n')
print('α=0\n',file=f1)    #s盒
print('[')
print('[',file=f1)
print('65536',':')
print('65536',':',file=f1)
print('0',':')
print('0',':',file=f1)
print(']')  
print(']',file=f1) 

#a=1;b=1;#1行1列不计算。错！非双射S盒需计算输入差分非0输出差分为0情况
number_final = 0;#差分均匀度
for a in range(1,65536):
    print('α=',a)
    print('α=',a,file=f1)    #输入差分α      
    DD = np.zeros((65536), dtype=int)#创建全0差分分布表-单行
    for i in range(65536):
            b = S_BOX[i]^S_BOX[i^a]
            DD[b]+=1;
    temp = np.max(DD)
    if number_final<temp:
            number_final=temp;
            
    print('[')
    print('[',file=f1)
    print(temp,':')
    print(temp,':',file=f1)
    for j in range(65536):        
        if DD[j] == temp:
            print(j,end=' ')
            print(j,end=' ',file=f1)
    print(']')  
    print(']',file=f1) 

print("差分均匀度：",int(number_final))#输出差分均匀度
print("差分均匀度：",int(number_final),file=f1)#输出差分均匀度

'''
print("差分均匀度：",int(number_final))#输出差分均匀度
print("差分分布表：")
print(DD)    #输出差分分布表        

print("差分均匀度：",int(number_final),file=f1)#输出差分均匀度
print("差分分布表：",file=f1)
#print(DD,file=f1)    #输出差分分布表               
for i in range(256):
    print('输入差分：',i,file=f1)
    for j in range(256):
        print('输出差分',j,'  ',DD[i][j],file=f1)
'''    
'''
#输出差分始终为0的具体输入差分 & 不可能输出的差分
test1 = np.zeros((256), dtype=int)#
test2 = np.zeros((256), dtype=int)#
for i in range(256):
    temp1=0
    temp2=0
    temp3=0
    for j in range(256):
        temp1+=DD[i][j]
        temp2+=DD[j][i]
   
    test1[i]=temp1
    test2[i]=temp2

#print('输出差分始终为0的具体输入差分:')
print('输入差分对应行加和:')
print(test1)
#print('不可能输出的差分:')
print('输出差分对应列加和:')
print(test2)

#print('输出差分始终为0的具体输入差分:')
print('输入差分对应行加和:',file=f1)
print(test1,file=f1)
#print('不可能输出的差分:')
print('输出差分对应列加和:',file=f1)
print(test2,file=f1)
'''



'''
#print('差分均匀度对应输入差分:')#1
#print('0000*0*0对应输出差分模式:')#2
#print('0001*0*0对应输入差分模式:')#3
#COUNT=0
for i in range(256):
    temp1=0
    temp2=0
    temp3=0
    for j in range(256):
        temp1+=DD[i][j]
        temp2+=DD[j][i]
        #1、差分均匀度对应输入差分
        if (DD[i][j]==64)&(temp3==0):
            temp3+=1
            print(i,end=' ')
        #2、0000*0*0对应输出差分模式
        #if ((i==0)|(i==2)|(i==8)|(i==10))&(DD[i][j]!=0):
        #    print(' {:08b}'.format(j),',',j)
        #3、'0001*0*0对应输入差分模式
        #if ((j==16)|(j==18)|(j==26)|(j==24))&(DD[i][j]!=0)&(temp3==0):
        #    temp3+=1
        #    print('{:08b}'.format(i),' 对应',i,)
        #    COUNT+=1
            
#print(COUNT)
'''