from random import randint
long=0;count=0
for i in range(100):
    x=randint(0,1)
    print(x,end='   ')
    if not x:
        count+=1
    else:
       if long<count:   
            long=count
       count=0
print("\nLongest run of 0's:",end='')
print(long)