#!/usr/local/bin/python

import basics
import tlinks


@basics.command_line
def main(pif):
    tlinks.check_links(pif.filelist)

if __name__ == '__main__':  # pragma: no cover
    main()
