import os
import click
from app import create_app, db
from app.models.models import User, Role, Permission, Post, Comment
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
if __name__ == "__main__":
    app.run(host="", port=5000)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role,
                Permission=Permission, Post=Post, Comment=Comment)


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
