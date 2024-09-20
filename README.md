# Django Example Project

This project build with django framework, integrate with mysql mongodb redis, ... and dockerize it

## 1. Setup

Make sure these software have been installed on your computers:

- [Python](https://www.python.org/downloads/) 3.12 or newer version
- (Optional) If you are using ubuntu linux, you might have to install mysql client too.

```
    sudo apt-get -y install python-virtualenv mysql-server mysql-client python3 python3-dev python3-pip python-mysqldb libmysqlclient-dev
```

- (Optional) For Mac OSX, make sure you export (run it in your current terminal) these flags before pip install
  ```
      export CFLAGS="-isysroot $(xcrun --show-sdk-path) -I/usr/include -I/usr/local/include/ ${CFLAGS}"
      export LDFLAGS="-isysroot $(xcrun --show-sdk-path) -L/usr/local/lib -L/usr/lib"
      export CPPFLAGS="-isysroot $(xcrun --show-sdk-path) -I/usr/include -L/usr/lib"
  ```

### 1.1. Create python virtual evironment

Follow one of these guide to create python virtual environment corresponding to your operating system.

#### 1.1.1. Linux

```
sudo apt-get install python3-venv    # If needed
python3 -m venv .venv
source .venv/bin/activate
```

#### 1.1.2. MacOS

```
python3 -m venv .venv
source .venv/bin/activate
```

#### 1.1.3.Windows

```
py.exe -3 -m venv .venv
.venv\scripts\activate
```

### 1.2. Install libraries for backend

After activating the python virtual environment, rung this command to install libraries:

```
pip install -r ./requirements.txt
```

### 1.3. Config

copy [.env.sample](.env.sample) to `.env`. Open this file and change the variables values according to your environment.

### 1.4. Migrate data

```
python ./backend/manage.py migrate
```

### 1.5. Run backend

Open source code with Visual Studio -> Chose `Run and Debug` on the left panel -> Click `Start Debuging`
Or open terminal using: python manage.py runserver

## 2. Use docker

If you would like to use docker on your pc. Please following these steps to build and rund docker container locally

- Build and rund docker conatiner:
  ```
  docker-compose up -d --build
  ```
- Stop docker container:
  ```
  docker-compose down
  ```
