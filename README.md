To run flask_url_shortener2/flask_shorty
(affectionately named Get Shorty!) locally:

Libraries & Versions
see requirements.txt for list of dependencies

Activate virtual environment:
$ python3.9 -m venv venv
$ . vev/bin/activate

Export environment variables:
$ export FLASK_APP=app
$ export FLASK_ENV=development

Create and Configure Database (MySQL)
DB Name  = flask_url_shorten2 (change as required)
Edit line 9 in flask_shorty/__init__.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/flask_url_shorten2'

Run app
$ python run.py

Enjoy!
