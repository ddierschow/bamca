GIT = /usr/local/bin/git
RM = /bin/rm

all: configs test

configs: ../templates/config.html ../htdocs/config.php

../templates/config.html ../htdocs/config.php: config.py
	./filesys.py p
	./filesys.py j

test:
	./check

deploy: clean
	$(GIT) reset --hard HEAD
	$(GIT) pull
	./filesys.py p
	./filesys.py j

clean:
	$(RM) -f *~ *.pyc
