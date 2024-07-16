FROM python
LABEL author="Owain Jones <github.com/erinaceous>"
ENTRYPOINT [ "fastapi",  "run", "--port", "80", "/app/api.py" ]
WORKDIR /app
RUN useradd -d /app -m user && chown -R user:user /app
COPY ./requirements.txt /tmp/
RUN pip install --upgrade pip && pip install --upgrade -r /tmp/requirements.txt
COPY ./src/meds_tracker /app/
RUN find -type f -name '*.py' | xargs python -m py_compile
USER user