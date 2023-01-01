# Damage control: Clean traces from social media (mainly Twitter)

[![Trigger twitter deleter using a CRON
job](https://github.com/ivanhigueram/damage_control/actions/workflows/scheduled-build.yml/badge.svg)](https://github.com/ivanhigueram/damage_control/actions/workflows/scheduled-build.yml)

This repo runs a cronjob to delete and backup tweets yearly from my personal
account. The execution relies on Github actions to connect to the API, delete
tweeets under the desired timeframe and then backup to `backups` as a SQLite
dataset. 

The Github actions do a self-push on the backups only if there are changes on
the tables. Ideally, I should have done a schema and do not allow repetition on
commit, but lazyness. 

## Year summary
<!-- MARKDOWN-AUTO-DOCS:START (JSON_TO_HTML_TABLE:src=./backups/year_groupby.json) --> 


### To-do
 - [ ] Add Mastodon (:elephant:)
