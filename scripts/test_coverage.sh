#!/bin/bash

cd tests || exit
pytest --cov=src
