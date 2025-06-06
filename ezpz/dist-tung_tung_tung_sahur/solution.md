# Tung Tung Tung Sahur
In this challenge, we are given a python file and a text file which depicts the expected output of running the python code.
Clearly, from the code [tung_tung_tung_sahur.py](./tung_tung_tung_sahur.py), we can see that this is a twist on RSA encryption. 
The typical RSA key generation is given by public exponent e, large primes p, q and modulus N = p * q. 
```
e = 3
p, q = getPrime(512), getPrime(512)
N = p * q
```
- getPrime(n) is a function from the PyCryptodome library that returns a random prime number with a bit length of n.

The following code snippet reflects the message encoding and encryption.
```
m = bytes_to_long(flag.encode())
C = pow(m, e)
```
- flag.encode() converts the flag string to a bytes object using UTF-8.
- bytes_to_long() function from the PyCryptodome library converts the flag to a single large integer `m`.
- $C = m^e$  
Note that there is no modular reduction in C.

Following this we have artificial modifications, such that C is repeatedly multiplied by 2 until C >= N.
```
assert C < N 
while (C < N):
    C *= 2
    print("Tung!")
```
Then it subtracts N until C < N again.
```
while (C >= N):
    C -= N 
    print("Sahur!")
```
These modifications essentially reduce to `C = pow(m, e) % N`.

To solve it with RSA decryption, we will need to factor N to get p and q, in order to derive the private key. However since N is 1024-bit, factoring it is not feasible.

From [output.txt](./output,txt), we are given:  
- N
- C (the final output, ciphertext)
- "Tung!" printed 164 times; C *= 2 164 times
- "Sahur!" printed 1 time; C -= N once

Mathematically, 
C = (($m^3$) * $2^r$) - k\*N, where r is the number of times "Tung!" printed, k is the number of times "Sahur!" printed.
=> $m^3$ = (C + k\*N) // $2^r$  

∴ We need to reverse C to recover $m^3$ using C + k*N // $2^r$.  

Crafting [solve_tung.py](./solve_tung.py), we first define a custom implementation of computing the nth root of an integer `x` using binary search. The resulting function `integer_nthroot(x, n)` ensures the root is an integer, and tells you if it was exact. Alternatively, the `integer_nthroot()` function from sympy (a symbolic math library) has a very similar usage as well, and returns integer m, as well as if it is exact.  

We then define known values e, N, C, r and k as given in `output.txt`.  

Finally, we recover $m^3$ from the final C using
```
m_cubed = (C + k * N) // (2**r)
```
Before recovering plaintext m using our defined function
```
m, exact = integer_nthroot(m_cubed, 3)
```
Since m is still an integer, we need to convert it back to bytes using the `long_to_bytes()` function, then decode it to convert those bytes into a string to recover our original flag.

Running `solve_tung.py`, we get the flag:
```
Recovered flag: grey{tUn9_t00nG_t0ONg_x7_th3n_s4hUr}
```
