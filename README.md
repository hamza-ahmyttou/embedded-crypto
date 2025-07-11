# Embedded Cryptography — Discrete Logarithms & Diffie-Hellman

This project implements fundamental algorithms in computational number theory and cryptography, including:

- Discrete Logarithm (DL) problem solvers
  - Trial Multiplication
  - Baby-Step Giant-Step (BSGS)
  - Pohlig-Hellman
- Group abstraction for `ZpAdditive` and `ZpMultiplicative`
- Diffie-Hellman key exchange simulation
- ASN.1 parsing of `dhParam.der` using `pyasn1`

## Features

- Modular group class with group law and exponentiation
- Subgroup with custom generators
- Efficient DL solving techniques
- Support for prime-power order subgroups
- Reversible Diffie-Hellman protocol with key validation
- Unit tests with `unittest` and `hamcrest`


[![codecov](https://codecov.io/github/hamza-ahmyttou/embedded-crypto//branch/main/graph/badge.svg)](https://codecov.io/github/hamza-ahmyttou/embedded-crypto)
