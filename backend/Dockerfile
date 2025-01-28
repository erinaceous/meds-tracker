FROM python:3.12
LABEL author="Owain Jones <github.com/erinaceous>"
ENTRYPOINT [ "fastapi",  "run", "--port", "80", "/app/api.py" ]
WORKDIR /app
EXPOSE 80
RUN useradd -d /app -m user && chown -R user:user /app && mkdir -p /app/data/download && chown -R user:user /app/data
COPY ./requirements.txt /tmp/
#RUN apt-get update -y && apt-get install -y cargo
RUN pip install --upgrade pip && pip install --upgrade -r /tmp/requirements.txt
COPY ./src/meds_tracker /app/
RUN find -type f -name '*.py' | xargs python -m py_compile
#RUN /app/static_db/build.sh && rm -vrf /app/data/download
USER user