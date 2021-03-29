
1. git clone https://github.com/xsaysoft/blurapp-backend.git
2 . git checkout develop
3 .  cd  blurapp-backend
4 . Install virtualenv
5. activate  virtualenv
6.  install pip3
7. pip3 install -r requirements.txt
8. python migrate.py db init
9. python migrate.py db migrate
10. python migrate.py db upgrade
11. python run.py