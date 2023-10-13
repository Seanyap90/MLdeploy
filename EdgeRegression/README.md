<h1>ML inference for sensor data from edge devices</h1>

<p>An extension of https://github.com/Seanyap90/MLpowerplanteg, this solution showcases simple machine learning inferences of incoming sensor data or relevant PLC data to predict, in this case, power output.  Relative humidity and temperature can be measured by temperature and humidity sensors while pressure can be measured via flowmeters etc.</p>

<h2>Solution Architecture</h2>

![ModeldeploymentonGreengrassdevice](https://github.com/Seanyap90/MLdeploy/assets/34641712/a18aa67f-29a1-478d-b77e-0c2a9a6605bb)

<p>For this example, a virtual gateway was created while hypothetical data was generated to simulate temperature, relative humidity and pressure readings.  But this solution can be used with edge gateways, raspberry pis etc while being connected to different sensors.</p>

<h2>ML Model Creation</h2>

<p>Run powerplant.ipynb to generate the regression model in joblib format</p>

<h2>Docker image for ECR</h2>

<p>On your virtual device/edge gateway, create a directory with a sub directory called model</p>

<h2>AWS Greengrass</h2>

<p>On Edge device</p>

<p>On Greengrass Console</p>
