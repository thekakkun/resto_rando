# Resto Rando

## API Documentation

### Endpoints

#### `GET /api/cuisines`

##### Example

`curl -X Get URL/api/categories`

##### Returns

```json
{
  "categories": {
    "0": "African"
  }
}
```

#### `GET /api/categories/{cuisine_id}/restaurants`

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
          "categories": [
              "African",
              "Vegan"
          ]
      },
  ]
}
```

#### `GET /api/restaurants`

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
          "categories": [
              "African",
              "Vegan"
          ]
      },
  ]
}
```

#### `POST /api/restaurants`

##### Example

```
curl -X POST URL/api/restaurants \
    --header "Authorization: Bearer {access token}" \
    --header "Content-Type: application/json" \
    --data "{'name': 'Foo Foods','address': '123 Pacific Drive, Los Angeles, CA','category': ['Asian', 'Fast Food'],'visited': true}'
```

###### Parameters

```json
{
  "name": "Foo Foods",
  "address": "123 Pacific Drive, Los Angeles, CA",
  "category": ["Asian", "Fast Food"],
  "visited": true
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
          "categories": [
              "African",
              "Vegan"
          ]
      },
  ]
}
```

#### `DELETE /api/restaurants/{restaurant_id}`

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
          ]
      },
  ]
}
```

#### `POST /api/random/`

##### Example

```
curl -X POST URL/api/restaurants \
    --header "Authorization: Bearer {access token}" \
    --header "Content-Type: application/json" \
    --data "{'category': ['Asian', 'Fast Food'],'visited': true}'
```

###### Parameters

```json
{
  "category": ["Asian", "Fast Food"],
  "visited": true
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
          "name": "Best Restaurant",
          "address": "123 Main Street, New York, NY",
          "categories": [
              "African",
              "Vegan"
          ]
      }
  ]
}
```
