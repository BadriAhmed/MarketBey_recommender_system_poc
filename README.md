# Marklocallyrecommender_system_poc

On startup the application will train the recommendation system model.
in order to do so

## Installation and running localy

create a virtual env, then run the following command
```bash
pip install -r requirements.txt
```
then run the main.py


## Running on Docker

On the project directory, Build the docker image via
```
docker build -t MarketBey_recommender .
```

Run and bind port 8000 to the one of your choice:

```
docker run -p 8000:8000 --name MarketBey_recommender_container MarketBey_recommender
```
