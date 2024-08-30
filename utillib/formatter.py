import sys;sys.path.append('/home/minhinc/tmp')
from MISC.utillib.util import utilcm
utilcm.usage(f'python3 {__name__}.py <configurationfile>',f'python3 {__name__}.py tt.json')
def readjson(jsondata):
 formatter=None
 if 'formatter' in jsondata:
  modulename=re.sub(r'(.*?)([.]\w+cm([.]\w+\()?).*$',r'\1',jsondata['formatter'])
  formatter=re.sub(r'.*([.]\w+cm).*',r'\1',jsondata['formatter']) if re.search(r'[.]\w+cm',jsondata['formatter']) else modulename
  funcname=re.sub(r'.*[.](.*)$',r'\1',jsondata['formatter']) if re.search('\(.*\)$',jsondata['formatter']) else 'get()'
  utilcm.print(f'M {modulename=} {{formatter=} {funcname=}')
  exec(f'from {modulename} import {formatter}' if not modulename==formatter else f'import {modulename}')
 [formatter.get(readjson(jsondata[xx])) if formatter else readjson(jsondata[xx]) for xx in jsondata if type(xx)==int]
 formatter.get(jsondata) if formatter else None
