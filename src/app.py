import sys
from datetime import date

from flask import Flask, abort, request
from flask_restful import Api, Resource, reqparse, inputs, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

# Create the Flask api
app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

# Global variables
EVENT_NON_EXISTENT = "The event doesn't exist!"

# Initialize the database connection
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Configure the database
resource_fields = {
    'id': fields.Integer,
    'event': fields.String,
    'date': fields.DateTime(dt_format='iso8601')
}

# Add parser arguments
parser.add_argument(
    'date',
    type=inputs.date,
    help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
    required=True
)

parser.add_argument(
    'event',
    type=str,
    help="The event name is required!",
    required=True
)


# Database model
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)


# Methods for handling the /event endpoint
class EventResource(Resource):
    def post(self):
        args = parser.parse_args()
        event = args['event']
        date = args['date'].date()

        # Save the new event to the database
        new_event = Event(event=event, date=date)
        db.session.add(new_event)
        db.session.commit()

        response = {
            "message": "The event has been added!",
            "event": f"{event}",
            "date": f"{date}"
        }

        return response, 200

    @marshal_with(resource_fields)
    def get(self):
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        if start_time and end_time:
            events = Event.query.filter(Event.date >= start_time). \
                filter(Event.date <= end_time).all()
            if len(events) < 1:
                abort(404, {"message": EVENT_NON_EXISTENT})
            return events
        return Event.query.all()


# Methods for handling the /event/today endpoint
class EventTodayResource(Resource):
    @marshal_with(resource_fields)
    def get(self):
        return Event.query.filter(Event.date == date.today()).all()


# Methods for handling the /event/<id> endpoint
class EventByIdResource(Resource):
    @marshal_with(resource_fields)
    def get(self, id):
        event = Event.query.filter(Event.id == id).first()
        if not event:
            abort(404, EVENT_NON_EXISTENT)
        return event, 200

    def put(self, id):
        args = parser.parse_args()
        event = Event.query.filter(Event.id == id).first()

        if not event:
            abort(404, EVENT_NON_EXISTENT)

        event.event = f"{args['event']}"
        event.date = args['date'].date()
        db.session.commit()

        return {"message": "The event has been updated"}, 201

    def delete(self, id):
        event = Event.query.filter(Event.id == id).first()
        if not event:
            abort(404, EVENT_NON_EXISTENT)
        Event.query.filter_by(id=id).delete()
        db.session.commit()
        return {"message": "The event has been deleted!"}, 204


# Create database tables
db.create_all()

# Register the resource classes
api.add_resource(EventResource, "/api/event")
api.add_resource(EventTodayResource, "/api/event/today")
api.add_resource(EventByIdResource, '/api/event/<int:id>')

# Run the app
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
