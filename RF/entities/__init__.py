from sqlalchemy.ext.declarative import declarative_base
import pkgutil
import inspect

# Get the DB Base Class
Base = declarative_base()

__all__ = ['Base']

# Load all Entities
for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(name).load_module(name)

    for name, value in inspect.getmembers(module):
        if name.startswith('__'):
            continue

        globals()[name] = value
        __all__.append(name)