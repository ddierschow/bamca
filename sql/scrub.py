import sys

doing = True
while ln := sys.stdin.readline():
    if ln.startswith('-- Dumping data for table `user`'):
        doing = False
        sys.stdin.readline()
    elif ln.startswith('--'):
        if doing:
            sys.stdout.write(ln)
        else:
            doing = True
    elif doing:
        sys.stdout.write(ln)
