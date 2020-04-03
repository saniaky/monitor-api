docker run --rm --network host \
  -v "${PWD}/db/migrations:/flyway/sql" \
  flyway/flyway:6.2.0 \
  -url=jdbc:mysql://${MYSQL_HOST}:${MYSQL_PORT}/${MYSQL_DB} \
  -user=${MYSQL_USER} \
  -password=${MYSQL_USER_PASSWORD} \
  migrate
