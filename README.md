# NespressoMetropolisTrainingApp

## Description

This project was created with the intent best educate both new and existing Nespresso Coffee specialists reagrding the various coffee flavours and each their respective taste profiles, as well as make recommendations for alternative coffee flavours based on a user selected coffee. In turn, the Nespresso Coffee specialists improve their knowledge of the coffee flavours to a greater degree to provide more accurate recommendations to customers. In actuality, this project is a machine learning and natural language processing (NLP) web application in the guise of a training platform.

The core audience of this application are Nespresso Coffee Specialists; in particular those of the Metrotown Boutique branch. However, as the application was created to serve as a cross-hierarhical referential tool for employees that are both in the front-line and in managerial roles due to the user experience of the application emulating a dashboard yet with high-level machine learning capabilities. This application was created during my Fall 2022 Semester at Douglas College to fulfill the term project requirement of CSIS 3290: Fundamentals of Machine Learning.

This project in its entirety was developed using the Python programming language along with the Numpy, Pandas, Scikit-Learn, NLTK, Matplotlib, Seaborn, WordCloud, Plotly, and Dash libraries. 

This project was developed in two stages.

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

## How to Install and Run the Project

1. Install Python on your computer (if it is not already installed). The Python programming language can be installed from its official website, although packages do not come pre installed. An alternate version can be installed from the Anaconda Distribution which is geared towards Data Science & Machine Learning with relavant packages coming pre-installed.
    * [Official Python Version](https://www.python.org/)
    * [Anaconda Python Version](https://www.anaconda.com/products/distribution)
2. Install Microsoft Visual Studio Code, or any other Text Editor/IDE that is able to run Python code. For the purpose of this set instructions, it will be presumed Microsoft Visual Studio Code is used; in my opinion, it is one of the most lightweight and versatile text editors for programming in multiple scripting languages.
    * [Microsoft Visual Studio Code](https://code.visualstudio.com/)
3. Perform the following commands to retrieve the project from GitHub. For simplicity purposes, it is best to save the project repository on your Desktop. Note that the commands shown below are presuming that you are using a Mac OS X or Linux based Operating System. If using Windows Operating system, the terminal commands would differ.

        $ cd Desktop
        $ git clone https://github.com/kjeshang/NespressoMetropolisTrainingApp

    You can also install the project manually from this repository, however you would have to unzip the 

4. The GitHub repository of the project should now be saved on your desktop with the name **NespressoMetropolisTrainingApp**. Using the Operating System GUI, open the aforementioned project directory. The **NespressoTrainingApp** directory should be visible. This directory contains the actual web application.
5. Launch Microsoft Visual Studio Code.
6. Open the **NespressoTrainingApp** directory in Microsoft Visual Studio Code.
7. Navigate to **_app.py_**. This file instantiates the web application, which is a Plotly Dash application, and runs it on a local server on your computer.
8. Run the application by selecting the "Play" icon on the top right-hand corner of the Microsoft Visual Studio Code window. An in-built terminal should pop-up at the bottom of the Microsoft Visual Studio Code window indicating that the application is running on a local server. In my case, the application was running on local host in port 8050.
9. Open any web browser of your choice and enter `http://127.0.0.1:8050/` in the URL search bar and then press the ENTER key. After this, you will be able to access and utilize the web application.

## Video Presentation (i.e., How to Use the Project)

Below is a link to video that demonstrates in great detail the functionality and features of the application. In turn, the video also serves as an instructional video on how to utilize the application.

Background Music: A Day to Remember by Storyblocks (Provided by Clipchamp)

[![Nespresso Metropolis Training App - Demonstration Video](https://github.com/kjeshang/NespressoMetropolisTrainingApp/blob/main/Report/Images/mq2.jpeg?raw=true)](https://youtu.be/1LL-yqbQuig "Nespresso Metropolis Training App Demonstration Video")

## Credits

This project was developed independently yet I consider it a culmination of my knowledge & experience working as a Nespresso Coffee Specalist at the Metrotown Branch. I would not have been able to conceive such a project without the thorough training, guidance and support regarding on the product line-up and duties of being a Coffee Specialist from my Managers, Team Leaders, and the Senior Coffee Specialists.

In regards to the development of this project, I would like to thank my Boutique Manager, Compliance Team Leader, Bard Team Leader, and Total Quality Management Team Leader for providing me direct opinions and feedback during the analysis stage and post-completion of the whole project.