# Olympic-news-web-application
This project is a web application about Olympic News. 
We use Python + Django + CSS + HTML + JS + JQuery + AJAX to complete this project. 
 
# How to run
After clonning our project, first you need to run the below command to access into rango_complete directory.
$ cd rango_complete



And then install the dependent package.


$ pip install -r requirements.txt



After that, you need to activate the app.


$ conda activate rango



Now, you can run these command to generate database and neccessry data.


$ python manage.py migrate


$ python manage.py makemigrations rango


$ python manage.py migrate


$ python population_script.py



If you successful do all above, now you can run our web application through this command.


$ python manage.py runserver


If you would like to test some function, we provide the tests.py. You can run it with the below command.


$ python manage.py test rango.tests


