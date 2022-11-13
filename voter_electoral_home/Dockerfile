FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV APP_HOME=/home/app

RUN apt-get update 
RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils

#download and install chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

#
# # install google chrome
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
# RUN apt-get -y update
# RUN apt-get install -y google-chrome-stable --fix-missing
#
# # install chromedriver
# RUN apt-get install -yqq unzip
# RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
# RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

WORKDIR $APP_HOME

COPY req.txt $APP_HOME
RUN pip install --upgrade pip
RUN pip install -r req.txt

COPY . $APP_HOME
# COPY scripts/keys.json $APP_HOME
RUN ls
# ENV GOOGLE_APPLICATION_CREDENTIALS /home/app/keys.json

# WORKDIR $APP_HOME/voter_electoral_home
# CMD ["python3", "-m", "scripts.voter_portal.scraper"]
# CMD ["python3", "-m", "scripts.mainScraper"]
EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
