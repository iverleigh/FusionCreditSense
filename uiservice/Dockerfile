# Stage 1 - Set up the base container
FROM node:13.7.0-alpine3.11 as node
WORKDIR /usr/src/app
COPY package*.json /usr/src/app/
RUN npm install
COPY . /usr/src/app/
EXPOSE 4200 49153
CMD npm run start