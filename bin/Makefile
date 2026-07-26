GIT = /usr/local/bin/git
RM = /bin/rm
DATE != date +'%Y%m%d'
FLAKE8 = /usr/local/bin/flake8

all: configs test

configs: ../templates/config.html ../htdocs/config.php

../templates/config.html ../htdocs/config.php: config.py
	./filsys.py p
	./filsys.py j

test:
	./checks.py

deploy: clean
	$(GIT) reset --hard HEAD
	$(GIT) pull
	$(GIT) pull --tags
	./filsys.py p
	./filsys.py j
	./filsys.py v

clean: lint
	$(RM) -f *~ __pycache__/*.pyc

lint:
	$(FLAKE8)

dumpdb:
	@echo "This is looking for the database root password."
	@echo "Dumping to bamca"
	mysqldump -u root -p bamca > ../sql/bamca.mysql.$(DATE)
	git add ../sql/bamca.mysql.$(DATE)
	@echo "Dumping to buser"
	mysqldump -u root -p buser | python ../sql/scrub.py > ../sql/buser.mysql.$(DATE)
	git add ../sql/buser.mysql.$(DATE)
