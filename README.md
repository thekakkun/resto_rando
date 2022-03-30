# Resto Rando

## API Documentation

### Endpoints

#### `GET /api/categories`

Get the list of categories.

##### Example

`curl -X Get URL/api/categories`

##### Returns

```json
{
  "success": true,
  "categories": {
    "0": "African"
  }
}
```

#### `GET /api/restaurants`

The the full list of restaurants.

##### Example

```
curl -X Get URL/api/restaurants \
    --header "Authorization: Bearer {access token}"
```

##### Returns

```json
{
  "success": true,
  "category": null,
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

#### `GET /api/categories/{category_id}/restaurants`

Get the list of restaurants belonging to a category.

##### Example

```
curl -X Get URL/api/categories/0/restaurants \
    --header "Authorization: Bearer {access token}"
```

##### Returns

```json
{
  "success": true,
  "category": "African",
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

#### `POST /api/restaurants`

Add a new restaurant to the database.

##### Example

```
curl -X POST URL/api/restaurants \
    --header "Authorization: Bearer {access token}" \
    --header "Content-Type: application/json" \
    --data '{"name":"Foo Foods","address":"123 Pacific Drive, Los Angeles, CA","categories":["Asian", "Fast Food"],"visited":false}'
```

###### Parameters

```json
{
  "name": "Foo Foods",
  "address": "123 Pacific Drive, Los Angeles, CA",
  "categories": ["Asian", "Fast Food"],
  "visited": false
}
```

- name\* (string): Name of the restaurant
- address\* (string): Restaurant location
- category\* (list): Caterogies that match the restaurant
- visited (boolean): Whether this restaurant has been visited

##### Returns

```json
{
  "success": true,
  "category": null,
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

#### `PATCH /api/restaurants/{restaurant_id}`

Edit a restaurant in the database.

##### Example

```
curl -X PATCH URL/api/restaurants/2 \
    --header "Authorization: Bearer {access token}" \
    --header "Content-Type: application/json" \
    --data '{"visited": true}'
```

###### Parameters

```json
{
  "visited": true
}
```

- name (string): Name of the restaurant
- address (string): Restaurant location
- category (list): Caterogies that match the restaurant
- visited (boolean): Whether this restaurant has been visited

##### Returns

```json
{
  "success": true,
  "category": null,
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

#### `DELETE /api/restaurants/{restaurant_id}`

Delete a restaurant in the dtabase.

##### Example

```
curl -X DELETE URL/api/restaurants/{0} \
    --header "Authorization: Bearer {access token}"
```

##### Returns

```json
{
  "success": true,
  "category": null,
  "restaurants" [
      {
          "name": "Best Restaurant",
          "address": "123 Main Street, New York, NY",
          "categories": [
              "African",
              "Vegan"
          ],
          "visited": true
      },
  ]
}
```

#### `POST /api/random/`

Get a random restaurant from the database. Results can be restricted by category and visited status.

##### Example

```
curl -X POST URL/api/restaurants \
    --header "Authorization: Bearer {access token}" \
    --header "Content-Type: application/json" \
    --data '{"category": ["Asian", "Fast Food"],"visited": true}'
```

###### Parameters

```json
{
  "category": ["Asian"]
}
```

- category (list): Select random restaurant from category
- visited (boolean): Filter restaurant by visited status

##### Returns

```json
{
  "success": true,
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
