---
title: "Sudo with macos and TouchID"
summary: I am a lazy guy, and type my password kind of annoy me :-D
cover: 2022-08-03.jpg
cover_alt: "Sudo with macos and TouchID article cover"
publish_date: 2022-08-03T09:30:00Z
update_date: 2022-08-03T09:30:00Z
tags: [macos, sudo, terminal, touch, id, touchid]
---

I’m addicted to home automation. There. Said it. But it’s just such a tremendous amount of fun to play with. I’m pretty sure it’s the SRE in me. Why do anything by hand when you can have computers do things for you? Why turn on the lights when you get home when it can happen automatically? Turn on the lights when you enter the bathroom? Barbaric! Turn them off? I’ve git better things to do! Why not wake up to the smell of freshly brewed coffee every morning instead of having to get out of bed first to turn on the coffee machine?

Last October, i got for myself one M1 Macbook pro.

It is a hell of a machine, powerful, silent and it comes with touchID.

I didn't change my laptop since my mid-2012 macbook pro, and this was a revolution !

I saw one day, one of my coworker edit files with <code>sudo vi</code>, no password typed, just put his finger on touchID pad, I always wanted to do the same, so i configured it.

By default, it is not configured on macos, you have to edit one file : <code>/etc/pam.d/sudo</code>

In this file, you'll find this content :

<pre>
    # sudo: auth account password session
    auth       sufficient     pam_smartcard.so
    auth       required       pam_opendirectory.so
    account    required       pam_permit.so
    password   required       pam_deny.so
    session    required       pam_permit.so
</pre>

I just add the line : <code>auth sufficient pam_tid.so</code> so the file looks like this then :

<pre>
    # sudo: auth account password session
    auth       sufficient     pam_tid.so
    auth       sufficient     pam_smartcard.so
    auth       required       pam_opendirectory.so
    account    required       pam_permit.so
    password   required       pam_deny.so
    session    required       pam_permit.so
</pre>

# Bonus 

On the day you update your mac, the <code>/etc/pam.d/sudo</code> may be overwritten by the update process. And your changes will be lost.

(I know it is one line to add to file, but if you are lazy like me, you will understand :D)

One github user, named [tjluoma](https://github.com/tjluoma) made a little script, named [tjluoma/sudo-via-touch-id](https://github.com/tjluoma/sudo-via-touch-id), that will check if the line is present in your <code>/etc/pam.d/sudo</code>, and will add it if not !

Just like he indicates it on his README :

<pre>
## How to use this

1. Download sudo-via-touch-id.sh
2. Make it executable: `chmod 755 sudo-via-touch-id.sh`
3. Run it: `./sudo-via-touch-id.sh`
4. (Optional But Useful) move it to a directory such as `/usr/local/bin/` 
so you can run it again next time there's an update to macOS.
</pre>

After i installed this script in my <code>/usr/local/bin/</code>, i edited my crontab to run the script each time my laptop is rebooted.

Like this :

<pre>
    @reboot    bash /usr/local/bin/sudo-via-touch-id.sh
</pre>

With this, on each reboot the script will run, and add the missing line to the <code>/etc/pam.d/sudo</code> if update deleted it !
