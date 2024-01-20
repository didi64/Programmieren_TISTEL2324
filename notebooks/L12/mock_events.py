from datetime import datetime

def _get_date():
    ds = datetime.today().strftime('%d,%m,%Y,%H,%M,%S').split(',')
    dmy = dict(zip(('Tag', 'Monat', 'Jahr'), ds[:3]))
    hms = tuple(int(x) for x in ds[3:])
    return dmy, hms
events = list('hms')
callbacks = {k:lambda x:x for k in events}
events_args = {'h': lambda: (('neue Stunde',)  +  (d:=_get_date())[1][:1], d[0]),
               'm': lambda: (('neue Minute',)  +  (d:=_get_date())[1][:2], d[0]),
               's': lambda: (('neue Sekunde',) +  (d:=_get_date())[1], d[0]),
              }

def register_callback(event, f):
    assert event in callbacks, 'unknown event "{}"'.format(event)
    callbacks[event] = f
    
def trigger_event(event):
    args, kwargs = events_args[event]()
    f = callbacks[event]
    f(args, **kwargs)    
