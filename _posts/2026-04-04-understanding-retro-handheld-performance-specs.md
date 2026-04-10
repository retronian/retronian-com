---
layout: post
title: "How to Read Retro Handheld Performance Specs"
date: 2026-04-04
description: "A quick guide to making sense of confusing retro handheld spec sheets like 'Allwinner H700 Quad-core ARM Cortex-A53 1.5GHz'."
tags: [hardware, performance, guide]
---

"Allwinner H700 Quad-core ARM Cortex-A53 1.5GHz", "SigmaStar SSD202D Dual-core ARM Cortex-A7 1.2GHz" — the specs of retro handheld game consoles are confusing, aren't they? Let me try to explain what they mean.

## Manufacturer, SoC, CPU Core

Take "Allwinner H700 Quad-core ARM Cortex-A53 1.5GHz" as an example. It breaks down like this:

- **Allwinner** — manufacturer
- **H700** — SoC
- **Quad-core** — number of CPU cores
- **ARM Cortex-A53** — CPU core
- **1.5GHz** — clock speed

## Manufacturer

Simply the company that makes the chip.

Major manufacturers:

- **Allwinner**: Cheap. Frequently used in the Anbernic XX series.
- **Rockchip**: The standard choice for mid-range and higher.
- **UNISOC**: Relatively new, high-performance.
- **MediaTek**: Smartphone class.
- **SigmaStar**: Ultra low power. Used in the Miyoo Mini family.

## SoC (System on a Chip)

A single chip that combines the CPU, GPU, memory controller, power management, and so on.

Major SoCs and the devices they're in:

- **H700**: RG35XX series
- **A33**: Miyoo A30
- **RK3326**: RG351 / RGB20S
- **RK3566**: RG353 / RGB30
- **RK3399**: RG552
- **T820**: RG556 and others
- **SSD202D**: Miyoo Mini

## Number of CPU Cores

Literally the number of cores.

- Dual-core: 2
- Quad-core: 4
- Octa-core: 8

## CPU Core

This lives inside the SoC. These are almost all designs from ARM.

Major CPU cores (higher numbers are stronger):

- Cortex-A7
- Cortex-A35
- Cortex-A53
- Cortex-A55
- Cortex-A72
- Cortex-A76

## Clock Speed

How fast the CPU runs. Basically, retro handhelds with the same CPU core tend to have the same clock speed, but apparently manufacturers sometimes overclock it through their settings, or intentionally lower it for better power efficiency.

## So What Should You Actually Look At?

As long as the SoC is the same, the other pieces are basically fixed. So if you know "this device uses the H700" or "it has an SSD202D", you already know most of what there is to know about its performance.

Snapdragon, which shows up often in Android-based devices, has its own separate flavor of complexity — I'll save that for another time.

## Bonus: What's the Difference Between an SoC (System on a Chip) and an SBC (Single Board Computer)?

An SoC is where the main functions are packed into a single chip. An SBC is where all the various things a computer needs (including the chips) are arranged on a single board.
