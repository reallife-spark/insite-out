---
title: nvidia-forums-hw-engines
source_url: https://forums.developer.nvidia.com/t/how-to-enable-activate-hardware-engines-like-pva-dla-nenvc-on-nvidia-jetson-xavier-nx/248856
fetched_at: 2026-11-26T08:23:37+00:00
engine: defuddle
defuddle_version: 0.19.13
content_sha256: eadeb63bf9261b722f189811d73507af555d5ea823c405820487da5af245293b
status: captured
depth: 1
root_source: https://share.google/aimode/mhgoDgYotEKcIHMGo
---

## How to enable / activate Hardware engines like PVA, DLA, NENVC on Nvidia Jetson Xavier NX?

[Robotics & Edge Computing](https://forums.developer.nvidia.com/c/robotics-edge-computing/55) [Jetson Systems](https://forums.developer.nvidia.com/c/robotics-edge-computing/jetson-systems/70) [Jetson Xavier NX](https://forums.developer.nvidia.com/c/robotics-edge-computing/jetson-systems/jetson-xavier-nx/258)

When I’m checking the Hardware engines in Xavier NX (using jtop), it’s showing all are turned off. How do I enable the hardware engine PVA? Kindly support.

[![xavier\_hw\_engines](https://global.discourse-cdn.com/nvidia/optimized/3X/3/6/362f0f312a329fd34ed5638c487d6770b1665f6e_2_690x457.png)](https://global.discourse-cdn.com/nvidia/original/3X/3/6/362f0f312a329fd34ed5638c487d6770b1665f6e.png "xavier_hw_engines")

Hi, please confirm whether these hardware engines are available in Jetson Xavier NX? If yes, how can we enable it?

Hi [@rahul7manu](https://forums.developer.nvidia.com/u/rahul7manu), yes these engines are all available on Xavier NX - I think jtop is showing if they are actively in use. So when you run an application that uses them, they should not show as OFF anymore - [@Raffaello](https://forums.developer.nvidia.com/u/raffaello) can confirm.

Hi Dusty,

Thank you for your reply [@dusty\_nv](https://forums.developer.nvidia.com/u/dusty_nv), It’s exactly such you wrote.  
jtop detects the engine running reading from:

> /sys/kernel/debug/clk/<ENGINE\_NAME>/clk\_enable\_count

Hi [@Raffaello](https://forums.developer.nvidia.com/u/raffaello), [@dusty\_nv](https://forums.developer.nvidia.com/u/dusty_nv),  
Thanks for confirmation. Could you please help me with some sample resource to check pva, nvenc, dla, etc… How can I enable them as well?

I tried running perspective warp example from vpi. Attaching the screenshots before running and while running the code.

Initial state…

[![Screenshot from 2023-04-05 19-56-19](https://global.discourse-cdn.com/nvidia/optimized/3X/c/d/cdcacfcabf79f2d67b753ee608f38f9c90b10266_2_690x388.png)](https://global.discourse-cdn.com/nvidia/original/3X/c/d/cdcacfcabf79f2d67b753ee608f38f9c90b10266.png "Screenshot from 2023-04-05 19-56-19")

While VIC code is running…

[![Screenshot from 2023-04-05 19-59-10](https://global.discourse-cdn.com/nvidia/optimized/3X/5/d/5d0eb9879c3b4effdc112b000ca3a8c9db9e1562_2_690x388.png)](https://global.discourse-cdn.com/nvidia/original/3X/5/d/5d0eb9879c3b4effdc112b000ca3a8c9db9e1562.png "Screenshot from 2023-04-05 19-59-10")

They are already enabled, you just need to run something that uses them so they are active. For example, TensorRT can use DLA, certain VPI algorithms use PVA, a GStreamer pipeline can use the encoder, ect.

Hi [@dusty\_nv](https://forums.developer.nvidia.com/u/dusty_nv), Thanks. Understand that.

I’m trying to run rescale, undistort and warping.  
These I’m unable to run in backend PVA.

Appreciate if you could point me to a resource (sample code) that uses the backend PVA.

![image](https://global.discourse-cdn.com/nvidia/original/3X/5/d/5d6cb727282172dd1450e27372975d5de7f70555.png)

You may want to open a new topic specifically about those PVA functions, but I’d check the VPI samples and see which could be run on PVA: [https://docs.nvidia.com/vpi/samples.html](https://docs.nvidia.com/vpi/samples.html)

Thanks [@dusty\_nv](https://forums.developer.nvidia.com/u/dusty_nv). Found pva in convolve2d. Let me check that.

I’ve tried 01-convolve\_2d example.  
Before running the code

[![Screenshot from 2023-04-07 12-01-09](https://global.discourse-cdn.com/nvidia/optimized/3X/b/6/b615072d1f6f8a5b5b9cf844f0f26776e15e74c5_2_690x388.png)](https://global.discourse-cdn.com/nvidia/original/3X/b/6/b615072d1f6f8a5b5b9cf844f0f26776e15e74c5.png "Screenshot from 2023-04-07 12-01-09")

While running the pva code

[![Screenshot from 2023-04-07 12-01-14](https://global.discourse-cdn.com/nvidia/optimized/3X/7/2/7288fee35cf178fc244f2d44d42e192a148168cf_2_690x388.png)](https://global.discourse-cdn.com/nvidia/original/3X/7/2/7288fee35cf178fc244f2d44d42e192a148168cf.png "Screenshot from 2023-04-07 12-01-14")

However, I still don’t see pva engine getting active in jtop. Only vic is running which runs while using vic backend as well.  
Carrying out these experiments for a time critical project pipeline that I’m building. I want to use the best backend for the operation.  
So, I need to know whether is there something additional I need to do to make them active; like do I need to reflash the jetpack or do something else?

Hi, Kindly respond why it isn’t showing PVA active, when I’m running PVA code?

[@rahul7manu](https://forums.developer.nvidia.com/u/rahul7manu) I would think it’s more likely that jtop isn’t detecting PVA as active than it is that PVA isn’t actually being used by VPI (which would throw an error). For more in-depth profiling, you can use the NSight tools. Also, [@Raffaello](https://forums.developer.nvidia.com/u/raffaello) can you share how you tested the PVA in jtop?

Also check out the DLA github page for samples and resources: [Recipes and tools for running deep learning workloads on NVIDIA DLA cores for inference applications.](https://github.com/NVIDIA/Deep-Learning-Accelerator-SW/)

We have a FAQ page that addresses some common questions that we see developers run into: [Deep-Learning-Accelerator-SW/FAQ](https://github.com/NVIDIA/Deep-Learning-Accelerator-SW/tree/main/FAQ)

Thank you [@ramc](https://forums.developer.nvidia.com/u/ramc). I’ll take a look at these also for understanding of other jetson modules other than PVA.

[@dusty\_nv](https://forums.developer.nvidia.com/u/dusty_nv), I guess, we still don’t have a clue about it why it doesn’t gets enabled. Probably, if it’s same for others too; I think this needs to be experimented / tested and confirmed.

However, I’m going ahead with CUDA backend for my tasks. This query can be considered as closed. In case, if you get any update on PVA, please do inform me. Thanks.
