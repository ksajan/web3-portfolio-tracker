import app.src.loader.env_vars
from app.src.resource_handler.http import create_session

print("Creating HTTP session")
HTTP_SESSION = create_session()
