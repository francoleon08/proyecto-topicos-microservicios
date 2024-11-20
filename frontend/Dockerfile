FROM node:18-alpine as build

WORKDIR /usr/src/app

ARG VITE_URL_MOVIES
ARG VITE_URL_HISTORY

COPY . .

RUN npm install

RUN echo "VITE_URL_MOVIES=$VITE_URL_MOVIES" > .env \
    echo "VITE_URL_HISTORY=$VITE_URL_HISTORY" >> .env

RUN npm run build

FROM nginx:1.23-alpine

COPY --from=build /usr/src/app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
