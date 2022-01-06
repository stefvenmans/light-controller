# Light controller
Light controller to switch lights on/of according to data of the sun-rise/set.

<h1>Auto-launch</h1>
To let the script run at startup:
```
cd light-controller
nano launcher.sh
```

Add the following to the launche file:
```
cd /
cd path_to_repo
sleep
sudo python3 main.py
cd /
```
and save the file.
Make the launcherfile executable:
```
chmod 755 launcher.sh
```
In the home directory create the following folder:
```
mkdir logs
```
Then start crontab and add the following line
```
sudo crontab -e
@reboot sh path_to_launcher/launcher.sh >/home/pi/logs/cronlog 2>&1
```
Done.

<h1>Logging</h1>
The script logs relevant information to a logfile (`logfile.log`). It can be viewed as follow:
<img width="1145" alt="terminal-view" src="https://user-images.githubusercontent.com/15052685/148351573-17ebbc33-a429-4c45-bea1-a02fada239e8.png">
