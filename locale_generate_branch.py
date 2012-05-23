#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Locale generator for iSida Jabber Bot                                    #
#    Copyright (C) 2012 diSabler <dsy@dsy.name>                               #
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.    #
#                                                                             #
# --------------------------------------------------------------------------- #

import os,re

def readfile(filename):
	fp = file(filename)
	data = fp.read()
	fp.close()
	return data

def writefile(filename, data):
	fp = file(filename, 'wb')
	fp.write(data)
	fp.close()

def regenerate(ptl,locale_name):
	def L(text):
		if not len(text): return text
		try: return locales[text]
		except: return text
	path_to_locale = '%s/%s' % (ptl,locale_name)
	root_files = os.listdir(path_to_source)
	plugins_files = os.listdir(path_to_plugins)
	plugins_files.sort()
	file_list,localez = [],[]
	regex = r'L\(u?\'(.*?)\'\)'

	for tmp in root_files:
		if tmp[-3:] == '.py' and tmp[0] != '.': file_list.append('%s/%s' % (path_to_source,tmp))

	for tmp in plugins_files:
		if tmp[-3:] == '.py' and tmp[0] != '.': file_list.append('%s/%s' % (path_to_plugins,tmp))

	locales = {}

	if os.path.isfile(path_to_locale):
		lf = readfile(path_to_locale).decode('UTF').replace('\r','').split('\n')
		for c in lf:
			if ('#' not in c[:3]) and len(c) and '\t' in c: locales[c.split('\t',1)[0]] = c.split('\t',1)[1]
	else: print 'Locale not found!'

	result = locale_header + '\n\n'

	error_count = 0

	for tmp in file_list:
		body = str(readfile(tmp)).replace('\\\'','\'').replace('\\\"','\"').replace('\\\\','\\')
		tm = re.findall(regex,body,re.S+re.U)
		tm2 = re.findall('# translate: (.*)',body)
		if tm2: tm2 = tm2[0].split(',')
		if tm or tm2:
			for tmp2 in tm:
				if tmp2 not in localez:
					localez.append(tmp2)
					tm2.append(tmp2)
			if tm2:
				result += '%s%s\n' % (file_mark,'/'.join(tmp.split('/')[2:]))
				for tmp2 in tm2:
					tr = L(tmp2)
					if tmp2 == tr:
						error_count += 1
						loc = locale_mark
					else: loc = tr
					result += '%s\t%s\n' % (tmp2,loc)
				result += '\n'

	msg = 'write locale file: %s' % locale_name
	if error_count: msg += '\nmissed translations: %s\n' % error_count
	else: msg += '\nregenarated without mistakes!\n'

	return msg, result, len(localez)

path_to_source = '../branch'
path_to_locale = '../branch/locales/'
path_to_plugins = '%s/plugins' % path_to_source
locale_mark = 'NO_TRANSLATE'
file_mark = '# file: '
locale_header = '''#---------------------------------------------
#	  Autogenerate for locales
#	(c) Disabler Production Lab.
#---------------------------------------------'''

if __name__ == "__main__" :
	print '\n',locale_header.replace('#',''),'\n'
	lf = os.listdir(path_to_locale)
	for tmp in lf:
		if tmp[-4:] == '.txt':
			msg, result, lz = regenerate(path_to_locale,tmp)
			writefile(tmp,'%s\n' % result.encode('utf-8'))
			print msg
	print 'Total found definitions: %s\n' % lz
	print 'Done!'
