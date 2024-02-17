import  nbf, sys
nargs = len(sys.argv)
if nargs > 1 and (nargs !=3 or sys.argv[1] != 'up' and not sys.argv[2].isnumeric()):
    print('Usage: %run -m nbf   ODER %run -m nbf -- up number\nnumber: durchsuche n-tes Elternverzeichnis')
else:
    root = sys.argv[-1] if nargs == 3 else None
    nbf.run(root)