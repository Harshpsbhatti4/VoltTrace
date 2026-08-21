# VoltTrace Hardware Design & Pinout Specifications

This directory contains the electrical interface details, pin connections, safety isolation design, and hardware setup instructions for the **VoltTrace Edge-AI Smart Plug Platform**.

---

## Hardware Architecture Overview

VoltTrace interfaces directly with mains AC voltage ($230\text{V RMS}, 50\text{Hz}$) to sample analog voltage and current signals safely using galvanic isolation.

```text
       +-------------------------------------------------------------+
       |                     AC MAINS (230V / 50Hz)                  |
       +------------------------------+------------------------------+
                                      |
                      +---------------+---------------+
                      |                               |
              [ ZMPT101B Voltage ]            [ SCT-013 Current ]
              [   Transformer    ]            [   Transformer   ]
                      |                               |
                      +---------------+---------------+
                                      |
                              (Analog Conditioning)
                                      |
                       +--------------+--------------+
                       |   Arduino UNO Q Board       |
                       |  - Pin A2: Voltage Signal   |
                       |  - Pin A1: Current Signal   |
                       |  - Pin D7: Relay Control    |
                       +--------------+--------------+
                                      |
                              [ 5V Relay Switch ]
                                      |
                           [ Universal AC Socket ]
