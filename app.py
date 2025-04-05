from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bucketlist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Goal model
class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'category': self.category,
            'completed': self.completed
        }

# Create the database tables
with app.app_context():
    db.create_all()

# Get all goals by category
@app.route('/goals/<category>', methods=['GET'])
def get_goals(category):
    goals = Goal.query.filter_by(category=category).all()
    return jsonify([goal.to_dict() for goal in goals])

# Add a new goal
@app.route('/goal', methods=['POST'])
def add_goal():
    data = request.get_json()
    new_goal = Goal(text=data['text'], category=data['category'])
    db.session.add(new_goal)
    db.session.commit()
    return jsonify(new_goal.to_dict())

# Toggle completion status of a goal
@app.route('/goal/<int:goal_id>', methods=['PUT'])
def toggle_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    goal.completed = not goal.completed
    db.session.commit()
    return jsonify(goal.to_dict())

# Delete a goal
@app.route('/goal/<int:goal_id>', methods=['DELETE'])
def delete_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    db.session.delete(goal)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)


