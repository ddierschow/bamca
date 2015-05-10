#!/usr/local/bin/python

import basics
import lineup


@basics.command_line
def main(pif):
    for y in pif.switch['y']:
        for r in pif.switch['r']:
            print lineup.text_main(pif, y, r)

if __name__ == '__main__':  # pragma: no cover
    main(options='ry')
