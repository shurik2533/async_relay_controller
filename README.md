# async_relay_controller

## Run
`sudo python3 run.py`

## Run as a service
`sudo apt-get install supervisor`

Create a config file for your daemon at `/etc/supervisor/conf.d/async_relay_controller.conf`

```
[program:async_relay_controller]
[program:async_relay_controller]
directory=/home/pi/async_relay_controller
command=sudo python3 run.py
autostart=true
autorestart=true
stderr_logfile=/home/pi/async_relay_controller/logs/supervisor.err.log
stdout_logfile=/home/pi/async_relay_controller/logs/supervisor.out.log
stdout_logfile_maxbytes=0
```

Restart supervisor to load your async_relay_controller.conf`
```
sudo supervisorctl update
sudo supervisorctl restart async_relay_controller
```
