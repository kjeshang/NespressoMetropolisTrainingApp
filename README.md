# NespressoMetropolisTrainingApp

## Description

This project was created with the intent best educate both new and existing Nespresso Coffee specialists reagrding the various coffee flavours and each their respective taste profiles, as well as make recommendations for alternative coffee flavours based on a user selected coffee. In turn, the Nespresso Coffee specialists improve their knowledge of the coffee flavours to a greater degree to provide more accurate recommendations to customers. In actuality, this project is a machine learning and natural language processing (NLP) web application in the guise of a training platform.

This project in its entirety was developed using the Python programming language along with the Numpy, Pandas, Scikit-Learn, Matplotlib, Seaborn, WordCloud, Plotly, and Dash libraries. This project was developed in two stages.

### First Stage: Analysis
In this stage of the project, I performed the following:
1. Data Retrieval
2. Data Transformation & Cleaning
3. Exploratory Data Analysis
4. Pre-Processing for NLP
5. Data Analysis
The above tasks were exclusively performed within Jupyter Notebooks. Anaconda Navigator was the software used to facilitate the Jupyter Notebooks, which utilizes Python Version 3.9.13 at the time of this writing.

For more detailed information regarding this stage of the project, please refer to the _Term Project Report_ within the Report Directory of this repository.

> The "5_DownloadImages" Jupyter Notebook was used to create a fully local version of the training application but due to the number of image files used, I am unable to push that version to GitHub. Thus, the version of the application that is pushed to GitHub retrieves images from the internet.

### Second Stage: Application
In this stage of the project, from the findings discovered and deductions made during previous stage, a web application is constructed that serves as a point of interaction for the user to understand the various coffee flavours and retrieve recommendations. This part of the project was exclusively performed using Python scripts that are structured in a project directory that lends well to develop a multi-page web application. Python Version 3.10.1 was used and the software used to facilitate development was Microsoft Visual Studio Code. The web application consists of the following sections (i.e., pages).

|Page|Description|
|--|--|
|Home Page|The landing page of the web application displaying the title of the project and my name.|
|About Page|The About page describes the project itself, its purpose, and the technologies used to develop it. In addition, credit is also given to those that provided me guidance during the development of this project.|
|Explore Page|The Explore page allows the user to perform a guided exploratory data analysis with visualizations designed to help provide insight regarding the dataset, as well as provide some selection & filteration options.|
|NLP Page|The NLP page is the interactive user interface to retrieve recommendations for on a user selected coffee based on specified feature engineering technique, similarity measure, and filteration & parameter option. Furthermore, coffee information and flavour & taste profile is communicated, along with feature charts and word clouds. Validation by means of classification is performed via specified feature engineering technique and Naive Bayes for a user specified target feature.|

## Video Presentation

Below is a link to video that demonstrates in great detail the functionality and features of the application. In turn, the video also serves as an instructional video on how to utilize the application.

Background Music: A Day to Remember by Storyblocks (Provided by Clipchamp)

[![Nespresso Metropolis Training App - Demonstration Video](https://github.com/kjeshang/NespressoMetropolisTrainingApp/blob/main/Report/Images/mq2.jpeg?raw=true)](https://youtu.be/1LL-yqbQuig "Nespresso Metropolis Training App Demonstration Video")