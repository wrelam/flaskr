import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    # Only create a connection when one hasn't been made yet
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Return rows that behave like dicts for accessing columns by name
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    # Only close if a connection was made
    if db is not None:
        db.close()

def init_db():
    db = get_db()

    # Open a file relative to the flaskr package
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    # Clear the existing data and create new tables
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    # Call the given function when cleaning up after returning a response
    app.teardown_appcontext(close_db)
    # Call this command with the flask command
    app.cli.add_command(init_db_command)

