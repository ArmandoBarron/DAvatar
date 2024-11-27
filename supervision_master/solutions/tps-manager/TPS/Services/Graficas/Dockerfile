FROM python

ADD ./app /app
WORKDIR /app

RUN pip install flask --user 
RUN pip install pandas --user
RUN pip install numpy --user

RUN pip install -r requirements.txt

EXPOSE 7070

ENTRYPOINT [ "python3", "/app/app.py" ]