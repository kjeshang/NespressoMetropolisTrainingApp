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

For more detailed information regarding this stage of the project, please refer to the _Term Project Report_ within the **_Report Directory_** of this repository.

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
3. Perform the following commands to retrieve the project from GitHub, and install the relevant Python packages that are necessary to locally run the application. For simplicity purposes, it is best to save the project repository on your Desktop. Note that the commands shown below are presuming that you are using a Mac OS X or Linux based Operating System. If using Windows Operating system, the terminal commands would differ.

        $ cd Desktop
        $ git clone https://github.com/kjeshang/NespressoMetropolisTrainingApp
        $ cd NespressoMetropolisTrainingApp/NespressoTrainingApp
        $ pip install -r requirements.txt

    You can also install the project manually from this repository, however you would have to unzip the downloaded GitHub Repository zipped folder.

4. The GitHub repository of the project should now be saved on your desktop with the name **NespressoMetropolisTrainingApp**, along with relevant dependencies installed using the previous step's commands. Using the Operating System GUI, open the aforementioned project directory. The **NespressoTrainingApp** directory should be visible. This directory contains the actual web application.
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

This project was developed independently yet I consider it a culmination of my knowledge & experience working as a Nespresso Coffee Specalist at the Metrotown Branch.

In regards to the coding of this project, I would like to show my appreciation to Prof. Bambang Sarif, my Python & Machine Learning instructor during the Fall 2022 semester, who shared great knowledge and provided insights during the throughout the stages of this project. His supervisory support was imperative to the completion of this project. 

In addition, I would like to thank my Boutique Manager (Scott Sorrell), Compliance Team Leader (Ali Nikan), Bard Team Leader (Kashish Bhandari), and Total Quality Management Team Leader (Zoe Jia) for providing me direct opinions and feedback during the analysis stage and post-completion of the whole project. Furthermore, they are excellent professionals that consistently inspire me to become a better Coffee Specialist. The creation of this project has helped me understand the product line-up on a more inquisitive level, and I have become a more knowledgable Coffee Specialist for it.

### Project Testimonials

This section consists of testimonials about my project from members of the Nespresso Metrotown Team. The Name of the person may not be shown to protect the privacy of my colleague/supervisor/manager.

|Name|Role|Testimonial|
|--|--|--|
|Scott Sorrell|Boutique Manager|Kunal has created a program that can give our brand new coffee specialists the ability to suggest new blends to customers like a pro. As opposed to just basing their recommendations on similar intensities, this program goes into the many different qualities of each of our coffees and finds attributes that may appeal to somebody besides just one attribute. After 13 years with the company, I have learned a solid grasp of all the types of coffees and I am able to point out things that a customer might like in a new coffee but this program replicates many of my suggestions using the exhaustive level of data provided. We did a test run and it was able to replicate most of the recommendations that I personally would have chosen. An excellent example of how data can be used to create better customer satisfaction.|
|Kashish Bhandari|Bard Team Leader|Kunal has created something that has given ‘Training’ a new world. Training doesn’t always means just showing stuff but it also includes applying those concepts learned while training and this app has done that. This app helps new coffee specialists to try to learn to the best of their ability by testing themselves , as well as our customers to choose a coffee that best matches their tastes or needs. The use of technology/ data in a coffee world is what this project shows which is so outstanding. Myself, being a coffee trainer, sometimes it becomes hard to train new coffee specialists on some concepts and I think this app can be proven helpful in these cases as it provides a very detailed insight for everything.|
|Ali Nikan|Compliance Team Leader|Nespresso Metropolis Training App is perfectly done by Kunal, and has very complete and thorough data for training a new person at Nespresso. As a team leader, I know that "saying" all the information to a new hire could be overwhelming for them. However, Kunal's app can make the training easier for us team leaders because of its complete data and also detailed "visuals". It is always easier for a person to "see" what is happening instead of being told. We did a test with Kunal's app and it was flawless. For instance, in the recommendation section, we saw every recommendation of alternative coffees if someone likes a specific coffee. I have worked in Nespresso for two years now, and had to drink lots of coffee and talk to my colleagues to find out the coffees that are similar to each other. However, Kunal's app could show you all the similar coffees with facts and detailed visualisations. In fact, people could also filter some of the coffees to make their lives easier (decaffeinated or caffeinated, with milk or without milk). Kunal went above and beyond with creating this app, and made the training really easier. Since I am a compliance team leader, Kunal's app made me think of having a similar app, but for compliance training. That could make my training more efficient and effective! Thank you Kunal!|
|Santiago Vargas|Coffee Specialist|Nespresso Metropolis Training App is a well designed tool that reaches a high level of detail and finds links and patterns between the different flavours we have at Nespresso. It would be of great help to Nespresso workers at all levels during the training process, because it allows us to understand correlations between coffees that would be very difficult to find at plain sight. This would increase our ability to satisfy our customers' needs and give more accurate recommendations. I would like to highlight the "Word Cloud" section as an interesting use of the data, because it smoothly translates a complex data comparison into an easy-to-understand chart, and helps the end user to understand what to expect from a coffee in comparison to another. On the other hand, I also think that this project would have a potential use directly with customers. Either in the Nespresso Webpage/App or in-store, a well developed and user friendly dashboard with the proper filters could be an interactive and innovative addition to the whole Nespresso experience. |