from settings import get_config


CONFIG = get_config()

ARN = CONFIG.get("IAM_ROLE", "ARN")
LOG_DATA = CONFIG.get("S3", "LOG_DATA")
LOG_JSON_PATH = CONFIG.get("S3", "LOG_JSONPATH")
SONG_DATA = CONFIG.get("S3", "SONG_DATA")

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplay"
user_table_drop = "DROP TABLE IF EXISTS user"
song_table_drop = "DROP TABLE IF EXISTS song"
artist_table_drop = "DROP TABLE IF EXISTS artist"
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
    registration INTEGER,
    session_id INTEGER NOT NULL,
    song VARCHAR,
    status INTEGER NOT NULL,
    ts INTEGER NOT NULL
    user_agent VARCHAR,
    user_id VARCHAR NOT NULL
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
    songplay_id IDENTITY(0,1) NOT NULL SORTKEY,
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
  CREATE TABLE artist (
    artist_id VARCHAR(18) SORTKEY,
    name VARCHAR NOT NULL,
    location VARCHAR NOT NULL,
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
  copy staging_events from '{LOG_DATA}'
  credentials 'aws_iam_role={ARN}'
  json from '{LOG_JSON_PATH}'
  compupdate off
  region 'us-west-2';
"""

staging_songs_copy = f"""
  copy staging_songs from '{SONG_DATA}'
  credentials 'aws_iam_role={ARN}'
  json 'auto'
  compupdate off
  region 'us-west-2';
"""

# FINAL TABLES

songplay_table_insert = """
"""

user_table_insert = """
"""

song_table_insert = """
"""

artist_table_insert = """
"""

time_table_insert = """
"""

# QUERY LISTS

create_table_queries = [
    staging_events_table_create,
    staging_songs_table_create,
    songplay_table_create,
    user_table_create,
    song_table_create,
    artist_table_create,
    time_table_create,
]

drop_table_queries = [
    staging_events_table_drop,
    staging_songs_table_drop,
    songplay_table_drop,
    user_table_drop,
    song_table_drop,
    artist_table_drop,
    time_table_drop,
]

copy_table_queries = [
    staging_events_copy,
    staging_songs_copy,
]

insert_table_queries = [
    songplay_table_insert,
    user_table_insert,
    song_table_insert,
    artist_table_insert,
    time_table_insert,
]
