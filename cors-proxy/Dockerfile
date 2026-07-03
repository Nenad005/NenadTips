FROM node:14

WORKDIR /cors-proxy

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 8000

CMD ["node", "server.js"]