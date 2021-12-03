from . import ma
from .model import *

class UserSchema(ma.Schema):
    class Meta:
        model = UserList
        fields = ("id", "firstname", "lastname", "email", "image_file", "pwd", "date_of_issue")

class TaskSchema(ma.Schema):
    class Meta:
        # model = TaskList()
        fields = ("id", "task_id", "project_id", "task_owner", "task_name", "task_description", "task_status", "task_terminator", "date_of_issue")

class ProjectSchema(ma.Schema):
    class Meta:
        model = ProjectList
        fields = ("id", "project_owner", "project_description", "project_start_date", "project_terminator", "date_of_issue")


