server {
    listen 80;
    server_name yourdomain.com www.http://notcheapnot2expensive.com/;

    location / {
        proxy_pass http://localhost:8080;  # Address of your application server
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/static/files;  # Path to your static files
        expires 30d;
    }

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}