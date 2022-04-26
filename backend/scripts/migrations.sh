#!/usr/bin/env bash
cd ../

alembic -n local revision --autogenerate -m "db migration"
alembic -n local upgrade head