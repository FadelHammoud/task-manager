
## Prerequisites

Before you begin, ensure you have the following installed:

    Python 3.x
    Docker

## Build and Run

1.	Clone the repository:
    
        git clone <repository_url>

2.	Navigate to the project directory: 
    
        cd <project_directory>

3.	Install dependencies:
    
        pip install -r requirements.txt

4.	Set environment variables if necessary under .env file
5.	Run the application:
       
    •   Without Docker:
            
             python app.py

    •   With Docker (recommended): 
        
            docker-compose up --build flask_app

## API Endpoints

there is an postman collection for the APIs named as 'ztask-manager-app.postman_collection.json', within it there is also random test (under tests in postman).

    •	/test (GET): Test route for verifying the application's availability.
    •	/tasks (POST): Create a new task.
    •	/tasks (GET): Get all tasks.
    •	/tasks/<id> (GET): Get a task by ID.
    •	/tasks/<id> (PUT): Update a task.
    •	/tasks/<id> (DELETE): Delete a task.
    •	/tasks/priority/<priority> (GET): Get tasks by priority.
    •	/tasks/category/<category> (GET): Get tasks by category.
    •	/tasks/due/<date> (GET): Get tasks due on a specific date.


## Task Table

    •	id: Integer (Primary Key)
    •	title: String (Unique, Not Null)
    •	description: String (Not Null)
    •	completed: Boolean (Default: False)
    •	priority: Enum (TaskPriority)
    •	category: Enum (TaskCategory)
    •	due_date: Date
