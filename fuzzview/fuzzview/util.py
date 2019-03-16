import os
import sys

def getenv(env_var):
    var_val = os.environ.get(env_var)

    if var_val is None:
        print(env_var + ' is not set.')
        sys.exit(1)
    
    return var_val
