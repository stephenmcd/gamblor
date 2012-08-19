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

TODO
====

  * Show chips dropped onto games.
  * Add collision detection between avatars.
  * Show actual amounts won and loss to all users.
  * Show players who are in a particular game.
  * Implement all the rules for Roulette and Craps.
  * Let users drag chips onto each other to share money.
  * Provide ways of getting more money (share on Twitter, random handouts).
  * Sound effects!
  * Walking animations for avatars.
