#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import datetime
import sys
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500), default='')
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500), default='')

    def __repr__(self):
        return f'<Venue {self.id} {self.name}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))

    def __repr__(self):
        return f'<Artist {self.id} {self.name}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  start_time = db.Column(db.DateTime(), nullable=False)

  def __repr__(self):
      return f'<Show {self.id} {self.start_time}>'


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = Venue.query.distinct(Venue.state, Venue.city)
  venues = Venue.query.all()
  return render_template('pages/venues.html', venues=venues, data=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  data = Venue.query.filter(Venue.name.ilike('%'+request.form.get('search_term', '')+'%')).all()
  response = {
    "count": len(data),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data = Venue.query.get(venue_id)
  data.upcoming_shows = db.session.query(Show.start_time, Show.venue_id, Artist.id.label('artist_id'), Artist.name.label('artist_name'), Artist.image_link.label('artist_image_link')).filter(Show.venue_id == venue_id, Show.start_time > datetime.now()).join(Artist).all()
  data.upcoming_shows_count = len(data.upcoming_shows)
  data.past_shows = db.session.query(Show.start_time, Show.venue_id, Artist.id.label('artist_id'), Artist.name.label('artist_name'), Artist.image_link.label('artist_image_link')).filter(Show.venue_id == venue_id, Show.start_time <= datetime.now()).join(Artist).all()
  data.past_shows_count = len(data.past_shows)

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  req = request.form
  error = False
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  try:
    print(req.getlist('genres'))
    venue = Venue(name=req.get('name', ''), city=req.get('city', ''), state=req.get('state', ''), address=req.get('address', ''), phone=req.get('phone', ''), genres=req.getlist('genres'), facebook_link=req.get('facebook_link', ''), website_link=req.get('website_link', ''), image_link=req.get('image_link', ''), seeking_talent=(req.get('seeking_talent', '0')=='1'), seeking_description=req.get('seeking_talent_description', ''))
    print(req)
    db.session.add(venue)
    db.session.commit()
    id = venue.id
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort(404)
  else:
    print('id:')
    print(id)
    return render_template('pages/home.html')
  # on successful db insert, flash success
  #flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
      venue = Venue.query.get(venue_id)
      db.session.delete(venue)
      db.session.commit()
  except:
      db.session.rollback()
  finally:
      db.session.close()
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  data = Artist.query.filter(Artist.name.ilike('%'+ request.form.get('search_term')+'%')).all()
  response={
    "count": len(data),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data = Artist.query.get(artist_id)
  data.upcoming_shows = db.session.query(Show.start_time, Show.artist_id, Venue.id.label('venue_id'),
                                         Venue.name.label('venue_name'),
                                         Venue.image_link.label('venue_image_link')).filter(Show.artist_id == artist_id,
                                                                                              Show.start_time > datetime.now()).join(
      Venue).all()
  data.upcoming_shows_count = len(data.upcoming_shows)
  data.past_shows = db.session.query(Show.start_time, Show.artist_id, Venue.id.label('venue_id'),
                                         Venue.name.label('venue_name'),
                                         Venue.image_link.label('venue_image_link')).filter(Show.artist_id == artist_id,
                                                                                              Show.start_time <= datetime.now()).join(
      Venue).all()
  data.past_shows_count = len(data.past_shows)
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  try:
    artist = Artist.query.get(artist_id)
    req = request.form
    artist.name = req.get('name', '')
    artist.city = req.get('city', '')
    artist.state = req.get('state', '')
    artist.phone = req.get('phone', '')
    artist.genres = req.getlist('genres')
    artist.facebook_link = req.get('facebook_link', '')
    artist.website_link = req.get('website_link', '')
    artist.image_link = req.get('image_link', '')
    artist.seeking_venue = req.get('seeking_venue', '')
    artist.seeking_description = req.get('seeking_venue_description', '')
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Artist.query.get(venue_id)
    return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  try:
    venue = Venue.query.get(venue_id)
    req = request.form
    venue.name = req.get('name', '')
    venue.city = req.get('city', '')
    venue.state = req.get('state', '')
    venue.address = req.get('address', '')
    venue.phone = req.get('phone', '')
    venue.genres = req.getlist('genres')
    venue.facebook_link = req.get('facebook_link', '')
    venue.website_link = req.get('website_link', '')
    venue.image_link = req.get('image_link', '')
    venue.seeking_venue = req.get('seeking_talent', '')
    venue.seeking_description = req.get('seeking_talent_description', '')
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  req = request.form
  error = False
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  try:
    artist = Artist(name=req.get('name', ''), city=req.get('city', ''), state=req.get('state', ''), phone=req.get('phone', ''), genres=req.getlist('genres'), facebook_link=req.get('facebook_link', ''), website_link=req.get('website_link', ''), image_link=req.get('image_link', ''), seeking_venue=(req.get('seeking_venue', '0')=='1'), seeking_description=req.get('seeking_venue_description', ''))
    db.session.add(artist)
    db.session.commit()
    id = artist.id
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort(404)
  else:
      return render_template('pages/home.html')
  # on successful db insert, flash success
  flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = db.session.query(Show.id, Show.artist_id, Show.venue_id, Artist.name.label('artist_name'), Artist.image_link.label('artist_image_link'), Venue.name.label('venue_name'), Show.start_time).join(Artist).join(Venue).all()
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create', methods=['GET'])
def create_show_form():
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  req = request.form
  error = False
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  try:
    show = Show(artist_id=req.get('artist_id', ''), venue_id=req.get('venue_id', ''), start_time=req.get('start_time', ''))
    db.session.add(show)
    db.session.commit()
    id = show.id
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort(404)
  else:
      return render_template('pages/home.html')
  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
