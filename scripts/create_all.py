from _script_common import init
init(__name__, __file__)
from models import Base, engine

Base.metadata.create_all(bind = engine)
