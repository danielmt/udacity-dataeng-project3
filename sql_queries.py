from settings import get_config


CONFIG = get_config()

ARN = CONFIG.get("IAM_ROLE", "ARN")
LOG_DATA = CONFIG.get("S3", "LOG_DATA")
LOG_JSON_PATH = CONFIG.get("S3", "LOG_JSONPATH")
SONG_DATA = CONFIG.get("S3", "SONG_DATA")

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create = """
  CREATE TABLE staging_events (
    artist VARCHAR,
    auth VARCHAR NOT NULL,
    first_name VARCHAR,
    gender VARCHAR(1),
    item_in_session INTEGER NOT NULL,
    last_name VARCHAR,
    length DECIMAL,
    level VARCHAR NOT NULL,
    location VARCHAR,
    method VARCHAR NOT NULL,
    page VARCHAR NOT NULL,
    registration VARCHAR,
    session_id INTEGER NOT NULL,
    song VARCHAR,
    status INTEGER NOT NULL,
    ts TIMESTAMP NOT NULL,
    user_agent VARCHAR,
    user_id INTEGER
  )
"""

staging_songs_table_create = """
  CREATE TABLE staging_songs (
    artist_id VARCHAR NOT NULL,
    artist_latitude DECIMAL,
    artist_location VARCHAR,
    artist_longitude DECIMAL,
    artist_name VARCHAR NOT NULL,
    duration DECIMAL NOT NULL,
    num_songs INTEGER NOT NULL,
    song_id VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    year INTEGER NOT NULL
  )
"""

songplay_table_create = """
  CREATE TABLE songplays (
    songplay_id INTEGER IDENTITY(0,1) NOT NULL SORTKEY,
    start_time TIMESTAMP NOT NULL,
    user_id INTEGER NOT NULL DISTKEY,
    level VARCHAR NOT NULL,
    song_id VARCHAR(18) NOT NULL,
    artist_id VARCHAR(18) NOT NULL,
    session_id INTEGER NOT NULL,
    location VARCHAR NOT NULL,
    user_agent VARCHAR NOT NULL
  )
"""

user_table_create = ("""
  CREATE TABLE users (
    user_id INTEGER SORTKEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    gender VARCHAR(1) NOT NULL,
    level VARCHAR NOT NULL
  )
""")

song_table_create = """
  CREATE TABLE songs (
    song_id VARCHAR(18) SORTKEY,
    title VARCHAR NOT NULL,
    artist_id VARCHAR(18) NOT NULL,
    year INTEGER NOT NULL,
    duration DECIMAL NOT NULL
  )
"""

artist_table_create = """
  CREATE TABLE artists (
    artist_id VARCHAR(18) SORTKEY,
    name VARCHAR NOT NULL,
    location VARCHAR,
    latitude DECIMAL,
    longitude DECIMAL
  )
"""

time_table_create = """
  CREATE TABLE time (
    start_time TIMESTAMP NOT NULL,
    hour int NOT NULL,
    day int NOT NULL,
    week int NOT NULL,
    month int NOT NULL distkey,
    year int NOT NULL,
    weekday int NOT NULL
  )
"""

# STAGING TABLES

staging_events_copy = f"""
  COPY staging_events FROM {LOG_DATA}
  CREDENTIALS 'aws_iam_role={ARN}'
  FORMAT AS JSON {LOG_JSON_PATH}
  TIMEFORMAT as 'epochmillisecs'
  TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL
  COMPUPDATE OFF
  REGION 'us-west-2';
"""

staging_songs_copy = f"""
  COPY staging_songs FROM {SONG_DATA}
  CREDENTIALS 'aws_iam_role={ARN}'
  JSON 'auto'
  TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL
  COMPUPDATE OFF
  REGION 'us-west-2';
"""

# FINAL TABLES

songplay_table_insert = """
  INSERT INTO songplays
    (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
  SELECT
    DISTINCT ts,
    e.user_id,
    e.level,
    s.song_id,
    s.artist_id,
    e.session_id,
    e.location,
    e.user_agent
  FROM staging_events AS e
  JOIN staging_songs AS s ON e.artist = s.artist_name
  WHERE
    e.page = 'NextSong'
"""

user_table_insert = """
  INSERT INTO users
    (user_id, first_name, last_name, gender, level)
  SELECT
    DISTINCT user_id,
    first_name,
    last_name,
    gender,
    level
  FROM staging_events
  WHERE
    page = 'NextSong'
    AND user_id IS NOT NULL
"""

song_table_insert = """
  INSERT INTO songs
    (song_id, title, artist_id, year, duration)
  SELECT
    DISTINCT song_id,
    title,
    artist_id,
    year,
    duration
  FROM staging_songs
  WHERE
    song_id IS NOT NULL
"""

artist_table_insert = """
  INSERT INTO artists
    (artist_id, name, location, latitude, longitude)
  SELECT
    DISTINCT artist_id,
    artist_name,
    artist_location,
    artist_latitude,
    artist_longitude
  FROM staging_songs
  WHERE
    artist_id IS NOT NULL
"""

time_table_insert = """
  INSERT INTO time
    (start_time, hour, day, week, month, year, weekday)
  SELECT
    DISTINCT ts,
    EXTRACT(hour FROM ts),
    EXTRACT(day FROM ts),
    EXTRACT(week FROM ts),
    EXTRACT(month FROM ts),
    EXTRACT(year FROM ts),
    EXTRACT(weekday FROM ts)
  FROM staging_events
  WHERE
    page = 'NextSong'
    AND ts IS NOT NULL
"""

# QUERY LISTS

create_staging_table_queries = [
    ("staging_events", staging_events_table_create),
    ("staging_songs", staging_songs_table_create),
]

create_table_queries = [
    ("songplays", songplay_table_create),
    ("users", user_table_create),
    ("songs", song_table_create),
    ("artists", artist_table_create),
    ("time", time_table_create),
]

drop_staging_table_queries = [
    ("staging_events", staging_events_table_drop),
    ("staging_songs", staging_songs_table_drop),
]

drop_table_queries = [
    ("songplays", songplay_table_drop),
    ("users", user_table_drop),
    ("songs", song_table_drop),
    ("artists", artist_table_drop),
    ("time", time_table_drop),
]

copy_table_queries = [
    ("staging_events", staging_events_copy),
    ("staging_songs", staging_songs_copy),
]

insert_table_queries = [
    ("songplays", songplay_table_insert),
    ("users", user_table_insert),
    ("songs", song_table_insert),
    ("artists", artist_table_insert),
    ("time", time_table_insert),
]
