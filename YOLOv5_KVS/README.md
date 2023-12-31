<h1>Deploying YOLOv5 on AWS and edge device for real time object detection</h1>

<p>This document showcases objection detection using open source pre-trained models such as YOLO on video streams from a standard camera and processor/laptop setup</p>

<h2>Solution Architecture</h2>

![solution_architecture](https://github.com/Seanyap90/MLdeploy/assets/34641712/6e921a19-e372-49f1-aadc-a5572621d706)

<p>In summary, this solution enables objection detection on captured frames from a video stream on Kinesis Video Streams.  As long as a device is able to be installed with a camera and Amazon Kinesis Video Streams Producer SDK for C/C++ library, its video stream can be used on KVS.</p>

<h4>Hardware Requirements</h4>
<p>1. Any web cam</p>
<p>2. Interfacing hardware such as edge gateway</p>

<h4>End Result</h4>

![inferenceresult](https://github.com/Seanyap90/MLdeploy/assets/34641712/4b0590f9-4ca2-40cc-a435-bfdc18dc9fe9)

<h2>Setting up Kinesis Video Streams</h2>

<p>In this case, we will be using a linux based gateway and a webcam.  The setup is done in 2 parts: on the console and the configuration of the gateway itself</p>

<h4>1. On Management Console</h4>

<p>An IoT thing on AWS IoT Core and a video stream on KVS need to be created.  Please follow the following references</p>
<p>References:</p>
<p> - https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/how-iot.html</p>
<p> - Kinesis Video Streams (KVS) RTSP Stream Part 1 - Ingestion from RTSP cameras (Tutorial): https://www.youtube.com/watch?v=YoOYTCD_v3Q</p>

<h4>2. Device Configuration</h4>

<p>Firstly please following the following instructions in this library: https://github.com/awslabs/amazon-kinesis-video-streams-producer-sdk-cpp. 
 You would need to install gstreamer and V4L2 on your gateway device.</p>

<p>Once set up, run the following command:</p>

````
gst-launch-1.0 v4l2src do-timestamp=TRUE device=/path/to/your/video/devices ! videoconvert ! video/x-raw,format=I420,width=640,height=480,framerate=30/1 ! x264enc  bframes=0 key-int-max=5 bitrate=500 ! video/x-h264,stream-format=avc,alignment=au,profile=baseline ! kvssink stream-name="your_cam_stream_kvs" storage-size=512 access-key="***" secret-key="****" aws-region="your-aws-region"
````


<h2>Create inference endpoint via Sagemaker</h2>

<p>Open a notebook instance on Sagemaker and run ObjD.ipynb to create an inference endpoint</p>

<h2>Inference code (App.py) and corresponding docker image</h2>

<p>Create the Dockerfile while putting app.py and requirements.txt in the home directory your gateway (or local device).</p>
<p>Then go to the management console and access Amazon ECR.  Create a private repository on ECR and follow the instructions to push the docker image from gateway to ECR.</p>

<h2>Create lambda function</h2>

<p>Access AWS Lambda through the console and create a lmabda function out of the image created in Amazon ECR by selecting the container image option</p>

<p>Once the function is created, please configure accordingly: </p>

![lambda_config](https://github.com/Seanyap90/MLdeploy/assets/34641712/4396b0bf-33d8-485d-8c7a-22d8e3b534f9)

<p>and test the inference!</p>
<h2>Expanding this project</h2>

<h4>Working with other AWS services for typical processes</h4>

<h4>Scaling</h4>

<h4>For edge applications</h4>
