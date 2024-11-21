IoT Challenge. [Gabriel Tecnology](https://github.com/gabriel-tecnologia), 2024.

<p align="center">
    <img src="assets/images/grafismo_gabriel.png" width="256">
</p>

<h1 align="center">
    IoT Challenge
</h1>

This is an API project that consumes data from an edge sensor, i.e., non-responsive. To this end, this application optimizes the delivery of data available for access as well as facilitates the consultation of available records.

See more about this case on the [challenge template](https://github.com/eusouagabriel/iot-challenge).

## Getting Started

Run application containers by executing:
```sh
docker compose up --build
```

## Routes

For more information, see the API documentation available at [localhost:5001/docs](http://localhost:5001/docs)

### GET `/records/?{query}`

#### Query Params

For more details, see the [schema file](client_container/schema/GET_Records_query.json).

##### Read by period

- `reference_start`: `Datetime` iso-formated string of start reference period of time;
- `reference_end`: `Datetime` iso-formated string of end reference period of time.

##### Read by date

- `reference_date`: `Date` iso-formated string of reference date.

#### Response
```json
[
    {
        "record_id": 0,
        "start_time": "2023-11-21T00:00:00",
        "end_time": "2023-11-21T00:05:00",
        "size": 0,
        "record_type": "NormalRecord",
        "disk_event": "EVENT0",
    }
]
```

### GET `/records/year/{year}`

#### Response
```json
[
    {
        "record_id": 0,
        "start_time": "2023-11-21T00:00:00",
        "end_time": "2023-11-21T00:05:00",
        "size": 0,
        "record_type": "NormalRecord",
        "disk_event": "EVENT0",
    }
]
```

### GET `/records/year/{year}/month/{month}`

#### Response
```json
[
    {
        "record_id": 0,
        "start_time": "2023-11-21T00:00:00",
        "end_time": "2023-11-21T00:05:00",
        "size": 0,
        "record_type": "NormalRecord",
        "disk_event": "EVENT0",
    }
]
```

### GET `/records/year/{year}/month/{month}/day/{day}`

#### Response
```json
[
    {
        "record_id": 0,
        "start_time": "2023-11-21T00:00:00",
        "end_time": "2023-11-21T00:05:00",
        "size": 0,
        "record_type": "NormalRecord",
        "disk_event": "EVENT0",
    }
]
```

## License

This project is [MIT licensed](https://github.com/FelixLuciano/gabriel-iot-challenge/blob/main/LICENSE).
