# ES-Movies

[![Python](https://img.shields.io/badge/python-Flask-000000?logo=flask&logoColor=fff)](requirements.txt)
[![Common Lisp](https://img.shields.io/badge/Common%20Lisp-SBCL-8CA1AF)](backend/expert_system/expert_system.lisp)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff)](Dockerfile)

A movie recommendation app built around a rule-based expert system
instead of a machine-learning model: you enter your favorite movies and
your current mood, and a Common Lisp reasoning engine picks a match by
applying explicit rules over genres, ratings, and release data pulled
from The Movie Database (TMDB).

## Why an expert system

Most recommendation demos reach straight for a trained model. This
project explores the other classic AI approach: symbolic, rule-based
reasoning, where every recommendation can be traced back to the exact
rule that produced it. It's a deliberate contrast to the statistical
side of this portfolio (see
[wine-quality](https://github.com/Pierrafrom/wine-quality)).

## How it works

1. **Flask backend** (`app.py`, `backend/routes/`) serves the frontend
   and exposes an API to submit a user's favorite movies and mood, and
   to search TMDB for movies.
2. **TMDB integration** (`backend/services/movie_selector.py`) fetches
   movie data, with a local JSON cache to avoid refetching the same
   titles.
3. **Data conversion** (`backend/services/data_formatter.py`) turns the
   user's input and cached movie data into an S-expression Lisp can read.
4. **Expert system** (`backend/expert_system/expert_system.lisp`) runs as
   a subprocess via SBCL, reasons over the data, and returns a JSON
   recommendation.

```
Browser --> Flask API --> TMDB (movie data, cached)
                       --> Lisp data --> SBCL subprocess (expert_system.lisp)
                                      --> JSON recommendation --> Browser
```

## Setup

Requires Python 3.11+ and [SBCL](http://www.sbcl.org/) (Steel Bank Common
Lisp) on the PATH.

```bash
pip install -r requirements.txt
cp backend/config/.env.example backend/config/.env   # fill in TMDB_API_KEY
python app.py
```

Or with Docker, which installs SBCL for you:

```bash
docker build -t es-movies .
docker run -p 5000:5000 --env-file backend/config/.env es-movies
```

## Stack

Flask, Common Lisp (SBCL), TMDB API, Docker/Gunicorn for deployment.
