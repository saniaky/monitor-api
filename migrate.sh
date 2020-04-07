# Load env variables
export $(grep -v '^#' .env | xargs)

docker run --rm --network host \
  -v "${PWD}/db/migrations:/flyway/sql" \
  flyway/flyway:6.2.0 \
  -url=jdbc:mysql://${DB_HOST}:${DB_PORT}/${DB_NAME} \
  -user=${DB_USER} \
  -password=${DB_USER_PASSWORD} \
  migrate
