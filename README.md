# T-Minus MBTA!

Welcome to T-Minus MBTA! This repo holds files that power https://tminusmbta.herokuapp.com.

## What is T-Minus MBTA?

T-Minus MBTA is a countdown timer web app. Users can build, save, and edit dashboards of countdown timer clocks for stations of interest in the Boston area.

T-Minus MBTA is powered by a live API, with real-time prediction data and schedules that update very frequently. For more information on the API, visit https://www.mbta.com/developers/v3-api.

## Features

- Countdown timers, just like you'd find at the station platform.
- Live data that refreshes every 15 seconds.
- Ability to create user accounts with email.
- Ability to log in with pre-authenticated social media accounts, such as Facebook, Github, and others. Includes OAuth support for the Recurse Center, which was a custom-developed functionality.
- Autocomplete search suggestions based on official MBTA station names.

## Technologies

- Back-end:
  - Python/Django:
    - Social Django
    - SSLServer
    - Crispy Forms
  - PostgreSQL
- Front-end:
  - Javascript
  - Bootstrap
  - HTML
  - CSS
- Deployment:
  - Heroku
  - Amazon S3

## Reflections

- I learned a lot working on this project.
- Writing a custom backend for social-core was a very worthwhile side-quest.
- The simplicity of Django is a double-edges sword. Because it handles so much, so gracefully, with so little operator input, it's easy to not learn how it works. And, it's not so easy to learn how it works. However, the source code is very legible, and in many ways instructive with regard to writing clean Python code.
