import sys
import os

def init(name, file):
    if name != '__main__':
        print("%s cannot be imported as a module; please run as a script instead." % __file__)
        sys.exit(1)

    sys.path.append(os.path.abspath(
        os.path.join(
            os.path.dirname(file), '..', 'src'
        )
    ))
