# README #

How to set up the UCR Web App

### What is this repository for? ###

* This is a Flask-Python web app/server that uses a SQL Server backend to store cancer patient and study informantion

### How do I get set up? ###

* Install [Anaconda](https://www.continuum.io/downloads) or [Miniconda](http://conda.pydata.org/miniconda.html) for Python 3.4+
* Optionally create a virtual environment in conda
* Install the dependencies (pip3 install -r Python/requirements.txt) into the conda installation. Note pyodbc will probably not install properly as it needs to be compilied.
* Install pyodbc from conda repo (conda install pydobc)
* Add [one-line](https://github.com/cameronbwhite/Flask-CAS/issues/43) patch to flask-cas library in "flask_cas/routing.py lines 124/125"
    ```python
    attributes = xml_from_dict.get("cas:attributes", {})
    if attributes is None: attributes = {}
    ```
* Clone the repository (verify the branch) to your machine
* Edit the config.py to meet your needs
* Navigate to the folder containing "runserver.py"
* If you need to seed your database, use the seed_database.py script
* Run the server (python runserver.py)
* You should now be able to navigate to localhost:\<port\> and see the website

### Getting the application to run with IIS ###

* Make sure you have a server configured with IIS and that you have a valid SSL Certificate to use
* On the server, do "How to I get set up?" steps but make sure the "DEV_MODE", "JSON_API", and "DEBUG" are commented out in the config
* Verify that you can run server as localhost (this ensure the dependencies are correct
* Install wfastcgi into your conda python installation (conda install wfastcgi OR pip install wfastcgi)
* Make sure the "Web Server (IIS)" role is set up
* Right-click on that role on the left panel, choose "Add Role Services", then ensure that CGI (under Application Development) is installed
* Now click on "Internet Information Services (IIS) Manager" on the left and drill in on the right so that you can right-click on the "Sites" element and choose "Add Web Site"
* Add a site called "ucr", with a physical path of \<wherever you cloned the repo to\>\\Python, and bind it to port 8443 or 443, chose the appropriate certificate to use
* Click on your new web site, and double-click on "Handler Mappings" on the right pane under IIS
* Pick "Add Module Mapping" on the right, and enter:
    *	Request path: \*
    *  	Module: FastCgiModule
    *	Executable: C:\\Miniconda3\\python.exe|C:\\Miniconda3\\lib\\site-packages\\wfastcgi.pyc
    *	Name: python-wfastcgi
*	When you continue, you will be prompted to create a FastCGI application; say "Yes"
*	Click on your server in IIS and go to "FastCGI Settings". Open application (C:\\Miniconda3\\python.exe) and open the "Environment Variables"
    *	Add WSGI_HANDLER as runserver.app.wsgi_app
* Make sure your server/application is running and navigate to localhost:8443 or localhost:443. You should be prompted to enter your uID and password. If entered correctly, you will be redirected to the application.


### What do the extra variables in the config mean? ###

* DEV_MODE is a flag that can be set which will ignore the CAS/SSO and fake authenticates using the first user in your database. Since the CAS/SSO requires a SSL secured and whitelisted domain we must ignore the CAS login stuff when not working on a whitelisted server.
* SSL_CRT is the path to the certificate to use when running flask locally (development) with SSL enabled
* SSL_KEY is the path to the certificate key to use when running flask locally (development) with SSL enabled
* JSON_API is a boolean flag that can enable or disable the "/api" endpoint (which serves unprotected json)
* SQLALCHEMY_DATABASE_URI is the uri to connect to the sql server instance

