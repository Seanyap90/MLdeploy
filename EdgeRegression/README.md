<h1>ML inference for sensor data from edge devices</h1>

<p>An extension of https://github.com/Seanyap90/MLpowerplanteg, this solution showcases simple machine learning inferences of incoming sensor data or relevant PLC data to predict, in this case, power output.  Relative humidity and temperature can be measured by temperature and humidity sensors while pressure can be measured via flowmeters etc.</p>

<h2>Solution Architecture</h2>

![ModeldeploymentonGreengrassdevice](https://github.com/Seanyap90/MLdeploy/assets/34641712/a18aa67f-29a1-478d-b77e-0c2a9a6605bb)

<p>For this example, a virtual gateway was created while hypothetical data (via running gendata.py) was generated to simulate temperature, relative humidity and pressure readings.  But this solution can be used with edge gateways, raspberry pis etc while being connected to different sensors.  You will need to have docker installed too.</p>

<h2>ML Model Creation</h2>

<p>Run powerplant.ipynb to generate the regression model in joblib format.  This notebook can be run on any jupyter runtime or you can adjust the code to run in any Python runtime.</p>

<h2>Docker image for ECR</h2>

<p>On your virtual device/edge gateway, create a directory with a sub directory called model.  Subsequently put Dockerfile, inference.py and the packaged model, now in joblib format, in the following manner:</p>

````
|--docker_model
|  |--inference.py
|  |--Dockerfile
|  |--model
|     |--model.joblib
````
Log on to your AWS Management Console and create new repository in Amazon ECR and follow instructions to create the docker image on the virtual gateway/edge gateway and push to ECR.

<h2>AWS Greengrass</h2>

<h4>On AWS Management section</h4>

<p>1. Create new core device</p>
<p>Follow the instructions when accessing the AWS Greengrass section to create a new core device.  The core device will be the virutal/edge gateway.  The gateway also has to be accessed at the same time as there are instructions to download and run the greengrass installer</p>

<p>2. Create component</p>
<p>On AWS Greengrass section of the console, go to "Components" under Greengrass device.  While creating the component, you can copy the contents from AWSSG_component_receipe and paste in onto JSON input section in the "Create component page".  Finalize the creation of the component and subsequently deploy onto the core device.</p>

<h4>On virtual/edge gateway</h4>

<p>Please make sure that you give ggc_user permissions to run docker containers on your device</p>

````
sudo usermod -aG docker ggc_user
````
<p>Constantly access the logs on /greengrass folder to troubleshoot if failure of deployment arises.</p>
<p>If you are running a virtual gateway, please run gendata.py on the background.  This code has to be executed outside Docker environment</p>
