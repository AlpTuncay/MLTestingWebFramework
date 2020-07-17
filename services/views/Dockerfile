FROM node:13.6.0-alpine

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

ENV PATH /app/node_modules/.bin:$PATH

COPY package.json /usr/src/app/package.json
COPY package-lock.json /usr/src/app/package-lock.json

RUN npm ci
RUN npm install react-scripts@3.3.0 -g --silent

ADD src /usr/src/app/src
ADD public /usr/src/app/public

CMD ["npm", "start"]
