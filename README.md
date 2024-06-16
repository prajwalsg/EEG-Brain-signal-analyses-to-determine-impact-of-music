# EEG-Brain-signal-analyses-to-determine-impact-of-music
Development of a model to analyse the impact of music on human health using brain signals. This model will explore the influence of three distinct musical genres on brain activity, furthering our understanding of music's influence on well-being

EEG Device used : MUSE Band 2
![image](https://github.com/prajwalsg/EEG-Brain-signal-analyses-to-determine-impact-of-music/assets/90396143/61b24648-0849-4a49-b7d9-dbd5095ea0ea)
Brain mapping
![image](https://github.com/prajwalsg/EEG-Brain-signal-analyses-to-determine-impact-of-music/assets/90396143/0336ea3b-84c2-4365-ae54-897f331855ae)

Before data acquisition, we ensured the proper placement and preparation of the Muse 2 band on the participant's head. The band was positioned in accordance with the manufacturer's guidelines, ensuring optimal contact with the forehead and earlobes. We took care to clean the electrode sensors and ensured a snug fit to minimize movement artifacts

# Calibration and Reference Signal
To establish a baseline for data analysis, we performed a calibration procedure. Participants were instructed to remain still and relax while the Muse 2 band recorded a reference signal. This step was essential to account for individual variations and establish a consistent starting point for subsequent brain signal measurements.

example of collected csv data :
![image](https://github.com/prajwalsg/EEG-Brain-signal-analyses-to-determine-impact-of-music/assets/90396143/eb293fa7-82d5-402e-a874-81ca644e1157)

# Data Sampling and Bandwidth:
During the EEG signal recording, the Muse 2 band sampled the brain signals at a predefined frequency, typically in the range of 256 to 500 Hz. The sampling rate was carefully selected to capture the desired frequency components while avoiding aliasing effects. The bandwidth of the recorded signals was typically limited to the range of 0.5 to 40 Hz, focusing on the frequency bands relevant to the study objectives, such as
alpha, beta, theta, and gamma 

![image](https://github.com/prajwalsg/EEG-Brain-signal-analyses-to-determine-impact-of-music/assets/90396143/1f4c90f6-ebc2-48e0-a424-0962eda61fcc)

# Accuracy and Variance:

●	Accuracy indicates the proportion of data points where the absolute difference exceeds the threshold, providing insight into the reliability of the comparison. Variance measures the average deviation between corresponding data points in the "Before" and "After" datasets, helping assess the consistency of changes across the bands.

 Figure: ResNet-152 Model:
  ![image](https://github.com/prajwalsg/EEG-Brain-signal-analyses-to-determine-impact-of-music/assets/90396143/3cf3954a-0b1c-4055-be5f-e7bbab65745c)

ResNet-152 represents a remarkable advancement in deep learning architecture, characterized by its formidable depth of 152 layers. At the core of its innovation lies the introduction of residual connections, which redefine the approach to training profoundly deep neural networks. These connections allow information to bypass certain layers, enabling the network to learn residual mappings. This novel strategy mitigates the vanishing gradient problem encountered in traditional deep networks, facilitating smoother optimization of model parameters. As a result, ResNet-152 achieves unprecedented levels of performance in various computer vision tasks, showcasing its efficacy in handling complex image data with remarkable accuracy and efficiency.

# UI
![image](https://github.com/prajwalsg/EEG-Brain-signal-analyses-to-determine-impact-of-music/assets/90396143/02e6eeda-46a9-4ba8-aaed-5fe7ddeb4ab1)

# Result 
![image](https://github.com/prajwalsg/EEG-Brain-signal-analyses-to-determine-impact-of-music/assets/90396143/8dfe08d2-d4b5-4ab2-8053-08603fdde846)

![image](https://github.com/prajwalsg/EEG-Brain-signal-analyses-to-determine-impact-of-music/assets/90396143/9e1bb57d-e32b-47df-8c30-0d67d0420013)


©copyrighted only for fair use and research purposes only...



