# README #

How to set up the UCR Web App

### What is this repository for? ###

* This is a Flask-Python web app/server that uses a SQL Server backend to store cancer patient and study informantion

### How do I get set up? ###

* Install [Anaconda](https://www.continuum.io/downloads) or [Miniconda](http://conda.pydata.org/miniconda.html) for Python 3.4+
* Optionally create a virtual environment in conda
* Install the dependencies (pip3 install -r Python/requirements.txt) into the conda installation. Note pyodbc will probably not install properly as it needs to be compilied.
* Install pyodbc from conda repo (conda install pydobc)
* Clone the repository (webappwithauth branch) to your machine
* Edit the config.py to meet your needs (uncomment DEV_MODE and DEV_ROLE, make sure it points to the right database and has the right connection properties etc...)
* Edit runserver.py to point to your certificate and key (see [here](http://flask.pocoo.org/snippets/111/) for more information (assuming you want to use basic SSL/TLS). Edit the port if you want.
* Navigate to the folder containing "runserver.py"
* Run the server (python runserver.py)
* You should now be able to navigate to localhost:\<port\> and see the website

### Getting the application to run with IIS ###

* Make sure you have a server configured with IIS and that you have a valid SSL Certificate to use
* On the server, do "How to I get set up?" steps but make sure the "DEV_MODE" and "DEV_ROLE" are commented out in the config.py file
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


### What are DEV_MODE and DEV_ROLE in the Config File? ###

* DEV_MODE is a flag that can be set which will ignore the CAS/SSO and basically create a fake user and pretend that that user is signed in.
* DEV_ROLE is a string that can be set to "Developer", "Contact Staff", "Director", "Informatics Staff", or "Research Manager". It is used to set the role of the fake user when DEV_MODE is set. 

These are meant to be used when developing on a local machine. Since the CAS/SSO requires a SSL secured and whitelisted domain we must ignore the CAS login stuff.