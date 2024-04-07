Flask Task Manager Application
This is a Flask application that serves as a task manager, allowing users to create, retrieve, update, and delete tasks. It also provides endpoints to retrieve tasks based on priority, category, and due date.

Table of Contents
Installation
Usage
Endpoints
Project Structure
Dependencies
Contributing
License
Installation
Prerequisites
Before you begin, ensure you have the following installed:

Python 3.x
Docker
Docker Compose
Clone the Repository
bash
Copy code
git clone <repository-url>
cd flask-task-manager
Environment Variables
Create a .env file in the root directory of the project and add the following environment variables:

plaintext
Copy code
DB_URL=<database-url>
Build and Run the Docker Container
bash
Copy code
docker-compose up --build flask_app
Usage
Once the Docker container is up and running, you can access the application at http://localhost:5000. Use a tool like Postman to interact with the API endpoints.

Endpoints
GET /test: Test route to check if the server is running.
POST /tasks: Create a new task.
GET /tasks: Get all tasks.
GET /tasks/<id>: Get a task by ID.
PUT /tasks/<id>: Update a task.
DELETE /tasks/<id>: Delete a task.
GET /tasks/priority/<priority>: Get tasks by priority.
GET /tasks/category/<category>: Get tasks by category.
GET /tasks/due/<date>: Get tasks due on a specific date.
For detailed information about each endpoint, refer to the source code documentation.

Project Structure
The project structure is as follows:

bash
Copy code
flask-task-manager/
│
├── app.py               # Main Flask application file
├── interceptor.py       # Interceptor for handling request orders
├── validators.py        # Validators for task creation and update
│
├── Dockerfile           # Dockerfile for building the application image
├── docker-compose.yml   # Docker Compose configuration file
│
├── enums/               # Directory containing task enums
│   └── ...
│
├── README.md            # Project README file
├── requirements.txt     # Python dependencies
└── .env                 # Environment variable file
Dependencies
Flask
Flask-SQLAlchemy
SQLAlchemy-Enums
...
For a complete list of dependencies, refer to the requirements.txt file.

Contributing
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

License
This project is licensed under the MIT License.