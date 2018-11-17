FROM node:8
FROM python:2.7

RUN mkdir -p /usr/src/app 
WORKDIR /usr/src/app 

# Various Python and C/build deps
RUN apt-get update && apt-get install -y \ 
    wget \
    build-essential \ 
    cmake \ 
    git \
    pkg-config \
    python-dev \ 
    python-opencv \ 
    libopencv-dev \ 
    libav-tools  \ 
    libjpeg-dev \ 
    libpng-dev \ 
    libtiff-dev \ 
    libjasper-dev \ 
    libgtk2.0-dev \ 
    python-numpy \ 
    python-pycurl \ 
    libatlas-base-dev \
    gfortran \
    webp \ 
    python-opencv

# Install Open CV - Warning, this takes absolutely forever
RUN cd ~ && git clone https://github.com/Itseez/opencv.git && \ 
    cd opencv && \
    git checkout 3.0.0 && \
    cd ~ && git clone https://github.com/Itseez/opencv_contrib.git && \
    cd opencv_contrib && \
    git checkout 3.0.0 && \
    cd ~/opencv && mkdir -p build && cd build && \
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \ 
    -D INSTALL_C_EXAMPLES=ON \ 
    -D INSTALL_PYTHON_EXAMPLES=ON \ 
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \ 
    -D BUILD_EXAMPLES=OFF .. && \
    make -j4 && \
    make install && \ 
    ldconfig

COPY requirements.txt /usr/src/app/
# install python depencies
RUN pip install numpy
RUN pip install --no-cache-dir -r requirements.txt

# capy package.json
COPY package*.json ./

# install npm packages
RUN npm install
RUN npm i nodemon

# copy everything
COPY . .

# expose the port
EXPOSE 3000
CMD [ "npm", "run", "start" ]
