GIT = /usr/local/bin/git
RM = /bin/rm

all: configs test

configs: ../templates/config.html ../htdocs/config.php

../templates/config.html ../htdocs/config.php: config.py
	./filsys.py p
	./filsys.py j

test:
	./check

deploy: clean
	$(GIT) reset --hard HEAD
	$(GIT) pull
	./filsys.py p
	./filsys.py j

clean:
	$(RM) -f *~ *.pyc
