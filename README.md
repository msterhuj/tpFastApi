# tpFastApi

## Deploy env

Create a `.env` file in the root of the project with the following content:

```shell
DATABASE_URL=sqlite:///./test.db
```

## Run the project

```shell
docker compose up
```

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
- [ ] 1 point: web interface with framework of your choice
- [x] 1 point: Store password hashed
- [ ] 1 point: Documentation for how to set up the project
- [ ] 1 point: Use real database (PostgresSQL, MySQL) and not SQLite