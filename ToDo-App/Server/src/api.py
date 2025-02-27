from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
#from bson.objectid import ObjectId

# Initialize Flask app
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://ColePhilips:MongoDBDragon22!@monsterhunterdb.3kgwi.mongodb.net/ToDo?retryWrites=true&w=majority&appName=MonsterHunterDB"  # MongoDB URI
CORS(app)
mongo = PyMongo(app)

# Check if mongo is initialized
if mongo is None:
    print("MongoDB connection failed!")
else:
    print("MongoDB connection established.")

api = Api(app)

# Swagger for API documentation
swaggerui_blueprint = get_swaggerui_blueprint('/swagger', '/static/swagger.json', config={'app_name': "TODO List"})
app.register_blueprint(swaggerui_blueprint, url_prefix='/swagger')

class Task(Resource):
    # Create: POST /Tasks
    def post(self):
        data = request.get_json()
        task_description = data.get("Task")
        insert_id = data.get("id")
        
        if not task_description:
            return {"message": "Task description is required!"}, 400
        
        # Insert task into the database
        task = {
            "id": insert_id,
            "Task": task_description
        }
        mongo.db.Tasks.insert_one(task)
        
        return jsonify({
            "id": insert_id,
            "Task": task_description
        })

    # Read: GET /Tasks or GET /Tasks/<id>
    def get(self, task_id=None):
        if task_id is None:
            # Fetch all tasks
            tasks = mongo.db.Tasks.find()
            result = []
            for task in tasks:
                result.append({"id": task["id"], "Task": task["Task"]})
            return jsonify(result)
        else:
            # Fetch a specific task by ID
            task = mongo.db.Tasks.find_one({"id": int(task_id)})
            if not task:
                return {"message": "Task not found"}, 404
            return jsonify({"id": task["id"], "Task": task["Task"]})

    # Update: PUT /Tasks/<id>
    def put(self, task_id):
        data = request.get_json()
        task_description = data.get("Task")

        if not task_description:
            return {"message": "Task description is required!"}, 400
        
        result = mongo.db.Tasks.update_one(
            {"id": int(task_id)},
            {"$set": {"Task": task_description}}
        )
        
        if result.matched_count == 0:
            return {"message": "Task not found!"}, 404
        
        return jsonify({
            "id": task_id,
            "Task": task_description
        })

    # Delete: DELETE /Tasks/<id>
    def delete(self, task_id):
        result = mongo.db.Tasks.delete_one({"id": int(task_id)})
        if result.deleted_count == 0:
            return {"message": "Task not found!"}, 404
        return {"message": "Task deleted successfully!"}, 200
    
class Monster(Resource):
    # Read: GET /Monsters
    def get(self):
        # Fetch all monsters from the mhw_db database
        monsters = mongo.cx['mhw_db']['monsters'].find()
        result = []
        for monster in monsters:
            result.append({"id": monster.get("id"), "name": monster.get("name")})  # Adjust based on your monster document structure
        return jsonify(result)

# Set up the routes for the Task and Monster resources
api.add_resource(Task, "/Tasks", "/Tasks/<string:task_id>")
api.add_resource(Monster, "/Monsters")  # New route for monsters

if __name__ == "__main__":
    app.run(port=5000, debug=True)