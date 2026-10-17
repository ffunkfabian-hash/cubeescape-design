#!/usr/bin/env python3
"""Build and capture both independent series in one Mac heavy_lock time band.

Run this script through heavy_lock; it does not acquire nested locks.
"""
import build
import compare


def main():
    for family in ('parallax','fluxbloom'):
        build.main(['--collection',family])
    compare.main()


if __name__=='__main__':main()
