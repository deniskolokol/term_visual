# terminal visualizer
terminal visualizer for MOON2 live visuals

WARNING: Despite the fact that the real data from OSCeleton debug log is used, the output doesn't represent it in any meanfingful way. It is made exclusively for creating visual effect of logs running on a background.

Dependencies:

* Python
* tmux


Raspberry Pi display control:
````$ vcgencmd display_power 0````
````$ vcgencmd display_power 1````

Kill tmux server:
````$ tmux kill-server````

Disable screen-server in console:

````
$ apt-get install lightdm
$ nano /etc/lightdm/lightdm.conf
````

in section [Seat:*] add or adjust line to say

````xserver-command=X -s 0 -dpms````