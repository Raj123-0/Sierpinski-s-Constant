[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

===============================================================================
PROJECT: Sierpinski's Constant Computation Engine
===============================================================================

OVERVIEW:
Calculates Sierpinski's constant (K ≈ 2.58498175957925321706...) to arbitrary 
precision (N digits). K specifies the second-order asymptotic term for sum-of-squares 
lattice point counting.

ALGORITHM & MATHEMATICS:
- Closed-Form Logarithmic Gamma Relation:
    K = pi * ln( (4 * pi^3 * e^(2 * gamma)) / Gamma(1/4)^4 )
- Evaluated using high-precision Euler-Mascheroni and Gamma functions in mpmath + gmpy2.

## Usage

```bash
python "Sierpinski's Constant.py" --help
```
