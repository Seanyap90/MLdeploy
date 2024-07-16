<h1>ML powered Condition Monitoring Dashboard </h1>

<h2>Summary</h2>
<p>This project is about converting machine learning projects done on Kaggle or jupyter notebook to realistic implementations of machine learning on actual applications such as condition monitoring.  I found the following notebook that worked on datasets, with sources coming from actual industrial assets in operation such as the following:
https://www.kaggle.com/datasets/anikannal/solar-power-generation-data into a full application.</p>

<h2>Idea</h2>
<p>The idea is to create a conceptual application has the following: </p>

- An actual user interface, that is not about monitoring about model performance, but one that people will be viewing.  For this case, we could think of visualizing solar panel related data for supervisors to view in real time and make data driven maintenance decisions to ensure operational consistency
- ML deployment
- Basic monitoring of model performance to ensure that the deployed model is working optimally while future models can be trained

<p>We are using the following notebook that did some work on the solar power generation data:
  https://www.kaggle.com/code/paule404/eda-condition-monitoring-solar-power-plant
</p>

<p>This notebook deployed both threshold/rule based logic, linear and non linearregression to detect faults or failures of the inverters belonging to a solar panel.  The training of the regression models led to the use of residuals to determine faults, hence it led to my hypothesis that this allows granularity in condition monitoring or more importantly, proactive fault detection.  Beyond hard thresholds for fault detection, other levels of alerts can be created to signify potential action for early intervention that could be crucial to maintain operational consistency.

We will be deploying the logic as well as the model to do inference on real time data.  The real time data will be simulated with data provided by the dataset. </p>

<h2>Demonstration</h2>
<p>Please review the following videos to understand how ML is powering the alerting feature of this dashboard that monitors solar panel inverters</p>

<h3>Version 1: Condition monitoring by setting hard thresholds</h3>

https://github.com/Seanyap90/MLdeploy/assets/34641712/23a06b8f-23cb-46d9-ae25-6391f9f9fd18


<h3>Version 2: Condition monitoring with Linear Regression</h3>

https://github.com/Seanyap90/MLdeploy/assets/34641712/1c6db1d8-919c-48db-a9cd-79e16f39b599


<p>For version 1, a hard threshold, which is detection of zero DC power generation in daytime, is deployed to generate fault alerts.  In version 2, the linear regression model deployed created fault alerts for zero DC power generation and attention alerts for potentially failing inverters </p>

<h3>Version 2.1: Non linear regression vs threshold for potential fault detection due to high temperature of solar panel</h3>



https://github.com/Seanyap90/MLdeploy/assets/34641712/3ef53d81-715d-4596-8860-09e1c267b0f5




<h2>ML Deployment Design Overview</h2>

![ML inference system design](https://github.com/Seanyap90/MLdeploy/assets/34641712/10339341-1318-4eb5-aac2-a0fba4391556)


<p>We have the following: </p>

- The condition monitoring dashboard is a single page react js application
- We have a nodejs server to pass real time data to both the application and the inference server.  While real time data is flowing to the dashboard, the server is passing inference to the application after inference is done.
- The usage of endpoints to communicate with the inference server
- Usage of strategy pattern to design deployment infrastructure for ML inference.

<h2>Frontend Overview</h2>

![Front end condition monitoring UI](https://github.com/Seanyap90/MLdeploy/assets/34641712/9b62e1b9-a857-49d3-85f0-b998164c78ae)


