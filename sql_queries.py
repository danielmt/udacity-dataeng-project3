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
        gender CHAR(1),
        item_in_session INT NOT NULL,
        last_name VARCHAR,
        length FLOAT,
        level VARCHAR NOT NULL,
        location VARCHAR,
        method VARCHAR NOT NULL,
        page VARCHAR NOT NULL,
        registration INT,
        session_id INT NOT NULL,
        song VARCHAR,
        status INT NOT NULL,
        ts INT NOT NULL
        user_agent VARCHAR,
        user_id VARCHAR NOT NULL
    )
"""

staging_songs_table_create = """
    CREATE TABLE staging_songs (
        artist_id VARCHAR NOT NULL,
        artist_latitude FLOAT,
        artist_location VARCHAR,
        artist_longitude FLOAT,
        artist_name VARCHAR NOT NULL,
        duration FLOAT NOT NULL,
        num_songs INT NOT NULL,
        song_id VARCHAR NOT NULL,
        title VARCHAR NOT NULL,
        year INT NOT NULL
    )
"""

songplay_table_create = """
    CREATE TABLE songplay (
        songplay_id IDENTITY(0,1),
        start_time TIMESTAMP NOT NULL,
        user_id INT NOT NULL,
        level VARCHAR NOT NULL,
        song_id VARCHAR(18),
        artist_id VARCHAR(18),
        session_id INT NOT NULL,
        location VARCHAR NOT NULL,
        user_agent VARCHAR NOT NULL,
        PRIMARY KEY (songplay_id)
    )
"""

user_table_create = ("""
    CREATE TABLE user (
        user_id INT,
        first_name VARCHAR NOT NULL,
        last_name VARCHAR NOT NULL,
        gender CHAR(1) NOT NULL,
        level VARCHAR NOT NULL,
        PRIMARY KEY (user_id)
    )
""")

song_table_create = """
    CREATE TABLE song (
        song_id VARCHAR(18),
        title VARCHAR NOT NULL,
        artist_id VARCHAR(18) NOT NULL,
        year INT NOT NULL,
        duration FLOAT NOT NULL,
        PRIMARY KEY (song_id)
    )
"""

artist_table_create = """
    CREATE TABLE time (
        start_time TIMESTAMP NOT NULL,
        hour int NOT NULL,
        day int NOT NULL,
        week int NOT NULL,
        month int NOT NULL,
        year int NOT NULL,
        weekday int NOT NULL
    )
"""

time_table_create = """
    CREATE TABLE time (
        start_time TIMESTAMP NOT NULL,
        hour int NOT NULL,
        day int NOT NULL,
        week int NOT NULL,
        month int NOT NULL,
        year int NOT NULL,
        weekday int NOT NULL
    )
"""

# STAGING TABLES

staging_events_copy = ("""
    copy staging_events from 's3://udacity-dend/log_data'
    credentials 'aws_iam_role={}'
    json from 's3://udacity-dend/log_json_path.json'
    compupdate off
    region 'us-west-2';
""").format()

staging_songs_copy = ("""
    copy staging_songs from 's3://udacity-dend/song_data'
    credentials 'aws_iam_role={}'
    json 'auto'
    compupdate off
    region 'us-west-2';
""").format()

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
