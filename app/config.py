from decouple import config

SQL_HOST = config("SQL_HOST")
SQL_USER = config("SQL_USER")
SQL_PASSWORD = config("SQL_PASSWORD")
SQL_DB = config("SQL_DB")
SQL_PORT = int(config("SQL_PORT"))
EMAIL = config("EMAIL")
EMAIL_PASSWORD = config("EMAIL_PASSWORD")
SEASON = int(config("SEASON"))
MIN_GAME = int(config("MIN_GAME"))
MAX_GAME = int(config("MAX_GAME"))
MAX_TEAM_ID = int(config("MAX_TEAM_ID"))
FILE_PATH = config("FILE_PATH")