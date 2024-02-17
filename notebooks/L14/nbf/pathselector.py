import os
from ipywidgets import Select
from . import helpers

class PathSelector:
    
    type_prefix = {'relpath':   '⬆️ ',
                   'folder':    '  📁 ',
                   'file'  :    '  ',
                  }  
    
    def __init__(self, rootdir):
        self.rootdir = rootdir
        self.path = self.rootdir
        self.relpath = os.curdir
        
        self.widget = Select(options = self.get_options(), value = None, rows  = 5)
        self.widget.observe(self.on_select, names = 'value')
       
    def _make_options(self, folders, files):
        top = self.type_prefix['relpath'] + self.relpath
        folders = [self.type_prefix['folder'] + f for f in folders]
        files = [self.type_prefix['file'] + f for f in files]
        return [top] + folders + files
        
    def get_selected(self):
        val = self.widget.value
        for tp, pre in self.type_prefix.items():
            if val.startswith(pre):
                return tp, val.removeprefix(pre)
   
    def get_options(self):
        folders, files = helpers.folders_and_files(self.path)
        options = self._make_options(folders, files)
        return options
    
    def update_options(self):
        options = self.get_options()
        self.widget.unobserve(self.on_select, names = 'value')
        self.widget.options = options
        self.widget.value = None
        self.widget.observe(self.on_select, names = 'value')

    def on_select(self, change):
        tp, f = self.get_selected()
        if tp == 'file' or (tp == 'relpath'  and f == os.curdir):
            return
        elif tp == 'relpath':
            self.path = helpers.parent_dir(self.path) 
            self.relpath = os.path.relpath(self.path, self.rootdir)
        elif tp == 'folder':
            self.path = os.path.join(self.path, f)
            self.relpath = os.path.relpath(self.path, self.rootdir)
        else:
            raise Exception('Should never happen!')
            
        self.update_options()
        
    def __repr__(self):
        return 'PathSelector({})'.format(self.rootdir)
  
    def _ipython_display_(self):
        display(self.widget)   
