![BeardBot Logo](http://github.com/mossblaser/BeardBot/raw/master/logo.png "BeardBot")

A modular Python IRC bot with an assortment of amusing and useful functions.
Currently at a rather early stage in development.


Usage
-----
    $ python bot.py server.example.com "#channel"
The bot will join the specified room with the name "BeardBot".

Note:
The bot remembers settings etc. on a per-channel basis, this includes the
selection of loaded modules so don't forget to load them!


### Killing the bot
Send "die" in a PM to the bot. (Note: No security for this at present!)


### Loading/Unloading/Listing Modules
Module management must be done via private messages to the bot. The following
commands are available to facilitate this.

*   Load specified module(s).

        modprobe modulename [[modulename] ...]

*   Unload the specified modules   

        rmmod modulename [[modulename] ...]

*   List available modules.

        lsmod

The loaded modules will be remembered on a per-channel basis and the server will
attempt to restart them on subsequent runs.


### Current Modules
The following modules are shipped with BeardBot (hopefully) ready for use.

#### admin
The module that provides an interface to load/unload modules. It will
eventually have some sort of authentication and other features. See the
section on loading/unloading/listing modules above for usage.


#### astersed
Applies corrections made by clients like:
    *correction
Using the most likely word they intended to correct. Only applies
corrections if it is 60% certain of the word to be corrected.

#### beardy
Jonathan Heathcote's `beardy' Markov chain generator. It collects messages
written by users (and will use logs made by the log module if it is loaded)
and produces markov chains which can then be used to generate sentences in
the style of the specified user using either 1st order or 2nd order chains.
Due to the fact most IM messages are short, 1st order messages are
preferable for variety and humour while 2nd order ones tend to be direct
quotations disappointingly often. Usage is as follows (where beardbot is the
name of the bot in the channel):

*   generate a sentence based on the your own messages

        beardbot: what do I sound like?

*   generate a sentence based on someone else's messages

        beardbot: what does username sound like?

*   switch to a 2nd order model

        beardbot: grow your beard

*   switch to a 1st order model

        beardbot: shave your beard
        
#### help
Currently experimental help function which uses docstrings. Awaiting further
work.

#### highscore
Keeps track of the daily high-score of the number of :D emoticons in one
message. Will announce high scores as they occur.
Other commands:
  
*   Reset the highscores

        beardbot: we are all sad

*   Print the leaderboard

        beardbot: who is the happiest of them all?
    
#### hokay
Responds to various classic lines from The End of the World.
    
#### hyphen
Simply corrects users who forget to apply Randal Munroe's translation of
[hyphen](http://xkcd.com/37/)s one-word forwards when used in the form adjective-ass noun.

#### log
A logging feature. Keeps a log of the channel in an sqlite database and
provides access to data to other modules. Also features some querying
features:

*   Report whether a user said anything matching the regular expression
    provided. This function automatically appends .* to the start and end of
    the expression unless you start the regex with a /

        did username say regex.*search

*   As above but not limited to a particular user.

        who said regex.*search

*   Prints out the most recently said things on the channel.

        [in a pm] recent messages

#### nazi
A spelling-nazi function. It will shout at users who misspell words. Note of
warning, this module is bloody annoying. If the spellcheck doesn't know a
word that it should you can correct it when it complains by saying:

    beardbot: yes I [your choice of expletives here] do

#### sed
Provides sed-like regex substitution functionality for messages. Simply
write a sed-like substitution command in a message and beardbot will apply
it to the first of the last five messages that matches the expression. Eg:

    s/some(.*)/all \1/

Add the 'g' flag at the end to replace all occurrences.

#### wtf
An acronym decryption module. For occasions when someone uses an obscure
acronym which you do not know simply say

    wtf is wtf

where the second wtf is your chosen acronym and the module will try to
answer your question. This does require you have an acronym file installed
on your system which appear to be somewhat uncommon.

#### whatthehellguys
Keeps a record of the tone of conversation based on keywords it sees. If the
tone of the conversation drops by 50% in one message it will announce the
tone of conversation.

*   Report the current tone of conversation

        beardbot: what the hell

*   Disable automatic feedback on large drops (default)

        beardbot: don't judge me

*   Enable automatic feedback on large drops

        beardbot: tell me if this goes too far

#### xkcdhighscore
Keeps track of the number of times users post xkcd links. Will print out a
leaderboard on request:

    beardbot: xkcd leader board

Prints out the leaderboard of the number of times users have used xkcd
refrences and provided links.

About
-----
Developed By [Jonathan Heathcote](http://github.com/mossblaser) with significant
architecture contributions and some modules by [Tom Nixon](http://github.com/tomjnixon)
and some disturbing contributions by [James Sandford](http://github.com/j616)

All code GNU GPLv2, no warranties etc. etc.

### The Name
BeardBot is named after the `Beardy' Markov chain generator which inspired it.
Beardy was in turn named in honour of Markov's epic beard.
