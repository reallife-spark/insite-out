---
title: nvidia-forums-nvpmodel
source_url: https://forums.developer.nvidia.com/t/how-to-use-nvpmodel-to-power-down-unused-functional-units/214759
fetched_at: 2026-11-26T08:23:37+00:00
engine: defuddle
defuddle_version: 0.19.13
content_sha256: 409eadde30d44d5e83e9fb78336cd92016b7ee299ec69dfe747faaf6267ba03a
status: captured
depth: 1
root_source: https://share.google/aimode/mhgoDgYotEKcIHMGo
---

[Robotics & Edge Computing](https://forums.developer.nvidia.com/c/robotics-edge-computing/55) [Jetson Systems](https://forums.developer.nvidia.com/c/robotics-edge-computing/jetson-systems/70) [Jetson AGX Orin](https://forums.developer.nvidia.com/c/robotics-edge-computing/jetson-systems/jetson-agx-orin/486)

I have an AGX Orin application where I would like to maximize GPU compute performance. Essentially, I want to do the following:

- Force the external memory interface to 3200 MHz
- Enable all GPU TPCs
- Force the GPU clock to the maximum

I’m not sure how much CPU will be required, so that’s still up in the air. For now, I want to keep it at max performance as well, then scale it down as we determine what’s needed for the application.

At the same time, I want to minimize power usage to the greatest extent possible for thermal reasons. There are several other functional units that I would like to power down/disable/frequency scale as low as possible, because they will not be used at all. Ones that I’m aware of include:

- DLA
- PVA
- VIC
- NVDEC
- NVENC
- NVJPG

The power management documentation that I’ve found implies that nvpmodel could potentially be used to do this, but I don’t see it spelled out anywhere how I could create a custom profile that would turn these things off. Is there any documentation that describes more clearly how one would create a custom power profile?

Please refer to [Jetson Orin NX Series and Jetson AGX Orin Series — Jetson Linux  
Developer Guide 34.1 documentation (nvidia.com)](https://docs.nvidia.com/jetson/archives/r34.1/DeveloperGuide/text/SD/PlatformPowerAndPerformance/JetsonOrinNxSeriesAndJetsonAgxOrinSeries.html)

That’s the documentation that I was referring to. I couldn’t find anything in there that specifically indicates how to create a custom model that disables DLA, PVA, etc.

There is a custom power mode definition, have you tried?

I have looked at that. It doesn’t seem to be well documented, but I can infer what’s going on by inspecting the configuration file.

My question is whether there is any documentation on the knobs for controlling the power to the DLA, PVA, etc. It appears that I can set maximum clock rates for the DLA cores, and PVA0\_VPS and PVA0\_AXI. What is the lowest power state I can set for these? Do I set the clock rate to zero? Is there some other knob? Are there other parameters that control the clocks for the other modules I’m not using like NVDEC, NVENC, and NVJPG?

Hi,  
VIC, NVENC, NVDEC, NVJPG are on demand, These engines are disabled if it is not in use.

For Xavier, PVA and DLA cannot be disabled and need to be run in minimum clocks. Is is mode 7 in the table:  
[Jetson Xavier NX Series and Jetson AGX Xavier Series — Jetson Linux\<br/>Developer Guide 34.1 documentation](https://docs.nvidia.com/jetson/archives/r34.1/DeveloperGuide/text/SD/PlatformPowerAndPerformance/JetsonXavierNxSeriesAndJetsonAgxXavierSeries.html#supported-modes-and-power-efficiency)

We will check and add a similar mode to Orin.

Thanks for the information. Is there a way to query what clock frequencies are allowed for DLA/PVA like you can for the external memory interface, GPU, etc.?

Hi,  
We have checked and confirmed if the engine is not in-use, it is power-gated. Please check the status:

```
root@tegra-ubuntu:/sys/kernel/debug/bpmp/debug/powergate# cat pva/state
0
root@tegra-ubuntu:/sys/kernel/debug/bpmp/debug/powergate# cat dlaa/state
0
root@tegra-ubuntu:/sys/kernel/debug/bpmp/debug/powergate# cat dlab/state
0
```

Perfect, thank you.
