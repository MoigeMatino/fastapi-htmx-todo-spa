#!/bin/bash
docker-compose exec app pytest --cov=app --maxfail=1
