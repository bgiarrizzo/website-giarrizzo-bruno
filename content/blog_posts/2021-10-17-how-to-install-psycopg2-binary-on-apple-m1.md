---
title: "How to install psycopg2-binary on Apple M1"
summary: I had some difficulties working with python code accessing postgres databases. Let me show you how I handled it.
cover: "2021-10-17.png"
cover_alt: "how to install psycopg2-binary on mac m1 article cover"
date: 2021-10-17
tags: [apple, m1, postgres, python3.10, psycopg2, psycopg2-binary, install]
---

Last month I bought to myself an Apple M1, really good computer, with great power, and awesome battery.

My work with it is pretty simple, I code python API, some simple front App with TypeScript/react, trying some Go, learning swift and administrating some kubernetes clusters. Nothing too fancy.

I am trying to work with latest versions of software I use, and in this case, python 3.10.

I installed it with brew, pretty easily : 

<blockquote class="blockquotecode">
    brew install python@3.10
</blockquote>

I had troubles with psycopg2-binary, installing depedencies of one of the projects I work with, the error message i was getting was this one : 

<blockquote class="blockquotecode">
    Error: pg_config executable not found.

pg_config is required to build psycopg2 from source.  Please add the directory
containing pg_config to the $PATH or specify the full executable path with the
option:

    python setup.py build_ext --pg-config /path/to/pg_config build ...

or with the pg_config option in 'setup.cfg'.
</blockquote>

It seems there is some conf file that is missing. I tried to solve it by installing postgres server to get that missing file :

<blockquote class="blockquotecode">
    brew install postgresql@12
</blockquote>

At this point, brew tell me to setup the path to PG in my PATH, this way (using ZSH, it tells me to write it obviously to .zshrc):

<blockquote class="blockquotecode">
    echo 'export PATH="/opt/homebrew/opt/postgresql@12/bin:$PATH"' > ~/.zshrc
</blockquote>

Now i'm all set, and i can install it the way i want :

<blockquote class="blockquotecode">
    pip(3) install psycopg2-binary
</blockquote>

Or in my project repository :

<blockquote class="blockquotecode">
    pipenv install psycopg2-binary
</blockquote>