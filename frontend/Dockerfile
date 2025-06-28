FROM node:20-slim

WORKDIR /app

COPY package.json .

RUN npm install

COPY . .

RUN npm run build

# Install a lightweight server to serve the built files
RUN npm install -g serve

# Expose port 3000 for the app
EXPOSE 3000

# Serve the built app
CMD ["serve", "-s", "dist", "-l", "3000"]

