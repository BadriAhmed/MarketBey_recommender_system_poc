FROM bitnami/python:3.8.11 as builder
ENV PATH="/app/.venv/bin:${PATH}"
WORKDIR /app
RUN mkdir tmp
RUN python -m venv .venv
RUN /app/.venv/bin/python3 -m pip install --upgrade pip
COPY requirements.txt /app

COPY . /app
RUN  python3 -m pip install -r requirements.txt

FROM bitnami/python:3.8.11-prod
ENV PATH="/app/.venv/bin:${PATH}"
WORKDIR /app

COPY --from=builder /app /app

EXPOSE 8000
CMD ["python","main.py"]