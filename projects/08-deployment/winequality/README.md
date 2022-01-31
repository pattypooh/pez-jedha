### Deployment project for Jedha Certification


This directory is a copy or the original repository containing the projetct.  Please go to this repository  [winequality](https://github.com/pattypooh/wine-quality)

Content :
- models/: Contains the model to be deployed
- templates/: Contains an html file that represents the API page.  It explains how the API can be used.
- Procfile : File needed by Heroku which has the command line launch the webserver (in this case, gunicorn)
- wine.py : The flash application

To test the application using a notebook, you can use the notebook Test_Endpoint in the root directory of this project (one level up)


To test the application deployed in Heroku, use the following https://pez-wine-app.herokuapp.com/ . The instructions on how to use the API are explained in there
