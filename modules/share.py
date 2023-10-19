import pickle
import subprocess
from pathlib import Path

ROOT = '/home/tistel/work'
SRC = '/home/tistel/work/src'


def init_share(pin):
    with open(SRC + '/data/.init.pkl','rb') as f:
        data=pickle.load(f)
    with open(SRC + '/data/emails.pkl','rb') as f:
        emails=pickle.load(f)  
    
    tok = ''.join([chr((x-pin)) for x in data])
    if tok[6:11] != '_pat_':
        print('Ungueltiger Pin!', file=sys.stderr)
        return
    
    user = input('Enter Email prefix (Teil vor @):')
    if user + '@edu.teko.ch' not in [x for _,_,x in emails]:
        print('Prefix {} not found!'.format(user), file=sys.stderr)
        
    with open(ROOT + '/.user', 'w') as f:
        f.write(user)
        
    with open(ROOT  + '.token_tistel2324', 'w') as f:
        f.write(tok)
        
    res = subprocess.call(ROOT + '/bin/init_share')
    if res:
        print('share=Folder fuer User {} eingerichtet.'.format(user))     
    else:
        print('Etwas ging schief!', file=sys.stderr)
