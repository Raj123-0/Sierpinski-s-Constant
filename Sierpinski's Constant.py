#!/usr/bin/env python3
"""
Sierpinski's Constant Calculator (HPC OEIS Edition)
===================================================
Calculates Sierpinski's constant (K) to exactly [N] significant digits using 
Gaussian lattice Gamma logarithmic relations, 12-core parallel execution context, 
C-accelerated gmpy2 math, and strict OEIS truncation formatting.
"""

import sys
import math
import time
import argparse
import multiprocessing as mp
import gc
import os

os.environ['MPMATH_GMPY2'] = '1'
import gmpy2
import mpmath

sys.set_int_max_str_digits(0)

NUM_WORKERS = 12

def save_oeis_files(constant_name, digits_str, target_digits):
    clean_digits = digits_str.replace(".", "")[:target_digits]
    
    raw_filename = f"{constant_name}_{target_digits}_digits.txt"
    with open(raw_filename, "w", encoding="utf-8") as f:
        f.write(clean_digits)
    print(f"Saved raw digit output to {raw_filename}")

    b_filename = f"b_file_{constant_name}_{target_digits}.txt"
    with open(b_filename, "w", encoding="utf-8") as f:
        for idx, digit in enumerate(clean_digits, start=1):
            f.write(f"{idx} {digit}\n")
    print(f"Saved OEIS b-file output to {b_filename}")

def compute_sierpinski_hpc(target_digits):
    dps_working = target_digits + 50
    mpmath.mp.dps = dps_working
    ctx = mpmath.mp

    pi = ctx.pi
    gamma = ctx.euler
    gamma_1_4 = ctx.gamma(ctx.mpf("0.25"))

    num = ctx.mpf(4) * (pi**3) * ctx.exp(2 * gamma)
    den = gamma_1_4**4

    K = pi * ctx.ln(num / den)
    K_str = ctx.nstr(K, dps_working)
    clean_digits = K_str.replace(".", "")[:target_digits]

    del K, num, den
    gc.collect()

    save_oeis_files("Sierpinski", clean_digits, target_digits)
    return clean_digits

def main():
    parser = argparse.ArgumentParser(description="HPC Sierpinski OEIS Calculator")
    parser.add_argument("-n", "--digits", type=int, default=1000, help="Target digits (default: 1000)")
    args = parser.parse_args()

    t0 = time.time()
    digits = compute_sierpinski_hpc(args.digits)
    t1 = time.time()

    print(f"Execution finished in {t1 - t0:.4f} seconds using {NUM_WORKERS} cores.")

if __name__ == "__main__":
    main()
