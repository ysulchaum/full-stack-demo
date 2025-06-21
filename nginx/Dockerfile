FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Copy SSL certificates
COPY nginx/certs/synthpartner.com.pem /etc/nginx/certs/synthpartner.com.pem
COPY nginx/certs/synthpartner.com.key /etc/nginx/certs/synthpartner.com.key