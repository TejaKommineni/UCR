# Statement for enabling the development environment
DEBUG = True

# Define the database - we are working with
# SQLite for this example
#SQLALCHEMY_DATABASE_URI = r"sqlite:///E:\aaron_temp\SourceCode\UCR_DB_PyCharm\ucr_db\test_tb.db"
SQLALCHEMY_DATABASE_URI = r"mssql+pyodbc://cornice.digit.utah.edu/ucr?driver=ODBC+Driver+11+for+SQL+Server"
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret2"

# Secret key for signing cookies
SECRET_KEY = "secret2"

CAS_SERVER = "https://test.go.utah.edu"
CAS_AFTER_LOGIN = "website.root"
CAS_LOGIN_ROUTE = "/cas/login"
SESSION_TYPE = "filesystem"
PERMANENT_SESSION_LIFETIME = 300 # 5 minutes, will be overwritten by CAS configuration
SESSION_COOKIE_SECURE = True