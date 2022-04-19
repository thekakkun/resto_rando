# Resto Rando

This is the capstone project completed for [Udacity's Full Stack Web Developer Nanodegree Program](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044).

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
- `new`: If the `new` parameter is provided, only return restaurants not yet visited.

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
  "new": true,
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
