IoT Challenge. [Gabriel Tecnology](https://github.com/gabriel-tecnologia), 2024.

<p align="center">
    <img src="assets/images/grafismo_gabriel.png" width="256">
</p>

<h1 align="center">
    IoT Challenge
</h1>

## Getting Started

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


## Project case

`camera_container` directory contains an application with a couple of routes simulating an API used to access stored video metadata from a specific model of security camera.

Your task is to create an application that consumes this API and aggregates the data it provides. The camera API is quite verbose and slow, so it's beneficial to group the data for faster future access while consuming less bandwidth.

The new API should be able to respond about the camera's stored videos, filtering for start time, end time and video type.

The expected outcome of this challenge is a well-documented, tested, and efficient application (including both the new API and the `camera_container` app). Additionally, it is recommended to create a Docker Compose configuration that integrates both applications.

### Additional Data:
```
record_type:
    NormalRecord: 0x1
    AlarmRecord: 0x2
    MotionRecord: 0x4
```

## License

This project is [MIT licensed](https://github.com/FelixLuciano/gabriel-iot-challenge/blob/main/LICENSE).
