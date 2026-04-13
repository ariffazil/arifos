server {
    listen 80;
    server_name wiki.arif-fazil.com;

    root /var/www/wiki.arif-fazil.com;
    index index.html;

    location / {
        try_files $uri $uri/ $uri.html =404;
    }

    location /docs/ {
        try_files $uri $uri.html =404;
    }
}

server {
    listen 443 ssl;
    server_name wiki.arif-fazil.com;

    ssl_certificate /etc/ssl/certs/arif-fazil.crt;
    ssl_certificate_key /etc/ssl/private/arif-fazil.key;

    root /var/www/wiki.arif-fazil.com;
    index index.html;

    location / {
        try_files $uri $uri/ $uri.html =404;
    }

    location /docs/ {
        try_files $uri $uri.html =404;
    }
}
