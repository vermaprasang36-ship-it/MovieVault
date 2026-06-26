# MovieVault

MovieVault is a Python + SQL movie discovery app built with Streamlit. It allows users to search movies using the TMDB API, view movie details, and save selected movies to a personal watchlist stored in SQLite.

## Tech Stack

- Python
- Streamlit
- SQLite
- TMDB API

## Features Planned

- Search movies by title
- Browse popular movies
- View movie details
- Save movies to watchlist
- Mark movies as watched or unwatched
- Remove movies from watchlist

## Current Progress

### Week 1 / Backend Setup

Completed:
- Created project repository
- Added Python project files
- Created SQLite database file
- Created `watchlist` table
- Added database functions to:
  - Add a movie
  - Read all saved movies
  - Remove a movie
  - Update watched/unwatched status

## Database Design

### Table: `watchlist`

| Column | Type | Purpose |
|---|---|---|
| id | INTEGER | Unique local ID |
| tmdb_id | INTEGER | Movie ID from TMDB API |
| title | TEXT | Movie title |
| release_date | TEXT | Movie release date |
| rating | REAL | TMDB movie rating |
| overview | TEXT | Short movie description |
| poster_url | TEXT | Movie poster image URL |
| watched | INTEGER | 0 = not watched, 1 = watched |
| added_at | TIMESTAMP | Date and time when movie was saved |

## How to Run Database Setup

```bash
python database.py
