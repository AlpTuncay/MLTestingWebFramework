from flask.cli import FlaskGroup
from project import create_app, database
import unittest

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command("create-db")
def create_db():
    database.create_all()
    database.session.commit()


@cli.command("recreate-db")
def recreate_db():
    database.drop_all()
    database.create_all()
    database.session.commit()


@cli.command("test")
def run_tests():
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command("seed-db")
def seed_db():
    pass


if __name__ == '__main__':
    cli()
