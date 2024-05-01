# tpFastApi

## Deploy env

Create a `.env` file in the root of the project with the following content:

```shell
MYSQL_ROOT_PASSWORD=root
MYSQL_DATABASE=fastapi
MYSQL_USER=fastapi
MYSQL_PASSWORD=fastapi
DB_URI=mysql+pymysql://fastapi:fastapi@mariadb:3306/fastapi
```

You can change the values or customize the values on docker compose file

## Run the project

```shell
# start the project
docker compose up -d

# in some cases, the database is not ready when the api is starting
# you can restart the api container
docker compose restart api

# Create the first admin user or update user password and set admin role
docker compose exec api python -m app [username]
```

You can now access the api at `http://localhost:8081`
Docs are available at `http://localhost:8081/docs`

## Work asked by the teacher

- Database (SQLModel)
- The app need to be scalable in container
- Query and Reply with json and http protocol
- No external lib other than FastAPI and SQLModel

### Features 15 points

#### Authentication Endpoint 5 points

- [x] User can log in (basic auth, user login on every request)
- [x] User can register
- [x] User can log out (we use basic auth, so we can just forget the user)
- [x] Add role user and admin
- [x] Create bootstrap script to create first admin user

#### Syslog Endpoint 5 points

- [x] Add user authentication to the endpoint
- [x] Create endpoint to
  - [x] Push log with severity
  - [x] Query log with filter on severity
- [x] Logs have datetime, ip / dns, severity, service, message

#### Admin Endpoint 5 points

These endpoints are only accessible by admin users

- [x] Add admin authentication to the endpoint
- [x] can update logs
- [x] can delete logs

### Bonus 5 points

- [ ] 1 point: api test with postman
- [ ] 1 point: web interface with framework of your choice (waaa la flemme)
- [x] 1 point: Store password hashed
- [x] 1 point: Documentation for how to set up the project
- [x] 1 point: Use real database (PostgresSQL, MySQL) and not SQLite