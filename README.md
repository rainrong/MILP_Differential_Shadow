# MILP_Differential_Shadow
This repository contains the programs for differential characteristic search for shadow ciphers based on MILP and differential uniformity solving for the equivalent S-box of the core encryption and decryption function module of shadow ciphers.

## Introduction
1. Shadow_Diff.py file to run on the Shadow cipher for any number of rounds of differential characteristic search, which can be constrained by the Init function on whether it is an iterative differential characteristic search, the default setting is now an iterative differential search. 
For solving the MILP modeling lp file we use the Gurobi solver.
2. In the Equivalent Difference Distribution folder, DDT-32.py and DDT-64.py solve the equivalent s-boxes, corresponding difference distributions, and difference uniformity of the Shadow-32 and Shadow-64 core modules, respectively, and finally output the results in the terminal and in the txt files under the corresponding path. It should be noted that because of the huge amount of data in the results, we have adopted the form of interlaced output of input difference-difference distribution table value-corresponding output difference, and ignored terms whose difference distribution is zero.

## Configuration
CPU model: AMD Ryzen 5 6600U with Radeon Graphics, instruction set [SSE2|AVX|AVX2]\
Gurobi Optimizer version 10.0.1 build v10.0.1rc0 (win64)\
Python 3.10.10 (tags/v3.10.10:aad5f6a, Feb  7 2023, 17:20:36) [MSC v.1929 64 bit (AMD64)] on win32


