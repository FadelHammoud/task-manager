from enum import Enum

# define Enum for task categories
class TaskCategory(Enum):
    PERSONAL = 'Personal'
    WORK = 'Work'
    SHOPPING = 'Shopping'
    OTHER = 'Other'

# define Enum for task priorities
class TaskPriority(Enum):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'