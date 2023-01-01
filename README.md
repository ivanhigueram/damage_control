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
<table class="JSON-TO-HTML-TABLE"><thead><tr><th class="year-th">year</th><th class="retweeted-th">retweeted</th><th class="count-th">count</th></tr></thead><tbody ><tr ><td class="year-td td_num">2011</td><td class="retweeted-td td_num">0</td><td class="count-td td_num">81</td></tr>
<tr ><td class="year-td td_num">2012</td><td class="retweeted-td td_num">0</td><td class="count-td td_num">601</td></tr>
<tr ><td class="year-td td_num">2013</td><td class="retweeted-td td_num">0</td><td class="count-td td_num">496</td></tr>
<tr ><td class="year-td td_num">2014</td><td class="retweeted-td td_num">0</td><td class="count-td td_num">508</td></tr>
<tr ><td class="year-td td_num">2015</td><td class="retweeted-td td_num">0</td><td class="count-td td_num">314</td></tr>
<tr ><td class="year-td td_num">2015</td><td class="retweeted-td td_num">1</td><td class="count-td td_num">1</td></tr>
<tr ><td class="year-td td_num">2016</td><td class="retweeted-td td_num">0</td><td class="count-td td_num">156</td></tr>
<tr ><td class="year-td td_num">2016</td><td class="retweeted-td td_num">1</td><td class="count-td td_num">198</td></tr>
<tr ><td class="year-td td_num">2017</td><td class="retweeted-td td_num">0</td><td class="count-td td_num">86</td></tr>
<tr ><td class="year-td td_num">2017</td><td class="retweeted-td td_num">1</td><td class="count-td td_num">222</td></tr>
<tr ><td class="year-td td_num">2018</td><td class="retweeted-td td_num">0</td><td class="count-td td_num">18</td></tr>
<tr ><td class="year-td td_num">2018</td><td class="retweeted-td td_num">1</td><td class="count-td td_num">101</td></tr>
<tr ><td class="year-td td_num">2019</td><td class="retweeted-td td_num">0</td><td class="count-td td_num">11</td></tr>
<tr ><td class="year-td td_num">2019</td><td class="retweeted-td td_num">1</td><td class="count-td td_num">70</td></tr>
<tr ><td class="year-td td_num">2020</td><td class="retweeted-td td_num">0</td><td class="count-td td_num">19</td></tr>
<tr ><td class="year-td td_num">2020</td><td class="retweeted-td td_num">1</td><td class="count-td td_num">91</td></tr>
<tr ><td class="year-td td_num">2021</td><td class="retweeted-td td_num">0</td><td class="count-td td_num">21</td></tr>
<tr ><td class="year-td td_num">2021</td><td class="retweeted-td td_num">1</td><td class="count-td td_num">90</td></tr></tbody></table>
<!-- MARKDOWN-AUTO-DOCS:END -->

### To-do
 - [ ] Add Mastodon (:elephant:)
