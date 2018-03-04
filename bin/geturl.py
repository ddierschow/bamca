#!/usr/local/bin/python

import re, urllib2

import basics
import useful


'''
+-----------------+--------------+------+-----+---------+----------------+
| Field           | Type         | Null | Key | Default | Extra          |
+-----------------+--------------+------+-----+---------+----------------+
| id              | int(11)      | NO   | PRI | NULL    | auto_increment |
| page_id         | varchar(20)  | NO   | MUL |         |                |
| section_id      | varchar(20)  | YES  |     |         |                |
| display_order   | int(3)       | YES  |     | 0       |                |
| flags           | int(11)      | YES  |     | 0       |                |
| associated_link | int(11)      | YES  |     | 0       |                |
| last_status     | varchar(5)   | YES  |     | NULL    |                |
| link_type       | varchar(1)   | YES  |     |         |                |
| country         | varchar(2)   | YES  |     |         |                |
| url             | varchar(256) | YES  |     |         |                |
| name            | varchar(128) | YES  |     |         |                |
| description     | varchar(512) | YES  |     |         |                |
| note            | varchar(256) | YES  |     |         |                |
+-----------------+--------------+------+-----+---------+----------------+

+----+------------------------+---------------------------------------------------+----------------------------------------+
| id | page_id - section_id   | url                                               | name                                   |
+----+------------------------+---------------------------------------------------+----------------------------------------+
|  2 | links.others  -Linfo   | http://www.mbxforum.com/                          | Matchbox Forum International Documents |
|  4 | links.toylinks-Lmb     | http://matchbox.wikia.com/wiki/Matchbox_Cars_Wiki | Matchbox Cars Wiki                     |
|  5 | links.toylinks-Lpeople | http://www.toyvan.co.uk/                          | ToyVan                                 |
|  6 | links.toylinks-Linfo   | http://www.publicsafetydiecast.com                | Public Safety Diecast                  |
|  7 | links.toylinks-Lpeople | http://www.areh.de/                               | Matchbox Picture Dictionary            |
|  8 | links.toylinks-Lpeople | http://matchbox-dan.com/                          | Dan's Matchbox Picture Pages           |
|  9 | links.toylinks-Lmb     | http://www.mbxforum.com/                          | Matchbox Forum International           |
| 10 | links.toylinks-Lpeople | http://www.cfalkensteiner.com/                    | Christian Falkensteiner's Homepage     |
| 11 | links.dealers -Ldealer | http://www.kulitjerukbali.net/index.html          | Hard To Find Diecast Brokers           |
| 12 | links.toylinks-Linfo   | http://www.diecastplus.info/                      | diecastplus.info                       |
| 14 | links.toylinks-Lmb     | http://mb-db.co.uk                                | Matchbox Database of Variations        |
| 15 | links.toylinks-Lmb     | http://www.mbx-u.com/                             | Matchbox University                    |
| 16 | links.toylinks-Linfo   | http://chezbois.com/index.htm                     | Die-Cast Automotive Models             |
+----+------------------------+---------------------------------------------------+----------------------------------------+
'''

assoc_ids = {
    'MBXD':  2,
    'WIKI':  4,
    'VAN' :  5,
    'PSDC':  6,
    'AREH':  7,
    'MDAN':  8,
    'MBXF':  9,
    'CF'  : 10,
    'HTFD': 11,
    'DPLS': 12,
    'MBDB': 14,
    'MBXU': 15,
    'LW'  : 16,
}

def get_links(pif, assoc_id):
    return pif.dbh.fetch_link_lines(where='associated_link=%d' % assoc_ids[assoc_id])


# an auto link updater would be nice.  this would be part of it.

def import_psdc(pif):
    pref = 'http://www.publicsafetydiecast.com/'
    u = urllib2.urlopen('http://www.publicsafetydiecast.com/Matchbox_MAN.htm').read()
    u_re = re.compile('<a href="(?P<u>[^"]*)".*?<font.*?>(?P<i>.*?)<\/font>')
    q = get_links(pif, 'PSDC')
    ul = list(set([x['link_line.url'] for x in q]))
    pl = list(set(u_re.findall(u)))
    for l in pl:
        if not pref + l[0] in ul:
            print l[1], pref + l[0]

# ---- importers ------------------------------------------

importers = {
    'PSDC': import_psdc,
}

def import_links(pif):
    for assoc_id in assoc_ids:
	if assoc_id in importers:
	    importers[assoc_id](pif)

# ---- commands -------------------------------------------

cmds = [
    ('i', import_links, "import"),
]

@basics.command_line
def commands(pif):
    useful.cmd_proc(pif, './tlinks.py', cmds)

# ---- ----------------------------------------------------

if __name__ == '__main__':  # pragma: no cover
    commands(dbedit='')
