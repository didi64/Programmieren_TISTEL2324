import re, os
from statistics import geometric_mean

def make_pat(word, escape = True, flags=0):
    '''returns a list of compiled regexes'''
    word = re.escape(word) if escape else word
    pat = re.compile(word, flags=flags)
    return pat  

def get_score(alls, anys=None):
    if not alls: 
        score = sum(anys)
    elif 0 in alls: 
        score = 0
    elif not anys: 
        score = geometric_mean(alls)
    else:    
        score = geometric_mean(alls) * sum(anys)
    
    return score

def file_iter(rootdir, filetypes = ('.ipynb',), exclude_dirs=('__pycache__',)):
    for root, folders, files in os.walk(rootdir):
        files[:] = [os.path.join(root,f) for f in  files if os.path.splitext(f)[1] in filetypes]
        folders[:] = [f for f in folders if not f.startswith('.') and f not in exclude_dirs]
        yield from files
        
def folders_and_files(path, filetypes = ('.ipynb',), exclude_dirs=('__pycache__',)):
    listing = os.listdir(path)
    visibles =  [f for f in listing if not f.startswith('.')]
    files = [f for f in  visibles if os.path.isfile(os.path.join(path, f)) and os.path.splitext(f)[1] in filetypes]
    folders = [f for f in visibles if os.path.isdir(os.path.join(path, f)) and f not in exclude_dirs]

    return sorted(folders), sorted(files)

def parent_dir(path):
    return os.path.abspath(os.path.join(path, os.pardir))     

def echo_args(*args, **kwargs):
    '''returns the arguments provided'''
    args_kwargs = []
    args_ = ', '.join('{!r}'.format(arg) for arg in args)
    if args_: 
        args_kwargs.append(args_)
        
    fs = ', '.join('{}={{{}!r}}'.format(k, k) for k in kwargs)
    kwargs_ =  fs.format(**kwargs)
    if kwargs_: 
        args_kwargs.append(kwargs_)
    
    return ', '.join(args_kwargs)
