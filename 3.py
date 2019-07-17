def RC4(key):
    N=256
    S=T=K=[N]
    for i in range(N):
        S[i]=i
        T[i]=K[i%5]
    for i in range(N):
        j=0
        j=(j+S[i]+T[i])%N
        temp=S[i]
        S[i]=S[j]
        S[j]=temp
    for r in range(key):
        i=j=t=0
        i=(i+1)%N
        j=(j+S[i])%N
        temp = S[i]
        S[i] = S[j]
        S[j] = temp
        t=(S[i]+S[j])%N
        K[r] = S[t]
        return k[r]


def main():
    h=RC4(6)
    print(h)

if __name__ == '__main__':
    main()

