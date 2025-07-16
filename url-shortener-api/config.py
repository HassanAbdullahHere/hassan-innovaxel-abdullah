import os
from dotenv import load_dotenv

load_dotenv()

mongo = os.getenv("MONGO_URI")
