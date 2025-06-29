from Crypto.Util.number import long_to_bytes

#Alternatively
#from sympy import integer_nthroot

def integer_nthroot(x, n):
    if x < 0:
        raise ValueError("Cannot compute root of negative number")
    if x == 0:
        return 0, True

    low, high = 0, x
    while low < high:
        mid = (low + high) // 2
        mid_pow = pow(mid, n)
        if mid_pow == x:
            return mid, True
        elif mid_pow < x:
            low = mid + 1
        else:
            high = mid

    root = low - 1
    return root, (pow(root, n) == x)


e = 3
N = 140435453730354645791411355194663476189925572822633969369789174462118371271596760636019139860253031574578527741964265651042308868891445943157297334529542262978581980510561588647737777257782808189452048059686839526183098369088517967034275028064545393619471943508597642789736561111876518966375338087811587061841
C = 49352042282005059128581014505726171900605591297613623345867441621895112187636996726631442703018174634451487011943207283077132380966236199654225908444639768747819586037837300977718224328851698492514071424157020166404634418443047079321427635477610768472595631700807761956649004094995037741924081602353532946351

r = 164  # count of "Tung!"
k = 1    # count of "Sahur!"

m_cubed = (C + k * N) // (2**r)

m, exact = integer_nthroot(m_cubed, 3)

if exact:
    flag = long_to_bytes(m).decode()
    print("Recovered flag:", flag)
else:
    print("Cube root not exact. Check the counts and data.")
