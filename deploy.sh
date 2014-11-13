#!/bin/bash

git add .
git commit -m 'Update'
git push
git push heroku master
heroku logs --tail

