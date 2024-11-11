FROM node:18

WORKDIR /usr/src/app

COPY . .

RUN npm install

ENV PORT=3000 MONGODB_APP_ID="application-mflix-yqrpksi"

EXPOSE 3000

CMD ["node", "src/server.js"]