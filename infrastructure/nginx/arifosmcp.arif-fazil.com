server {
    listen 80;
    server_name arifosmcp.arif-fazil.com;

    root /var/www/arifosmcp;
    index index.html;

    # Serve static HTML for root
    location = / {
        try_files /index.html =404;
    }

    # Proxy /.well-known/* to uvicorn (prefix match — takes precedence)
    location ^~ /.well-known/ {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Proxy API routes to uvicorn
    location ~ ^/(health|mcp|tools|resources|prompts|version|status|ready|discovery|api|a2a|tasks|subscribe|webmcp|widget|dashboard|_next) {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static assets caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}

server {
    listen 443 ssl;
    server_name arifosmcp.arif-fazil.com;

    ssl_certificate /etc/ssl/certs/arif-fazil.crt;
    ssl_certificate_key /etc/ssl/private/arif-fazil.key;

    root /var/www/arifosmcp;
    index index.html;

    # Serve static HTML for root
    location = / {
        try_files /index.html =404;
    }

    # Proxy /.well-known/* to uvicorn (prefix match — takes precedence)
    location ^~ /.well-known/ {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Proxy API routes to uvicorn
    location ~ ^/(health|mcp|tools|resources|prompts|version|status|ready|discovery|api|a2a|tasks|subscribe|webmcp|widget|dashboard|_next) {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static assets caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
