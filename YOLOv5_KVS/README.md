<h1>Deploying YOLOv5 on AWS and edge device for real time object detection</h1>

<p>This document showcases objection detection using open source pre-trained models such as YOLO on video streams from a standard camera and processor/laptop setup</p>

<h2>Solution Architecture</h2>

![solution_architecture](https://github.com/Seanyap90/MLdeploy/assets/34641712/6e921a19-e372-49f1-aadc-a5572621d706)

<p>In summary, this solution enables objection detection on captured frames from a video stream on Kinesis Video Streams.  As long as a device is able to be installed with a camera and Amazon Kinesis Video Streams Producer SDK for C/C++ library, its video stream can be used on KVS.</p>

<h2>Setting up Kinesis Video Streams</h2>

<p>In this case, we will be using a linux based gateway and a webcam.  The setup is done in 2 parts: on the console and the configuration of the gateway itself</p>

<h4>1. On Management Console</h4>

<p>An IoT thing on AWS IoT Core and a video stream on KVS need to be created.  Please follow the following references</p>
<p>References:</p>
<p> - https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/how-iot.html</p>
<p> - Kinesis Video Streams (KVS) RTSP Stream Part 1 - Ingestion from RTSP cameras (Tutorial): https://www.youtube.com/watch?v=YoOYTCD_v3Q</p>

<h4>2. Device Configuration</h4>

<p>Firstly please following the following instructions in this library: https://github.com/awslabs/amazon-kinesis-video-streams-producer-sdk-cpp. 
 You would need to install gstreamer and V4L2 on your gateway device</p>

<h2>Create inference endpoint via Sagemaker</h2>

<p>Open a notebook instance on Sagemaker and run ObjD.ipynb to create an inference endpoint</p>

<h2>Inference code (App.py) and corresponding docker image</h2>

<p>Create the Dockerfile while putting app.py in the home directory your gateway (or local device).</p>
<p>Then go to the management console and access Amazon ECR.  Create a private repository on ECR and follow the instructions to push the docker image from gateway to ECR.</p>

<h2>Create lambda function</h2>

<h2>Expanding this project</h2>

