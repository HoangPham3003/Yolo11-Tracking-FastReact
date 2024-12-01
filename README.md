# Stream CARS TRACKING using FastAPI and ReactJS

![demo](https://github.com/user-attachments/assets/a88137cb-38be-46cf-b422-6e70c5a39452)

!!! Note*: FPS can be extremely low because object recognizer is run on CPU (not GPU). 

## Requirements
- Docker
- Docker-compose

## What can be learned from this repo?
<ul>
<li>
  Object recognition:
  <ul>
    <li>Yolo 11</li>
    <li>Onnx</li>
  </ul>
</li>
<li>
  Object tracking:
  <ul>
    <li>Deep SORT</li>
  </ul>
</li>
<li>
  Streaming data:
  <ul>
    <li>FastAPI</li>
    <li>ReactJS</li>
  </ul>
</li>
<li>
  Deploy:
  <ul>
    <li>Docker</li>
    <li>Ngrok</li>
  </ul>
</li>
</ul>

## How to run

First, clone the repository.
```bash
git clone https://github.com/HoangPham3003/Yolo11-Tracking-FastReact.git
cd Yolo11-Tracking-FastReact
```
Second, in [docker-compose](https://github.com/HoangPham3003/Yolo11-Tracking-FastReact/blob/main/docker-compose.yml) file, replace this field by your Ngrok AUTHENTOKEN

```bash
NGROK_AUTHTOKEN=[NGROK AUTHTOKEN]
```
Finally, run 2 shell script file. Note that it should open a endpoint gate in ngrok after run the first shell script file [run_ngrok](https://github.com/HoangPham3003/Yolo11-Tracking-FastReact/blob/main/run_ngrok.sh). I can be found in dashboard of Ngrok.

```bash
sh run_ngrok.sh
sh run_docker.sh
```
