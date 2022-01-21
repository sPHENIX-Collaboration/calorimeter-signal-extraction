---
title: "Test Beam Data"
layout: base
name: test_beam
---

# Test Beam Data

Current studies rely on the test beam data collected in 2018.
In particular, data samples corresponging to electron beam
energies of 2, 3, 4, 6, 8, 16 and 28GeV have been used.

A typical file prepared for use in these series of studies is
formatted in ROOT and contains records for 64 calorimeter channels
(in case of the EMCal prototype), where each record contains
digitized waveform with 32 points each.

These data can be easily read by Python applications as well,
using the [uproot](https://uproot.readthedocs.io/){:target="_blank"} package.
