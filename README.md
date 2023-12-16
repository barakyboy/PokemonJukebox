# Pokémon Jukebox  

### Welcome
Welcome to Pokémon Jukebox!  
This project is an experiment to see if pokemon can be beaten using the power of music!

#### NOTE
This project is is currently a work-in-progress. The front-end repo
will be linked here when it goes into production.  

### How does it work?
Essentially, the idea is to converts audio signals into 
gameboy input, and see if a Pokémon game can be beaten
only via music.
For an enjoyable experience, this was implemented via Twitch.
Twitch moderators for the channel of choice submit youtube links in chat which
are then processed by a pipeline that returns a processed
audio representation of the music  

#### How is the audio processed?
The audio is converted to midi via Spotify's open source basic-pitch
AI. From that point on certain pitches map to certain inputs.
  
## Components
There are three components to this repo:
- The main gameloop, in game.py
- The twitch service
- The ai-api 

The latter two have a provided Dockerfile. The Dockerfile for the ai-api
must be built from the src level in order to include the utilities folder.

### Setting up
To be set up, you must simply set the following .env files in the following locations:
1. (in git repo highest level) with the following variables:
(env variables will be set here when front-end is written)
2. In src/ai_api with the following variables:
(env variables will be set here when front-end is written)
3. In src/twitch with the following variables:
(env variables will be set here when front-end is written)

You will also need a gameboy ROM of a Pokémon (or any other) game

## Assets
A picture of a labeled gameboy is provided in img/gameboy_labled.png.
This picture is used to render the gameboy inputs in real time.

