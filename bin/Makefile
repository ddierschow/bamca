GIT = /usr/local/bin/git
RM = /bin/rm
DATE != date +'%Y%m%d'

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

dumpdb:
	@echo "This is looking for the database root password."
	@echo "Dumping to bamca"
	mysqldump -u root -p bamca > ../sql/bamca.mysql.$(DATE)
	@echo "Dumping to buser"
	mysqldump -u root -p buser | python ../sql/scrub.py > ../sql/buser.mysql.$(DATE)
