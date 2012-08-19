Created by `Stephen McDonald <http://twitter.com/stephen_mcd>`_

Introduction
============

Gamblor is a real-time casino app built for the 2012
`Django Dash <http://www.djangodash.com/>`_.

The idea was to provide a plugin system for games that
can be played collaboratively in real-time using WebSockets,
and to that end Gamblor was successful.

Check out the deployed version at
`http://gamblor.jupo.org <http://gamblor.jupo.org>`_.

Features
========

Here are some of the highlights that were implemented over the 48
hours of the Dash:

  * Simple plugin system for adding games with their own turn
    arguments, template, JavaScript and CSS files.
  * Initial games implemented are simple versions of Roulette and
    Craps.
  * Real-time avatars, controlled by arrow keys - walk around
    the game room and bash into your friends.
  * Authentication by Twitter or Facebook - profile photo is then
    used as the head of your avatar.
  * Chat system - talk to other avatars, messages are displayed
    above each avatar in real-time.
  * Gambling! Each user starts with $5000 and can bet against
    each game, simply drag chips onto a game to bet.
  * Interface is almost entirely CSS - chips use 3D transforms and
    dashed borders.

Game Engine
===========

Games plug straight into Gamblor and consist of a handful of interfaces,
the primary one being the ``core.game.Game`` base class:

  * ``Game.Form`` - defines the form class for the game, allowing
    arguments to be passed into each turn.
  * ``Game.bet`` - handles each person betting, and any args provided
    by the game's form.
  * ``Game.turn`` - implements the rules for a turn of the game.
  * ``Game.outcome`` - called at the end of each turn for each player,
    with their betting args passed in, and returns a value to multiply
    their bet by, which would be zero for a loss.

Other interfaces for each game are:

  * ``templates/games/<game-name>.html`` - template that renders the
    game visibly.
  * ``static/css/games/<game-name>.css`` - stylesheet for the game.
  * ``static/js/games/<game-name>.cjs`` - any JavaScript for the game,
    that can implement custom game effects, as well as betting handlers
    for the game.

TODO
====

As a one-man team for the first time in three years, this year was
particularly gruelling! Here's a list of things I wanted to do, but
fell short of time:

  * Show chips dropped onto games.
  * Add collision detection between avatars.
  * Show actual amounts won and loss to all users.
  * Show players who are in a particular game.
  * Implement all the rules for Roulette and Craps.
  * Let users drag chips onto each other to share money.
  * Provide ways of getting more money (share on Twitter, random handouts).
  * Sound effects!
  * Walking animations for avatars.
  * Animated dice for Craps.

