"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email

url_signer = URLSigner(session)

@action('index')
@action.uses('index.html', db, auth.user)
def index():
    return dict(
        load_sightings_url = URL('load_sightings'),
        inc_sightings_url = URL('inc_sightings'),
        add_sightings_url = URL('add_sightings'),
        salutation = "Hello, my dear friend!",
    )

@action('load_sightings')
@action.uses(db, session, auth.user)
def load_sightings():
    rows = db(db.birds.user_email == get_user_email()).select().as_list()
    return dict(sightings=rows)

@action('add_sightings', method='POST')
@action.uses(db, session, auth.user)
def add_sightings():
    bird_species = request.json.get('bird_species')
    bird_count = request.json.get('bird_count')
    id = db.birds.insert(bird_species=bird_species, bird_count=bird_count)
    return dict(id=id)

@action('inc_sightings', method='POST')
@action.uses(db, session, auth.user)
def inc_sightings():
    id = request.json.get('id')
    bird = db(db.birds.id == id).select().first()
    assert bird.user_email == get_user_email() # Only the owner of the observation can inc it. 
    bird.bird_count += 1
    bird.update_record()
    return dict(bird_count=bird.bird_count)
