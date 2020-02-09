#!/usr/local/bin/python

from __future__ import print_function
import sys
import mbdata

jsfun = '''<SCRIPT LANGUAGE="JavaScript">
<!--

function pick(symbol) {
  if (window.opener && !window.opener.closed)
    window.opener.document.%s.value = symbol;
  window.close();
}

// -->
</SCRIPT>

'''


def countries_help():
    if len(sys.argv) > 1:
        print(jsfun % sys.argv[1])

    print("<table>")
    cols = 5
    rows = ((len(mbdata.countries) - 1) / cols) + 1
    while rows:
        print("<tr>")
        for col in range(0, cols):
            cc = mbdata.countries.pop(0)
            if len(sys.argv) > 1:
                print('''<td><a href="javascript:pick('%s')">%s</a></td>''' % cc)
            else:
                print('''<td>%s</td>''' % cc[1])
            if not mbdata.countries:
                break
        print("</tr>")
        rows -= 1
    print("</table>")

    """
    makes_help = '''<SCRIPT LANGUAGE="JavaScript">
<!--

function pick(symbol) {
  if (window.opener && !window.opener.closed)
    window.opener.document.%s.value = symbol;
  window.close();
}

// -->
</SCRIPT>

''' % sys.argv[1]
    """

    print("<table>")
    cols = 5
    rows = ((len(mbdata.countries) - 1) / cols) + 1
    while rows:
        print("<tr>")
        for col in range(0, cols):
            cc = mbdata.countries.pop(0)
            if len(sys.argv) > 1:
                print('''<td><a href="javascript:pick('%s')">%s</a></td>''' % cc)
            else:
                print('''<td>%s</td>''' % cc[1])
            if not mbdata.countries:
                break
        print("</tr>")
        rows -= 1
    print("</table>")
