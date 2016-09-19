TESTING = True

# Statement for enabling the development environment
DEBUG = True

# SSL
SSL_CRT = r"E:\SourceCode\ucr_db\UCR.crt"
SSL_KEY = r"E:\SourceCode\ucr_db\UCR.key"

# Port to run on
PORT = 8443

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = r"mssql+pyodbc://ucr_db_admin:ucr_db_admin@cornice.digit.utah.edu/ucr_test?driver=ODBC+Driver+13+for+SQL+Server"
DATABASE_CONNECT_OPTIONS = {}

PRESERVE_CONTEXT_ON_EXCEPTION = False
SQLALCHEMY_ECHO=False

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"

# Set this to not use CAS signle sign on server
DEV_MODE = True
# Set this to specifiy a specific role to use in DEV_MODE
#DEV_ROLE = "Contact Staff"

CAS_SERVER = "https://test.go.utah.edu"
CAS_AFTER_LOGIN = "website.root"
CAS_LOGIN_ROUTE = "/cas/login"
SESSION_TYPE = "filesystem"
PERMANENT_SESSION_LIFETIME = 300 # 5 minutes, will be overwritten by CAS configuration
SESSION_COOKIE_SECURE = True