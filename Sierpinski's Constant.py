#!/usr/bin/env python3
"""
Sierpinski's Constant Calculator
================================
Calculates Sierpinski's constant (K) to a specified number of significant
digits using Gaussian lattice Gamma logarithmic relations, with gmpy2-accelerated
mpmath arithmetic and strict OEIS truncation formatting.

Formula:
    K = pi * ln(4 * pi^3 * exp(2*gamma) / Gamma(1/4)^4)

Known value (OEIS A240882): 2.584981759579253...
"""

import argparse
import os
import sys
import time

os.environ.setdefault("MPMATH_GMPY2", "1")

import gmpy2  # noqa: F401 — imported to enable the gmpy2 backend for mpmath
import mpmath

sys.set_int_max_str_digits(0)


def save_oeis_files(constant_name: str, digits_str: str, target_digits: int) -> None:
    """Save raw digits and an OEIS b-file for the given constant.

    Parameters
    ----------
    constant_name:
        Name used in output filenames.
    digits_str:
        Decimal-expansion string (decimal point may be present; it is stripped).
    target_digits:
        Number of significant digits to retain.
    """
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


def compute_sierpinski(target_digits: int) -> str:
    """Compute Sierpinski's constant to *target_digits* significant digits.

    Returns the digit string (decimal point removed, truncated to
    *target_digits* characters) and writes OEIS-format output files.
    """
    working_dps = target_digits + 50
    mpmath.mp.dps = working_dps
    ctx = mpmath.mp

    pi = ctx.pi
    gamma = ctx.euler
    gamma_1_4 = ctx.gamma(ctx.mpf("0.25"))

    numerator = ctx.mpf(4) * pi**3 * ctx.exp(2 * gamma)
    denominator = gamma_1_4**4

    K = pi * ctx.ln(numerator / denominator)
    K_str = ctx.nstr(K, working_dps)
    clean_digits = K_str.replace(".", "")[:target_digits]

    save_oeis_files("Sierpinski", clean_digits, target_digits)
    return clean_digits


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sierpinski's Constant OEIS Calculator"
    )
    parser.add_argument(
        "-n", "--digits", type=int, default=1000,
        help="Target significant digits (default: 1000)",
    )
    args = parser.parse_args()

    t0 = time.time()
    compute_sierpinski(args.digits)
    t1 = time.time()

    print(f"Execution finished in {t1 - t0:.4f} seconds.")


if __name__ == "__main__":
    main()
