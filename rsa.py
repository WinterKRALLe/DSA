import random, math

def miller_rabin(n):
    if n % 2 == 0:
        return False
    u = n - 1
    k = 0
    while (u % 2 == 0):
        u //= 2
        k+=1
    a = random.randint(2,n-2)
    b = pow(a,u,n)
    if b==1 or b ==n-1:
        return True
    for _ in range (1,k-1):
        b= (b*b) % n
        if b==n-1: return True 
        if b==1: return False
    return False


def generateKeys():
        while True:
            p = random.randint(1*10**21, 1*10**22-1)
            q = random.randint(1*10**21, 1*10**22-1)
            if miller_rabin(p) == True and miller_rabin(q) == True and p != q:
                break
        n = p * q
        Fn = (p - 1)*(q - 1)
        while True:
            e = random.randint(2, Fn-1)
            if math.gcd(e, Fn) == 1:
                break
        d = pow(e, -1, Fn)
        return(n,e,d)
