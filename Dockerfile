FROM python:3.11.4
WORKDIR /app                                                                                                                                                             0.5s
COPY requirements.txt /app/                                                                                                                                               0.1s
RUN pip install -r requirements.txt                                                                                                                                     27.1s
COPY . .                                                                                                                                                                 0.6s
RUN sed -i '/from werkzeug.urls import url_decode/d' /app/venv/Lib/site-packages/flask_login/utils.py                                                                    0.4s
RUN sed -i '/from werkzeug.urls import url_encode/d' /app/venv/Lib/site-packages/flask_login/utils.py                                                                    0.5s
RUN sed -i '/from werkzeug.urls import url_decode/d' /usr/local/lib/python3.11/site-packages/flask_login/utils.py                                                        0.7s
RUN sed -i '/from werkzeug.urls import url_encode/d' /usr/local/lib/python3.11/site-packages/flask_login/utils.py
