from . import ma
from .model import UserList, ProjectList, TaskList




class UserSchema(ma.Schema):
    """
    This class inherits from the marshmallow class Schema and serves to provide  meta data namely the column names of the users table.
    That is used to create a json format response after querying data from the database.
    The class has a nested class called Meta which contains the column field names.
    """
    class Meta:
        """
        This nested class is used to store the Meta data (meaning column names) of the Table tbl_user_list.
        This class contains the following variables :
            * model (UserList): an instance of the class UserList
            * fields (tuple): an tuple containing the column names of the user table
        """
       
        model = UserList
        fields = ("id", "firstname", "lastname", "email", "image_file", "pwd", "date_of_issue")




class ProjectSchema(ma.Schema):
    """
    This class inherits from the marshmallow class Schema and serves to provide  meta data namely the column names of the project's table.
    That is used to create a json format response after querying data from the database.
    The class has a nested class called Meta which contains the column field names.
    """
    class Meta:
        """
        This nested class is used to store the Meta data (meaning column names) of the Table tbl_project_list.
        This class contains the following variables :
            * model (ProjectList): an instance of the class ProjectList
            * fields (tuple): an tuple containing the column names of Project table
        """
        model = ProjectList
        fields = ("id", "project_owner", "project_title", "project_description", "project_start_date", "project_terminator", "date_of_issue")




class TaskSchema(ma.Schema):
    """
    This class inherits from the marshmallow class Schema and serves to provide  meta data namely the column names of the tasks table.
    That is used to create a json format response after querying data from the database.
    The class has a nested class called Meta which contains the column field names.
    """
    class Meta:
        """This nested class is used to store the Meta data (meaning column names) of the Table tbl_task_list.
            This class contains the following variables :
            * model (TaskList): an instance of the class TaskList
            * fields (tuple): an tuple containing the column names of task table
        """
        model = TaskList()
        fields = ("id", "task_owner", "assigned_to_project_id", "task_title", "task_description", "task_status", "task_terminator", "last_modified", "date_of_issue")

