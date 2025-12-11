# Citizen Image

A FastAPI-based web application for image processing and management.

## Features
- RESTful API using FastAPI
- Image handling with Pillow
- PostgreSQL database integration via psycopg2-binary
- Environment configuration with python-dotenv

## Project Structure
```
src/
  config.py        # Configuration and environment variables
  db_client.py     # Database client setup
  main.py          # FastAPI application entry point
  utils.py         # Utility functions
Dockerfile         # Containerization setup
requirements.txt   # Python dependencies
```


## Environment Variables
Create a `.env` file in the project root for configuration. See `src/config.py` for required variables.

## License
MIT
