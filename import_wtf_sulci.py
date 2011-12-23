#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Import dump of wtf base from sulci to iSida Jabber Bot                   #
#    Copyright (C) 2011 diSabler <dsy@dsy.name>                               #
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

import os, urllib, sqlite3, time

wtfbase = 'wtfbase.db'

def readfile(filename):
	fp = file(filename)
	data = fp.read()
	fp.close()
	return data

def rss_replace(ms):
	ms = ms.replace('<br>','\n')
	ms = ms.replace('<br />','\n')
	ms = ms.replace('<br/>','\n')
	ms = ms.replace('<![CDATA[','')
	ms = ms.replace(']]>','')
	ms = ms.replace('&lt;','<')
	ms = ms.replace('&gt;','>')
	ms = ms.replace('&quot;','\"')
	ms = ms.replace('&apos;','\'')
	ms = ms.replace('&amp;','&')
	return ms

print 'lets begin'
wo = readfile('wtf.txt')
wo = wo.split('INSERT INTO wtf VALUES')
print 'size:',len(wo)

os.system('rm -rf '+wtfbase)
#os.system('del '+wtfbase)
wtfst = sqlite3.connect(wtfbase)
cu_wtfst = wtfst.cursor()
cu_wtfst.execute('''create table wtf (ind integer, room text, jid text, nick text, wtfword text, wtftext text, time text)''')
cnt = 1
print 'Import wtf base ...'

for ww in wo[1:]:
	ww = ww[:-2]
	ww = ww.replace('\n','<tempo_splitter>').replace('\\\'','\\\\\'')
	ww = eval(ww)
	print cnt,
	jid = unicode(str(ww[2]).decode('utf-8'))+u'@'+unicode(str(ww[3]).decode('utf-8'))
	what = str(ww[5]).decode('utf-8')
	what = what.replace(u'<tempo_splitter>',u'\n')
	what = rss_replace(what)
	wtime = time.ctime(ww[0])
	cu_wtfst.execute('insert into wtf values (?,?,?,?,?,?,?)', (cnt,u'import',jid,ww[1],ww[4],what,wtime))
	cnt += 1
wtfst.commit()
wtfst.close()
print 'Done!'