from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
from app.auth.model import Auth_DB
from app.wallet.model import Wallet_DB


app = create_app('config')

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()