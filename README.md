# Project: Sparkify AWS Pipeline

A music streaming startup, Sparkify, has grown their user base and song database
and want to move their processes and data onto the cloud. Their data resides in
S3, in a directory of JSON logs on user activity on the app, as well as a
directory with JSON metadata on the songs in their app.

This project will extract data from S3, stage into Redshift and transform the
data into a set of dimensional tables more suitable for analytics.


## Song data format

``` json
{
  "artist_id": "ARAJPHH1187FB5566A",
  "artist_latitude": 40.7038,
  "artist_location": "Queens, NY",
  "artist_longitude": -73.83168,
  "artist_name": "The Shangri-Las",
  "duration": 164.80608,
  "num_songs": 1,
  "song_id": "SOYTPEP12AB0180E7B",
  "title": "Twist and Shout",
  "year": 1964
}
```

## Event data format

``` json
{
  "artist": "Explosions In The Sky",
  "auth": "Logged In",
  "firstName": "Layla",
  "gender": "F",
  "itemInSession": 87,
  "lastName": "Griffin",
  "length": 220.3424,
  "level": "paid",
  "location": "Lake Havasu City-Kingman, AZ",
  "method": "PUT",
  "page": "NextSong",
  "registration": 1541057188796,
  "sessionId": 984,
  "song": "So Long_ Lonesome",
  "status": 200,
  "ts": 1543449470796,
  "userAgent": "\"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36\"",
  "userId": "24"
}
```

## Schema

### Staging Tables

#### staging_events

| Column          | Type                        | Nullable |
| --------------- | --------------------------- | -------- |
| artist          | VARCHAR                     | YES      |
| auth            | VARCHAR                     |          |
| first_name      | VARCHAR                     | YES      |
| gender          | VARCHAR(1)                  | YES      |
| item_in_session | INTEGER                     |          |
| last_name       | VARCHAR                     | YES      |
| length          | DECIMAL                     | YES      |
| level           | VARCHAR                     |          |
| location        | VARCHAR                     | YES      |
| method          | VARCHAR                     |          |
| page            | VARCHAR                     |          |
| registration    | VARCHAR                     | YES      |
| session_id      | INTEGER                     |          |
| song            | VARCHAR                     | YES      |
| status          | INTEGER                     |          |
| ts              | TIMESTAMP                   |          |
| user_agent      | VARCHAR                     | YES      |
| user_id         | INTEGER                     | YES      |

sort key: session_id
dist key: session_id

#### staging_songs

| Column           | Type                        | Nullable |
| ---------------- | --------------------------- | -------- |
| artist_id        | VARCHAR                     |          |
| artist_latitude  | DECIMAL                     | YES      |
| artist_location  | VARCHAR                     | YES      |
| artist_longitude | DECIMAL                     | YES      |
| artist_name      | VARCHAR                     |          |
| duration         | DECIMAL                     |          |
| num_songs        | INTEGER                     |          |
| song_id          | VARCHAR                     |          |
| title            | VARCHAR                     |          |
| year             | INTEGER                     |          |

dist key: artist_id
sort key: artist_id

### Fact Tables

#### songplays

Records in event data associated with song plays i.e. records with `page`
`NextSong`.

| Column      | Type                        | Nullable |
| ----------- | --------------------------- | -------- |
| songplay_id | INTEGER IDENTITY(0,1)       |          |
| start_time  | TIMESTAMP                   |          |
| user_id     | INTEGER                     |          |
| level       | VARCHAR                     |          |
| song_id     | VARCHAR(18)                 |          |
| artist_id   | VARCHAR(18)                 |          |
| session_id  | INTEGER                     |          |
| location    | VARCHAR                     |          |
| user_agent  | VARCHAR                     |          |

sort key: songplay_id
dist key: user_id

### Dimension Tables

#### users

Users in the app.

| Column     | Type              | Nullable |
| ---------- | ----------------- | -------- |
| user_id    | INTEGER           |          |
| first_name | VARCHAR           |          |
| last_name  | VARCHAR           |          |
| gender     | VARCHAR(1)        |          |
| level      | VARCHAR           |          |

sort key: user_id

#### songs

Songs in music database.

| Column    | Type                  | Nullable |
| --------- | --------------------- | -------- |
| song_id   | VARCHAR(18)           |          |
| title     | VARCHAR               |          |
| artist_id | VARCHAR(18)           |          |
| year      | INTEGER               |          |
| duration  | DECIMAL               |          |

sort key: song_id

#### artists

Artists in music database.

| Column    | Type                  | Nullable |
| --------- | --------------------- | -------- |
| artist_id | VARCHAR(18)           |          |
| name      | VARCHAR               |          |
| location  | VARCHAR               | YES      |
| latitude  | DECIMAL               | YES      |
| longitude | DECIMAL               | YES      |

sort key: artist_id

#### time

Timestamps of records in songplays broken down into specific units.

| Column     | Type                        | Nullable |
| ---------- | --------------------------- | -------- |
| start_time | TIMESTAMP                   |          |
| hour       | INTEGER                     |          |
| day        | INTEGER                     |          |
| week       | INTEGER                     |          |
| month      | INTEGER                     |          |
| year       | INTEGER                     |          |
| weekday    | INTEGER                     |          |

sort key: start_time
dist key: month

## Build

Pre-requisites:

- Python 3
- pyenv (optional)
- poetry

To install project python dependencies, run:

``` sh
poetry install
```

## Configuration

Copy `dwh.cfg.example` to `dwh.cfg`, and fill the settings for:

 - Redshift on `[CLUSTER]`
 - Your ARN to provide S3 access from Redshift on `[IAM_ROLE]`

The default database name is `sparkify`, which needs to be created on the
cluster.

## Running

To run the project, use `poetry` to activate the virtual environment:

``` sh
poetry shell
```

To create all tables (including staging area):

``` sh
./etl.py --create-tables --staging
```

To run the pipeline (including staging area):

``` sh
./etl.py --load-data --staging
```

If you don't need to reload data into staging area, you can drop `--staging`
parameter, which will only extract and transform data from staging area to final
tables.
