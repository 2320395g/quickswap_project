@pragatimishra2506 
 quickswap_project
This repository is for the WAD2 Team Project.


QUICKSWAP is a web application in which users can trade items and invest their time either as a hobby or need.

Using this Repository
This repository uses a virtual environment with specific packages, therefore it is essential to activate the environment and installing the packages before running the application.

    $ cd quickswap_project
Virtual Environment
If you haven't already created a virtual environment, you can do using Anaconda.

    $ conda create -n quickswap_project python=3.7
    $ conda activate quickswap_project
Installing packages
A requirements.txt file mentions all the packages along with their versions used for this project. 
You can install them using:

     (quickswap_project)$ pip install -r requirements.txt
Running the App
The main Python file is manage.py.
It is important to makemigrations and migrate before running the app. This is done by

    (quickswap_project)$ python manage.py makemigrations
    (quickswap_project)$ python manage.py migrate
It is recommended that you also run the population script before.

    (quickswap_project)$ python populate_quickswap_project.py
The app can be run using

     (quickswap_project)$ python manage.py runserver
     and then use a browser to go to http://127.0.0.1:8000/

Running Tests
The test Python file is       
         quickswap_project\tests.py. 
   It includes tests for models (quickswap_project\models.py), population script (populate_quickswap_project.py) and forms (quickswap_project\forms.py). This file can be run using

      (quickswap_project)$ python manage.py test



Assessment
This project counts for 40% of the final grade for the course. This is further divided into three parts.

Design Specification
The design specification (a PDF providing a whole range of details regarding the design of the web application intended to implement) counts for 10% of the 40%. It is graded out of 20 marks and should include:

An overview of the application
User personas
Specifications i.e. minimal list of requirements
A high-level system architecture diagram
An ER diagram
Wireframes
Presentation
The presentation counts for 5% of the 40%. It should include:

a description of the design of the application, using some material from the design specification
an overview of the technologies used
a brief summary of the contributions of each team member
a demonstration of the web application
Note: Due to COVID-19, this presentation was done in the form of a video.

The Application / Project
The application / project is worth 25% of the 40%, graded out of 50 marks, and should be developed using Python, Django, HTML, CSS and associated technologies including JavaScript, JQuery and AJAX. The basic expectations include:





  
The app should involve user authentication
it should certainly interact with some kind of model stored in a database
it should be visually appealing and have an intuitive user interface
overall the functionality supported should be rich enough in order to demonstrate an understanding of the technologies listed above
Developed With
Bootstrap: a CSS, JavaScript and HTML framework used to develop highly-responsive websites
Django: a web application framework written in Python
Django-Crispy-Forms: helps render and style forms in a neat and simple way
Django-Extensions: a collection of custom extensions for the Django Framework
Django-Location-Field: a location field that supports maps and lets users pick locations
Django-Registration: provides user registration functionalities
JavaScript Libraries: some open-source JavaScript libraries that helped create this project; the files include URLs to the organisations
jQuery: a JavaScript library which simplifies programming operations
Pillow: a fork of PIL (Python Imaging Library)
Team Members
The following are the members of Lab 13 (Team E):

      Pragati Mishra
     Michael Griffiths
    Diego Drago
    Alistair Hewitt
    Lennon Donaghy





