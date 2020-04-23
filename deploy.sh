docker login registry.gitlab.com

docker build -t registry.gitlab.com/loyola-monitor/monitor-api .

docker push registry.gitlab.com/loyola-monitor/monitor-api

# docker run --rm --env-file .env.production -p 8888:5000 tmp
