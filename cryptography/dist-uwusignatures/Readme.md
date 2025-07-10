# UWU Signatures
This challenge basically implements a digital signature scheme based on ElGamal-style signatures. The vulnerability likely lies how we can request two signatures on arbitrary messages (except the target message), and then attempt to forge a signature on the protected message "gib flag pls uwu". 

### Key Concepts
ElGamal-style Signature generation:
Given:

- p: large prime
- g: generator
- x: private key
- y = $g^x mod p$ = public key

To sign message m:

1. Hash message: h=SHA256(m)
2. Compute $r = g^k mod p$, for random k s.t. gcd(k,p−1) = 1
3. Compute $s=(h−x⋅r)⋅k^{−1} mod(p−1)$

Signature = (r,s)

Verification:
$g^h = y^r ⋅ r^s mod p$

### Attack vector: Signature Forgery
This scheme is not existentially unforgeable under chosen message attacks (EUF-CMA) if the attacker can obtain valid signatures and the hash function is predictable like SHA256.

1. Request two signatures: (m1, r1, s1) and (m2, r2, s2)
2. If both use the same r (i.e. the same k), we can compute the private key x:

     $s1 = (h1 - x ⋅ r) ⋅ k^{-1}$ &rarr; $h1 - s1 ⋅ k = x ⋅ r$  
     $s2 = (h2 - x ⋅ r) ⋅ k^{-1}$ &rarr; $h2 - s2 ⋅ k = x ⋅ r$
   
   Subtract:  
     $h1-h2 = (s1 - s2) ⋅ k &rarr; k = (h1-h2) ⋅ (s1-s2)^{-1} mod (p-1)$

   Then compute $x$ from either equation.

   Once $x$ is recovered, we can sign any message, including `"gib flag pls uwu"` to attain the flag.

   Flag: grey{h_h_H_h0wd_y0u_Do_tH4T_OMO}
