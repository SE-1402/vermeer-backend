vermeer-backend
===============

To run clone the project to your computer.

- git clone git@github.com:SE-1402/vermeer-backend.git

When you first 'cd' into the directory you'll be asked to initialize the 'virtual environment'.

This creates a directory at ~/.virtualenv/vermeer/, and all the dependencies for the project will be installed here.

To run the server:
- python server.py

To debug:
- python server.py debug

(You can also download intellij, or pycharm community editions to debug the server if neccessary.)

Credit goes to Autobahn|Python for the server implementation:
(https://github.com/tavendo/AutobahnPython)

From the WRT Node:
===============

1) ssh root@i.wrtno.de

2) ./mountUSB.sh

3) cd /mnt/shares

4) ./update.sh

5) source vermeer/bin/activate

6) pip install -r vermeer-backend-master/requirements

7) cd vermeer-backend-master

8) python vermeer/backend/server_asyncio.py
