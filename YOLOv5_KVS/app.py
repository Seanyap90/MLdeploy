import numpy as np
import cv2
import json
import boto3, botocore
from PIL import Image
import io

class_names = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
        'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
        'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
        'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
        'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
        'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
        'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
        'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
        'hair drier', 'toothbrush'] 
2
def get_video_url():
    kvs = boto3.client(
            'kinesisvideo',
            aws_access_key_id='',
            aws_secret_access_key=''
    )

    STREAM_NAME = "camera_1"
    # Grab the endpoint from GetDataEndpoint
    endpoint = kvs.get_data_endpoint(
        APIName="GET_HLS_STREAMING_SESSION_URL",
        StreamName=STREAM_NAME
    )['DataEndpoint']

    kvam = boto3.client(
        "kinesis-video-archived-media", 
        aws_access_key_id='',
        aws_secret_access_key='',
        endpoint_url=endpoint)
    
    url = kvam.get_hls_streaming_session_url(
        StreamName=STREAM_NAME,
        PlaybackMode="LIVE"
    )['HLSStreamingSessionURL']

    return url

def prep_image(frame):
    prep_img = cv2.imread(frame)
    prep_img = cv2.cvtColor(prep_img, cv2.COLOR_BGR2RGB)
    height,width = prep_img.shape[0], prep_img.shape[1]

    top_pad = bot_pad = height % 640 // 2
    left_pad = right_pad = width % 640 // 2

    prep_img = cv2.copyMakeBorder(prep_img, top_pad, bot_pad, left_pad, right_pad, cv2.BORDER_CONSTANT, value=[114,114,114])
    prep_img = cv2.resize(prep_img,(640,640))

    return prep_img

def processed_img(result_img, or_img, arr):
    indices = np.where(np.array(result_img['predictions'][0]['output_1']) > 0.5)
    xywh = np.array(result_img['predictions'][0]['output_0'])[indices]
    xywh[:,0] *= 640
    xywh[:,1] *= 640
    xywh[:,2] *= 640
    xywh[:,3] *= 640
    xywh = xywh.astype(int)

    classes = np.array(result_img['predictions'][0]['output_2'])[indices]
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    FONTSCALE = .6
    WHITE = (255, 255, 255)
    THICKNESS = 2
    for idx, rect in enumerate(xywh):
        or_img = cv2.rectangle(or_img,
                (rect[0], rect[1]-5),
                (rect[2], rect[3]), thickness=2, color = (255,0,0))
        
        class_idx = int(classes[idx])
        or_img = cv2.putText(or_img, 
                        f'{arr[class_idx]}',
                        (rect[0], rect[1]),
                        FONT,
                        FONTSCALE,
                        WHITE,
                        THICKNESS)
    
    return or_img
    

def handler(event, context):
    
    stream_url = get_video_url()
    bucket_name = ''
    frame_key = '/tmp/captured-frame.jpg'
    pro_img_key = 'processed-frame.jpg'

    s3_client = boto3.client(
        's3',
        aws_access_key_id='',
        aws_secret_access_key=''
    )

    config = botocore.config.Config(read_timeout=500)
    runtime = boto3.client(
        'runtime.sagemaker', 
        aws_access_key_id='',
        aws_secret_access_key='',
        config=config)

    cap = cv2.VideoCapture(stream_url)
    
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return
    
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        return
    
    cap.release()

    cv2.imwrite(frame_key, frame)
    prepimg = prep_image(frame_key) 

    data = np.array(prepimg.astype(np.float16) / 255.)
    payload = json.dumps([data.tolist()])
    response = runtime.invoke_endpoint(EndpointName='yolov5l-demo', ContentType='application/json', Body=payload)
    result = json.loads(response['Body'].read().decode())

    pro_img = processed_img(result,prepimg,class_names)
    encode_img = cv2.imwrite(pro_img_key, pro_img)
    colored_img = Image.fromarray(pro_img).convert('RGB')
    out_img = io.BytesIO()
    colored_img.save(out_img, format='jpeg')
    out_img.seek(0)  

    try:
        response = s3_client.put_object(Bucket=bucket_name, Key=pro_img_key, Body=out_img)
        print("File saved to S3:", response)
        return {
            'statusCode': 200,
            'body': 'File saved to S3 successfully'
        }
    except Exception as e:
        print("Error:", e)
        return {
            'statusCode': 500,
            'body': 'Error saving file to S3'
        }

