import random, math, base64

X = 12
z = 10
block = z * X


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


def encode(text, n, d):
    OTblocks = [ord(char) for char in text]
    BINblocks = [bin(ch)[2:] for ch in OTblocks]
    BIN = "".join(BINblocks)
    filled = len(BIN) % block
    if filled:
        BIN = "0"*(block - filled) + BIN
    BINs = [BIN[i:i + block] for i in range(0, len(BIN), block)]
    INTblocks = [int(ch, 2) for ch in BINs]
    c = [pow(ch, d, n) for ch in INTblocks]
    signature = " ".join([str(ch) for ch in c])
    return signature


def decode(text, n, e):
    INTblocks = [int(ch) for ch in text.split(" ")]
    m = [pow(c, e, n) for c in INTblocks]
    BINblocks = [bin(ch)[2:].zfill(block) for ch in m]
    BIN = "".join(BINblocks)
    BINs = [BIN[i:i + X] for i in range(0, len(BIN), X)]
    oBINs = [char for char in BINs if int(char) != 0]
    INTs = [int(ch, 2) for ch in oBINs]
    output = [chr(ch) for ch in INTs]
    output = "".join(output)
    return output


def encodeBase64(text):
    sample_string_bytes = text.encode("ascii")
    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string


def decodeBase64(text):
    base64_bytes = text.encode("ascii")
    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("ascii")
    return sample_string


def encodeKeyBase64(fi, se):
	key = str(fi) + " " + str(se)
	encoded = encodeBase64(key)
	return encoded


def decodeKeyBase64(key):
	decoded = decodeBase64(key)
	fi, se = decoded.split()
	return int(fi), int(se)
