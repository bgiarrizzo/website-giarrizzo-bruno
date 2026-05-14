FROM nginx:alpine

# Copy website files to nginx html directory

RUN rm -rf /usr/share/nginx/html/*

# Copy all files and folders from src to nginx html directory
COPY src/ /usr/share/nginx/html/

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]