# FROM python3.7
FROM node:8

# Create app directory
WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install
RUN npm i nodemon

COPY . .

EXPOSE 3000
CMD [ "npm", "run", "start" ]
