import re,os

def readfile(filename):
	fp = file(filename)
	data = fp.read()
	fp.close()
	return data

_path = '../branch/%s'
f = [_path % 'kernel.py']
for root,folder,files in os.walk(_path % 'plugins'):
	for _file in files:
		if _file[0] not in ['_','.'] and _file.endswith('.py'):
			f.append(os.path.join(root,_file))

print 'Found files: %s' % len(f)
_func = []

for t in f:
	_file = readfile(t)
	_func += re.findall('def\ (.*?)\(',_file)

print 'Found functions: %s' % len(_func)

_unused = []
_once = []
for fn in _func:
	cnt = 0
	for t in f:
		_file = readfile(t)
		func = re.findall('(?<!def\ )(%s)\(' % fn,_file)
		if func: cnt += len(func)
		func = re.findall('[\,\(\[\=]{1}\ ?(%s)[\,\]\)]{1}' % fn,_file)
		if func: cnt += len(func)
		func = re.findall('\.(%s)' % fn,_file)
		if func: cnt += len(func)
	if cnt == 0:
		_unused.append(fn)
		print fn
	elif cnt == 1:
		_once.append(fn)

_once.sort()
		
print 'Total unused functions: %s' % len(_unused)
print 'Total once time used: %s' % len(_once)
#print ' | '.join(_once)
