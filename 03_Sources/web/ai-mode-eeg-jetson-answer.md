---
title: Google AI Mode answer — Jetson HW engines, DLA, DeepStream and Neurosity Crown EEG
source_url: https://share.google/aimode/mhgoDgYotEKcIHMGo
fetched_at: 2026-11-26
engine: manual-paste
capture_method: "User pasted the rendered answer; direct defuddle/curl/headless-browser access returned Google's CAPTCHA page"
content_sha256: 71399a9e6d15f27253908d63cace705c64c58743ac5b194d5d361de8f4a28bc3
status: captured
depth: 0
note: "Two near-identical passes were pasted. This file keeps the second, complete pass, which includes the full HW-engine list."
---

# AI Mode

The image shows the [HW engines] section from jtop (jetson_stats) on an NVIDIA Jetson system, listing hardware accelerators that are all currently [OFF] (idle):

- GitHub +1 — APE: Audio Processing Engine (handles audio tasks).
- NVIDIA Developer Forums +3 — CVNAS: Computer Vision / Navigation Accelerator Subsystem.
- NVIDIA Developer Forums +1 — DLA0c / DLA1c: Deep Learning Accelerator cores 0 and 1 (offload deep learning inference). NVENC: NVIDIA Hardware Video Encoder. NVDEC: NVIDIA Hardware Video Decoder. NVJPG: NVIDIA Hardware JPEG Encoder/Decoder. PVA0a: Programmable Vision Accelerator 0 (computer vision workloads). SE: Security Engine (cryptographic operations). VIC: Video Image Compositor (2D image scaling, color space conversion, and composition).
- NVIDIA Developer Forums +3 — When active, jtop replaces [OFF] with the engine's current operating frequency (such as 150MHz or 1.6GHz).
- NVIDIA Developer Forums +1 — If you tell me what workload you are running (such as video encoding, JPEG decoding, or TensorRT/DLA inference), I can help you check whether those hardware engines are being used or troubleshoot why they stay off.

TensorRT runs on the GPU by default, which is why DLA0c and DLA1c stay [OFF] unless you explicitly assign layers to the Deep Learning Accelerators. To offload TensorRT inference to the DLA cores and free up GPU resources:

1. Enable DLA in trtexec (Command Line): `trtexec --onnx=model.onnx --useDLACore=0 --allowGPUFallback --fp16`. `--useDLACore=0` (or 1) targets DLA0c or DLA1c; `--allowGPUFallback` lets unsupported operations run on the GPU; `--fp16` (or `--int8`) is required because DLA supports only FP16 and INT8, not FP32.
2. Enable DLA in Python / C++ API via `IBuilderConfig`: `config.default_device_type = trt.DeviceType.DLA`, `config.DLA_core = 0`, `config.set_flag(trt.BuilderFlag.FP16)`, `config.set_flag(trt.BuilderFlag.GPU_FALLBACK)`.
3. Verify usage in jtop: during inference DLA0c/DLA1c switch from [OFF] to an active clock (e.g. 1.4GHz). DLA stays [OFF] while the engine is compiled; it turns on only at inference execution. On Jetson Orin Nano jtop still displays DLA rows although the silicon lacks physical DLA cores.

In DeepStream, enable DLA by setting `enable-dla=1` and `use-dla-core=0` (or 1) in the `nvinfer` config, with `network-mode=2` (FP16) or `1` (INT8). `network-mode=0` (FP32) makes DeepStream ignore DLA or fail engine generation. Delete any existing `.engine` file so DeepStream regenerates it; GPU fallback is enabled automatically by nvinfer. `use-dla-core` can split a primary detector on core 0 from a secondary classifier on core 1.

| jtop engine | DeepStream plugin | Role in pipeline |
| --- | --- | --- |
| NVDEC | nvv4l2decoder / uridecodebin | Hardware-decodes H.264/H.265 RTSP or MP4 streams |
| VIC | nvstreammux / nvvideoconvert | Resizes, converts color formats (NV12/RGBA), batches streams |
| DLA0c / DLA1c | nvinfer | Neural inference when enable-dla=1 |
| NVENC | nvv4l2h264enc / nvv4l2h265enc | Hardware-encodes output video to file or RTSP |

Orin Nano lacks hardware NVENC and DLA cores, so nvinfer uses the GPU and encoding falls back to software x264enc.

Both the 32GB and 64GB AGX Xavier modules have two full NVDLA v1 engines (DLA0c, DLA1c) plus NVDEC, NVENC, VIC, PVA and NVJPG. Heavy multi-stream DeepStream pipelines can keep the GPU free for custom CUDA kernels. Workloads can be split across GPU and both DLA cores in one pipeline: dual-DLA load balancing, hybrid GPU primary detector plus DLA secondary classifiers/trackers, and INT8 calibration (roughly doubles DLA throughput versus FP16).

Sample `config_infer_dla0.txt`:

```ini
[property]
gpu-id=0
net-scale-factor=0.0039215697906911373
onnx-file=model.onnx
model-engine-file=model_b4_dla0_fp16.engine
batch-size=4
network-mode=2
enable-dla=1
use-dla-core=0
scaling-compute-hw=1
```

`scaling-compute-hw=1` forces DeepStream's internal resizer onto the VIC engine. Quick pipeline test: edit `config_infer_primary.txt` with `enable-dla=1`, `use-dla-core=0`, `network-mode=2`, then run `deepstream-app -c source4_1080p_dec_infer-resnet_tracker_sgie_tiled_display_int8.txt` from `/opt/nvidia/deepstream/deepstream/samples/configs/deepstream-app/`; jtop should show NVDEC, VIC, DLA0c and NVENC active.

Yes, you can stream real-time data from a Neurosity Crown directly to a Jetson AGX Xavier using the official Python SDK, JavaScript SDK, or local protocols like Lab Streaming Layer (LSL) and Open Sound Control (OSC). DeepStream is built for video/audio media (NVDEC/NVENC); Crown EEG data can be bridged into a Jetson pipeline for custom TensorRT/DLA models or to trigger DeepStream actions based on mental state.

What the Crown streams:

- Raw EEG: 8 channels (CP3, C3, F5, PO3, PO4, F6, C4, CP4) at 256 Hz.
- Frequency bands: PSD / FFT across Delta, Theta, Alpha, Beta, Gamma.
- Cognitive metrics: real-time Focus and Calm probability scores on the Crown's N3 chip.
- Kinesis: trained motor-imagery triggers (e.g. imagined left-hand pinch).
- Telemetry: accelerometer, battery, per-sensor signal quality.

Option A — Neurosity Python SDK: `pip install neurosity`, then `neurosity.brainwaves_raw(callback)` for 8-channel epochs (16 samples every ~62.5ms) or `neurosity.focus(callback)` for probability. Option B — LSL or OSC from the Neurosity Developer Console, using `pylsl` or `python-osc` on the local Wi-Fi without cloud routing.

Because EEG is a 1D time series (8 channels × time steps) rather than video frames, the cleanest architecture is a custom 1D-CNN or EEGNet in PyTorch exported to ONNX and compiled with `trtexec --useDLACore=0`, with a Python EEG listener beside DeepStream using `pyds` or an MQTT/Kafka broker (`nvmsgbroker`) to switch feeds, toggle recording or overlay Focus/Calm on `nvdsosd`.

Full pipeline across both Xaviers:

- 32GB (Edge/Inference Node): connects to Crown via local LSL/Wi-Fi, runs EEG inference on DLA0c, publishes state/triggers over ZeroMQ/MQTT.
- 64GB (Heavy Vision + Fusion Node): runs multi-stream DeepStream (NVDEC + VIC + DLA0c/DLA1c + NVENC), receives EEG/Focus state, fuses into the video pipeline.

Setup on both boards: matching JetPack 5.1.x / L4T R35.x, DeepStream 6.3, TensorRT 8.5; `cat /etc/nv_tegra_release`; `sudo nvpmodel -m 0` and `sudo jetson_clocks`; `sudo usermod -aG video,render $USER`; apt install `nvidia-jetpack deepstream-6.3 python3-pip python3-gi python3-gst-1.0 ...`; `pip3 install pyds-1.1.8-py3-none-linux_aarch64.whl`. Engine files built on one board run on the other only with identical JetPack/TensorRT versions.

Neurosity Console: same 5GHz Wi-Fi/LAN subnet, enable LSL and optionally OSC, note Device ID, assign static IPs. Build `liblsl` from source for ARM64 (`cmake .. -DLSL_BUILD_STATIC=OFF`, `make -j$(nproc)`, `sudo make install`, `sudo ldconfig`), then `pip3 install neurosity pylsl pyzmq paho-mqtt scipy numpy`.

Inter-Xavier communication: 32GB publisher reads `pylsl` stream type `EEG`, runs the TensorRT DLA model, publishes JSON such as `{"focus": 0.82, "command": "left"}` over ZeroMQ PUB on port 5555 or MQTT. 64GB subscriber runs a background thread in DeepStream and updates `NvDsDisplayMeta` in an `nvdsosd` sink pad probe.

Verification checklist:

1. Crown LSL stream: `python3 -c "from pylsl import resolve_streams; print(resolve_streams())"`.
2. DLA compilation: `trtexec --onnx=eeg_model.onnx --saveEngine=eeg_dla0.engine --useDLACore=0 --allowGPUFallback --fp16`.
3. DeepStream hardware engines: jtop shows NVDEC, VIC, DLA0c/DLA1c, NVENC at active frequencies.
4. Cross-Xavier sync: `ping <64GB_IP>` — < 1 ms wired Ethernet or < 5 ms 5GHz Wi-Fi.

AI responses may include mistakes. Learn more.
