<h1> Bearing Condition Predictor </h1>

<h2>Introduction</h2>
Based on Predicting Bearings’ Degradation Stages for Predictive Maintenance in the Pharmaceutical Industry (2022) by Dovile Juodelyte, Veronika Cheplygina, Therese Graversen, Philippe Bonnet, we create a conceptual condition monitoring/predictive maintenance app to integrate their deep learing models for real time inference to predict state of degradation.  Also, the backend of this app will also schedule adding into feature pipelines and model training.  Hence this end-to-end system will be built based on the 3-pipeline methodology which includes the use of feature stores and ready made 3rd party model registry.  On the fronte end single page app with a monitoring dashboard that processes accelerometer data, displays the level of degradation as well as alerting a user of the seriousness of current condition of the monitored bearings.  The dataset used is from the FEMTO dataset.

<h3>Summary of Paper</h3>
The research paper, Predicting Bearings’ Degradation Stages for Predictive Maintenance in the Pharmaceutical Industry (2022), propsed a two step solution for a robust deep learning model:
- Data labelling is automated using a k-means bearing lifetime segmentation method, which is based on high-frequency bearing vibration signal embedded in a latent low-dimensional subspace 
- The a supervised classifier is built based on a multi-input neural network for bearing degradation stage detection

To illustrate:
![image](https://github.com/user-attachments/assets/af1b9f52-608f-4dfe-8e77-2be4e8de90ea)

From the raw accelerometer data in the FEMTO dataset, the signals are downsampled by half from 25600Hz to 12800Hz to reduce data dimensionality.  After converting to the frequency domain, frequencies up to 6,400 Hz are obtained, where bearing degradation signs are expected. The downsampled signal in the frequency domain has 641 features. Both vertical and horizontal vibration signals were transformed to the frequency domain.  Both vertical and horizontal vibration signals were transformed to the frequency domain.  To get time domain features, 

<h3> Summary of this project </h3>

<h2> Demonstration </h2>

<h3> Overall </h3>


<h2> System Design </h2>

