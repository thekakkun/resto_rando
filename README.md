# Resto Rando

Create a database of restaurants you have visited or are interested in visiting. Search through your list of restaurants, or just get one by random to mix things up.

This is the capstone project completed for [Udacity's Full Stack Web Developer Nanodegree Program](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044).

## Try it out

1. Visit the URL below to get your login link (Resto Rando uses Auth0 as the authentication platform.)  
  <https://resto-rando.herokuapp.com/auth/login>

2. It should automatically redirect to <https://resto-rando.herokuapp.com/auth/result>, which will display your access token.

3. Continue below for API endpoint reference.

## Getting Started

### Dependencies

- [Python 3](https://www.python.org/)
  - [Flask](https://flask.palletsprojects.com/en/2.1.x/): Flask is a lightweight web application framework, used to implement the requests and responses for the API.
  - [SQLAlchemy](https://www.sqlalchemy.org/): SQLAlchemy is used as the ORM to interface with the PosggreSQL database.
- [PostgreSQL 12](https://www.postgresql.org/)
- [Auth0](https://auth0.com/): Auth0 is used as the authentication and authorization service.

### Installing required python packages

Run the following command in the root folder of the project to install the required python packages.

```bash
pip install -r requirements.txt
```

### Initiating the database

1. Create a database using the PostgreSQL CLI.

    ```bash
    createdb resto_rando
    ```

2. Initiate and migrate the database.

    ```bash
    flask db upgrade
    ```

### Running the application

1. The necessary credentials to run the project are provided in the setup.sh file.

    ```bash
    source setup.sh
    ```

    To run the application on a local development environment, the additional environment variables are necessary.

    ```bash
    export FLASK_APP=flaskr
    export FLASK_ENV=development
    ```

2. Run the following command to start the local development server

    ```bash
    flask run
    ```

### Hosting the application on Heroku

1. Create an app in Heroku Cloud. This requires a [Heroku](https://www.heroku.com/) account and the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) to be installed on your machine.

    ```bash
    heroku create resto-rando --buildpack heroku/python
    ```

2. Add PostgreSQL addon for the database

    ```bash
    heroku addons:create heroku-postgresql:hobby-dev --app resto-rando
    ```

3. Specify the required environment variables through the [Heroku Dashboard](https://dashboard.heroku.com/) settings.

    - `API_AUDIENCE`
    - `AUTH0_DOMAIN`
    - `CLIENT_ID`
    - `FLASK_APP`
    - `REDIRECT_URI`

4. Push the application files to Heroku. It will be built on Heroku automatically.

    ```bash
    git push heroku main
    ```

## Authentication

### Scopes

#### User

- `get:my_resto`: Get data on restaurants added by you.
- `post:resto`: Add restaurant.
- `patch:my_resto`: Edit data for restaurants added by you.
- `delete:my_resto`: Delete restaurants added by you.

#### Admin

All scopes available to user roles +

- `get:any_resto`: Get data on any restaurant, regardless of user.
- `patch:any_resto`: Edit data for any restaurant, regardless of user.
- `delete:any_resto`: Delete any restaurant, regardless of user.

## API Documentation

### Error Handling

Erros are returned in the following format:

```json
{
  "succcess": false,
  "error": 404,
  "message": "The server cannot find the requested resource."
}
```

Some common errors:

- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not found
- `405`: Method not allowed
- `422`: Request unprocessable

### Endpoints

#### Authentication

##### `GET /auth/login`

Get the login url.

###### Permissions required

None.

###### Example requests

```bash
curl -X GET https://resto-rando.herokuapp.com/auth/login
```

###### Example responses

```json
{
  "url": "https://dev-2m33ryh3.us.auth0.com/authorize?audience=resto&response_type=token&client_id=yIpSovVjw5kDcpACpbPDQ9Fekb8khROU&redirect_uri=https://resto-rando.herokuapp.com/auth/results"
}
```

##### `GET /auth/logout`

Get the logout url.

###### Permissions required

None.

###### Example requests

```bash
curl -X GET https://resto-rando.herokuapp.com/auth/logout
```

###### Example responses

```json
{
  "url": "https://dev-2m33ryh3.us.auth0.com/logout"
}
```

##### `GET /auth/results`

Get your access token. This endpoint is only available using a browser. [Visit the URL here.](https://resto-rando.herokuapp.com/auth/results)

###### Permissions required

None.

#### Categories

##### `GET /api/categories`

Get the list of categories.

###### Permissions required

None.

###### Example requests

```bash
curl -X GET https://resto-rando.herokuapp.com/api/categories
```

###### Example responses

```json
{
  "success": true,
  "categories": {
    "0": "African",
    "1": "Alcohol",
  }
}
```

#### Restaurants

##### `GET /api/restaurants?category={cat}&user={user_id}&page={page}&q={search_term}`

The the list of restaurants added by user.

###### Permissions required

- `get:my_resto`
- `get:any_resto`: Needed to see restaurants added by other users.

###### Query string parameters

- `category` (string): Specify single category to filter by.
- `visited` (boolean): Specify `true` or `false` to only show from restaurants you have / have not visited.
- `user` (int): Show restaurants added by specified user. If unspecified returns restaurant list based on user role
  - Admin: All restaurants, regardless of user.
  - User: Only restaurants added by logged-in user.
- `page` (int): Results are paginated (10 restaurants per page). Set value to display specified page, or defaults to first page if unspecified.
- `q` (string): Keyword to search for. Case insensitive.

###### Example requests

```bash
curl -X GET "https://resto-rando.herokuapp.com/api/restaurants?category=African&page=1" \
    --header "Authorization: Bearer $ACCESS_TOKEN"
```

###### Example responses

```json
{
  "success": true,
  "category": "African",
  "visited": null,
  "count": 5,
  "page": 1,
  "restaurants" [
    {
      "name": "Best Restaurant",
      "address": "123 Main Street, New York, NY",
      "categories": ["African", "Vegan"],
      "visited": true
    },
  ]
}
```

##### `POST /api/restaurants`

Add a new restaurant to the database.

###### Permissions required

- `post:resto`

###### Request body parameters

- `name` (string, required): Name of the restaurant
- `address` (string, required): Restaurant location
- `category` (list, required): Caterogies that match the restaurant
- `visited` (boolean): Whether this restaurant has been visited
- `date_visited` (string): Date visited.
  - `YYYY-MM-DD`: Set date visited, uses ISO 8601 style formatting. Automatically sets `visited` to `true`.
  - `today`: Set date visited to today. Automatically sets `visited` to `true`.
  - `null`: Clears date visited. `visited` value kept as is.

###### Example requests

```bash
curl -X POST https://resto-rando.herokuapp.com/api/restaurants \
    --header "Authorization: Bearer $ACCESS_TOKEN" \
    --header "Content-Type: application/json" \
    --data '{"name":"Foo Foods","address":"123 Pacific Drive, Los Angeles, CA","categories":["Asian", "Fast Food"],"visited":false}'
```

###### Example responses

```json
{
  "success": true,
  "category": null,
  "count": 5,
  "page": 1,
  "restaurants" [
    {
      "name": "Best Restaurant",
      "address": "123 Main Street, New York, NY",
      "categories": ["African", "Vegan"],
      "visited": true
    },
    {
      "name": "Foo Foods",
      "address": "123 Pacific Drive, Los Angeles, CA",
      "categories": ["Asian", "Fast Food"],
      "visited": false
    },
  ]
}
```

##### `PATCH /api/restaurants/{restaurant_id}`

Edit a restaurant in the database.

###### Permissions required

- `patch:my_resto`
- `patch:any_resto`: Needed to edit data on restaurants added by other users.

###### Parameters

- `name` (string): Name of the restaurant
- `address` (string): Restaurant location
- `category` (list): Caterogies that match the restaurant
- `visited` (boolean): Whether this restaurant has been visited
- `date_visited` (string): Date visited.
  - `YYYY-MM-DD`: Set date visited, uses ISO 8601 style formatting. Automatically sets `visited` to `true`.
  - `today`: Set date visited to today. Automatically sets `visited` to `true`.
  - `null`: Clears date visited. `visited` value kept as is.

###### Example requests

```bash
curl -X PATCH https://resto-rando.herokuapp.com/api/restaurants/2 \
    --header "Authorization: Bearer $ACCESS_TOKEN" \
    --header "Content-Type: application/json" \
    --data '{"visited": true, "date_visited": "2020-03-14"}'
```

###### Example responses

```json
{
  "success": true,
  "category": null,
  "count": 5,
  "page": 1,
  "restaurants" [
    {
      "name": "Best Restaurant",
      "address": "123 Main Street, New York, NY",
      "categories": ["African", "Vegan"],
      "visited": true
    },
    {
      "name": "Foo Foods",
      "address": "123 Pacific Drive, Los Angeles, CA",
      "categories": ["Asian", "Fast Food"],
      "visited": true
    },
  ]
}
```

##### `DELETE /api/restaurants/{restaurant_id}`

Delete a restaurant in the database.

###### Permissions required

- `delete:my_resto`
- `delete:any_resto`: Needed to edit data on restaurants added by other users.

###### Example requests

```bash
curl -X DELETE https://resto-rando.herokuapp.com/api/restaurants/0 \
    --header "Authorization: Bearer $ACCESS_TOKEN"
```

###### Example responses

```json
{
  "success": true,
  "category": null,
  "count": 5,
  "page": 1,
  "restaurants" [
    {
      "name": "Best Restaurant",
      "address": "123 Main Street, New York, NY",
      "categories": ["African", "Vegan"],
      "visited": true
    },
  ]
}
```

#### Finding Restaurants

##### `GET /api/random/?category={cat}&new`

Get a random restaurant from the database. Results can be restricted by category and visited status.

###### Permissions required

- `get:my_resto`

###### Query string parameters

- `category` (string): Specify single category. Result must include this category.
- `visited` (boolean): Specify `true` or `false` to only pull from restaurants you have / have not visited.

###### Example requests

```bash
curl -X GET "https://resto-rando.herokuapp.com/api/restaurants?category=Asian&new" \
    --header "Content-Type: application/json" \
    --header "Authorization: Bearer $ACCESS_TOKEN" \
```

###### Example responses

```json
{
  "success": true,
  "category": "Asian",
  "visited": true,
  "restaurants" [
    {
      "name": "Foo Foods",
      "address": "123 Pacific Drive, Los Angeles, CA",
      "categories": ["Asian", "Fast Food"],
      "visited": true
    }
  ]
}
```
