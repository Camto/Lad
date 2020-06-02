# The Heroku setup for Ladbot

Here is the Heroku setup for the bot and this website, because why not?

It uses two webpacks: the normal Python one, and my very own [MarkDown buildpack](https://github.com/Camto/heroku-buildpack-markdown), which is a fork of [this](https://github.com/jamesward/heroku-buildpack-markdown). It also uses the Postgres add-on.

That's it. It's just a Heroku app with those and the [GitHub repo](https://github.com/Camto/Lad). Oh and also you have to set the TOKEN config var to the bot's token.