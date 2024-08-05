#!/bin/bash
set -x  # Enable debug mode
docker-compose exec app pytest --cov=app
