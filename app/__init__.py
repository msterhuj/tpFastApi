from .database import init_engine
from fastapi.security import HTTPBasic
engine = init_engine()
security = HTTPBasic()
