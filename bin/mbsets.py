#!/usr/local/bin/python

import os
import basics
import bfiles
import config

modnumlist = []
dups = 0


def DoSet(pif, setfile, set_id=None):
    tables = setfile.tables

    ostr = '<center>'

    '''
    if len(tables) > 1:
        bar = False
        for table in tables:
            if bar:
                ostr += "|",
            else:
                bar = True
            ostr += '<a href="#%(label)s">%(title)s</a>' % table,
        ostr += '\n'
    '''

    for db in tables:
        if len(tables) == 1 or not db['title'] or set_id == db['label'] or set_id == 'all':  # or not set_id
            ostr += PrintTable(pif, db, setfile)
        else:
            ostr += PrintNoTable(pif, db)

    ostr += '</center>\n'
    ostr += pif.render.FormatButtonComment(pif, '')
    return ostr


def PrintTable(pif, db, setfile):
    global modnumlist, dups
    ostr = '<a name="%(label)s"></a>\n' % db
    if db['title']:
        ostr += '<h3>%s</h3>\n' % db['title']
    ostr += pif.render.FormatTableStart()
    prefix = db['prefix']

    ncols = 0
    ostr += '\n' + pif.render.FormatRowStart()
    for field in db['header']:
        if field in setfile.colheads:
            #ostr += '    <th align=center>%s</th>' % setfile.colheads[field]
            ostr += pif.render.FormatCell(ncols, setfile.colheads[field], True)
            ncols = ncols + 1
    ostr += pif.render.FormatRowEnd()

    for model in db['model']:
        showme = True
        for field in db['header']:
            if pif.FormHas(field):
                if model[field] != pif.FormStr(field) or (not model[field] and not pif.FormStr(field)):
                    showme = False
        if not showme:
            continue
        ostr += pif.render.FormatRowStart()
        if 'text' in model:
            # Need to calculate the colspan better.
            ostr += pif.render.FormatCell(0, model['text'], False, {'colspan': len(db['header']) - 1})
            ostr += pif.render.FormatRowEnd()
            continue
        if 'section' in model:
            # Need to calculate the colspan better.
            #ostr += '    <th colspan=%d valign=top>\n' % (len(db['header']) - 1)
            #ostr += model['section']
            #ostr += '</th></tr>\n'
            ostr += pif.render.FormatSection(None, model['section'], also={'colspan': (len(db['header']) - 1)})
            continue
        ifield = 0
        for field in db['header']:
            if field == 'desc':
                ostr += pif.render.FormatCell(ifield, ModDesc(model[field]))
            elif field == 'fulldesc':
                ostr += pif.render.FormatRowEnd()
                ostr += pif.render.FormatRowStart()
                ostr += pif.render.FormatCell(ifield, ModDesc(model['desc']), False, {'colspan': repr(db['ncols'])})
            elif field == 'insetdesc':
                ostr += pif.render.FormatRowEnd()
                ostr += pif.render.FormatRowStart()
                ostr += pif.render.FormatCell(ifield, ModDesc(model['desc']), False, {'colspan': repr(db['ncols'] - 1)})
            elif field == 'num':
                modnums = []
                for modnum in model[field].split(';'):
                    modnum = ModNum(prefix, modnum, model.get('rank'))
                    if dups:
                        if modnum in modnumlist:
                            model['desc'].append('duplicate!')
                        modnumlist.append(modnum)
                    modnums.append(modnum)
                ostr += pif.render.FormatCell(ifield, '<nobr>%s</nobr>' % "<br>".join(modnums), False, {'height': '8'})
            elif field == 'pic':
                modnum = model['num'].split(';')
                also = {}
                if 'insetdesc' in db['header']:
                    also = {'rowspan': '2'}
                ostr += pif.render.FormatCell(ifield, Img(pif, prefix, modnum, model.get('rank'), int(db['digits']), (model['year'] != 'not made'), dirs=setfile.dirs), False, also)
            elif field == 'fullpic':
                ostr += pif.render.FormatRowEnd()
                ostr += pif.render.FormatRowStart()
                modnum = model['num'].split(';')
                also = {'colspan': repr(db['ncols'])}
                if 'insetdesc' in db['header']:
                    also = {'rowspan': '2'}
                ostr += pif.render.FormatCell(ifield, Img(pif, prefix, modnum, model.get('rank'), int(db['digits']), (model['year'] != 'not made'), dirs=setfile.dirs), False, also)
            elif field == 'name':
                if model[field]:
                    ostr += pif.render.FormatCell(ifield, '<center><b>' + model[field] + '</b></center>')
                else:
                    ostr += pif.render.FormatCell(ifield)
            else:
                if model[field]:
                    ostr += pif.render.FormatCell(ifield, model[field])
                else:
                    ostr += pif.render.FormatCell(ifield)
            ifield += 1
        ostr += pif.render.FormatRowEnd()
    ostr += '</table>\n'
    return ostr


def PrintNoTable(pif, db):
    global modnumlist, dups
    ostr = '<a name="%(label)s">\n' % db
    ostr += '<h3><a href="/cgi-bin/sets.cgi?page=' + pif.FormStr('page') + '&set=%(label)s#%(label)s">%(title)s</a></h3>\n' % db
    return ostr


def ModDesc(desclist):
    if desclist:
        ostr = '<ul>\n'
        for desc in desclist:
            ostr += ' <li>' + desc + '\n'
        ostr += '</ul>\n'
    else:
        ostr = '&nbsp;\n'
    return ostr


def ModNum(prefix, model, suffix):
    ostr = model
    if prefix:
        ostr = prefix + '-' + ostr
    if suffix:
        ostr += '-' + suffix
    return ostr


def Img(pif, prefix, model, suffix, digits=0, made=True, dirs={}):
    pif.render.Comment(prefix, model, suffix, digits, made)
    if not isinstance(model, list):
        model = [model]
    modnum = []
    for m in model:
        try:
            fmt = "%%0%dd" % digits
            m = fmt % int(m)
        except TypeError:
            pass
        except ValueError:
            pass
        if prefix:
            m = prefix + m
        if suffix:
            m += suffix
        modnum.append(m)
    ostr = pif.render.FormatImageRequired(modnum, ModNum(prefix, model[0], suffix), made=made, pdir=dirs.get(prefix))
    return '<center>' + ostr + '</center>'


def scmp(a, b):
    r = cmp(a['page_info.description'], b['page_info.description'])
    if r == 0:
        r = cmp(a['page_info.title'], b['page_info.title'])
    return r

def SelectSet(pif):
    ostr = "A few of the special sets produced by Matchbox in recent years:\n<ul>\n"
    ser = pif.dbh.FetchPages("id like 'sets.%' and (flags & 1)=0;")
    ser.sort(scmp)
    for ent in ser:
        ostr += '<li><b><a href="../' + pif.cgibin + '/' + ent['page_info.format_type'] + '.cgi?page=' + ent['page_info.id'][5:] + '">' + ent['page_info.title'] + '</a></b> - ' + ent['page_info.description'] + "\n"
    ostr += "</ul>\n"
    ostr += pif.render.FormatButton("back", link="..")
    ostr += " to the main index.\n"
    return ostr


@basics.WebPage
def SetsMain(pif):
    pif.render.PrintHtml()

    if pif.FormHas('page'):
        set_id = pif.FormStr('set')
        global dups
        dups = pif.FormInt('dups')
        setfile = bfiles.SetFile(os.path.join(config.srcdir, pif.FormStr('page') + '.dat'))
        print pif.render.FormatHead()
        print DoSet(pif, setfile, set_id)
    else:
        print pif.render.FormatHead()
        print SelectSet(pif)

    print pif.render.FormatTail()


if __name__ == '__main__':  # pragma: no cover
    pass
