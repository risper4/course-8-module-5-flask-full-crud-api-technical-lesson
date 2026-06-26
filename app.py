from flask import Flask, request, jsonify

app = Flask(__name__)

class Event:
    def __init__(self, title, id):
        self.title = title
        self.id = id

    def to_dict(self) :
        return {'id' : self.id , 'title' : self.title}
    

events = [
    Event(1 , 'Tech Meetup'),
    Event(2, 'Python Workshop')
]

@app.route('/events/<int:id>', methods=['GET'])
def get_event(id) :
    event = next((e for e in events if e.id == id), None)
    return jsonify(event.to_dict()) if event else ('Event not found!')

@app.route('/events', methods=['POST'])
def add_event() :
    data = request.get_json()
    new_id = max((e.id for e in events)) + 1 if events else 1
    new_event = Event(id=new_id, title=data['title'])
    events.append(new_event)
    return jsonify(new_event.to_dict)

@app.route('/events/<int:id>', methods=['PATCH'])
def update_event(id) :
    data = request.get_json()
    event = next((e for e in events if e.id == id), None)
    if not event :
        return ('Event not found', 404)
    if 'title' in data :
        event.title = data['title']
    return jsonify (event.to_dict)

@app.route('/events/<int:id>', methods=['DELETE'])
def delete_event(id) :
    global events
    event = next((e for e in event if e.id == id), None)
    if not event :
        return ('Event not found'), 404
    events = [e for e in events if e.id != id]
    return ('Event deleted successfully', 204)

if __name__ == "__main__":
    app.run(port=5555, debug=True)
