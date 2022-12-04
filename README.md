# Flask-Web-Calendar

Afraid to miss something interesting? Don't worry, you won't! This app provides a REST service that allows saving events to a database using the Flask framework. You will access the events with the help of REST endpoints.

## Requirements

-   Python3
-   SQLite3
-   Packages from `requirements.txt`

## Installation

1. Clone the repository

```bash
git clone https://github.com/dan-koller/Flask-Web-Calendar
```

2. Create a virtual environment

```bash
python3 -m venv venv
```

3. Install the requirements

```bash
pip install -r requirements.txt
```

4. Run the app

```bash
python3 app.py
```

## Usage

-   [Get today's events](#get-todays-events)
-   [Post a new event](#post-a-new-event)
-   [Get an event by id](#get-an-event-by-id)

## Endpoints

The following examples are using the JSON format.

### Get today's events

_(Only if there are any)_

```
GET /api/event/today
```

Response:

```
{
   "id": "<Integer value, not empty>",
   "event": "<String value, not empty>",
   "date": "<String value, not empty>"
}
```

### Post a new event

```
POST /api/event
{
   "event": "<String value, not empty>",
   "date": "<String value, not empty>"
}
```

Response:

```
{
   "message": "<String value, not empty>",
   "event": "<String value, not empty>",
   "date": "<String value, not empty>"
}
```

### Get an event by id

```
GET /api/event/<id>
```

Response:

```
{
   "id": "<Integer value, not empty>",
   "event": "<String value, not empty>",
   "date": "<String value, not empty>"
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
