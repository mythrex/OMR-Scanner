FROM conda/miniconda3

# Various Python and C/build deps
RUN conda install opencv

# install python depencies
RUN pip install --upgrade pip
RUN pip install scipy
RUN pip install imutils

# install NODE
RUN apt-get update -yqq
RUN apt-get install curl build-essential -yqq
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash
RUN apt-get install -yqq nodejs

# change working dir for app
RUN mkdir -p /usr/src/app 
WORKDIR /usr/src/app/

# copy package.json
COPY package*.json /usr/src/app/

# install npm packages
RUN npm install
RUN npm i nodemon

# copy everything
COPY . /usr/src/app/

# expose the port
EXPOSE 3000
CMD [ "npm", "run", "start" ]
