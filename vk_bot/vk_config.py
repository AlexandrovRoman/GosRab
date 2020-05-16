import os

GROUP_ID = os.environ.get("GOS_RAB_GROUP_ID", 0)
TOKEN = os.environ.get("GOS_RAB_GROUP_TOKEN", "")
DB_USER = os.environ.get("DB_USERNAME", "")
DB_URL = os.environ.get("DB_URL", "localhost:5432")
DB_NAME = os.environ.get("VK_BOT_DB_NAME", "VK_BOT_PROJECT")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
EMAIL = os.environ.get("GOS_RAB_USER_EMAIL", 'EMAIL')
PASSWORD = os.environ.get("GOS_RAB_USER_PASSWORD", 'PASSWORD')
