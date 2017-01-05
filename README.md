# gocd-information-radiator
An information radiator for Thoughtworks Go


## Setup

This is quite a good explaination of what's going on here
https://www.digitalocean.com/community/tutorials/how-to-deploy-python-wsgi-applications-using-uwsgi-web-server-with-nginx

Install some stuff

$ sudo pip install uwsgi
$ brew install nginx

Add config to nginx.conf:

```
server {
   listen 8080;

   location ^~ /  {
        root /Users/DTAYLOR/Development/gocd-radiator/ui;
   }

   location /script/ {  
        include            uwsgi_params;
        uwsgi_pass         uwsgicluster;
        proxy_redirect     off;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Host $server_name;
    }
}
```

Note that the nginx (web) server runs on 8080 and forwards requests to /script/* to the WSGI server running 8081. So there are two servers running!

Run the WSGI server

$ uwsgi --socket 127.0.0.1:8081 --py-autoreload 3 -w wsgi


