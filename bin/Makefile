GIT = /usr/local/bin/git
RM = /bin/rm

all: configs test

configs: ../templates/config.html ../htdocs/config.php

../templates/config.html ../htdocs/config.php: config.py
	./updcommits.py

test:
	./check

deploy: clean
	$(GIT) reset --hard HEAD
	$(GIT) pull

clean:
	$(RM) -f *~ *.pyc
