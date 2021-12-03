from . import ma
from .model import UserList, ProjectList, TaskList




class UserSchema(ma.Schema):
    """
    This class serves to provide some meta data such as the culumn names, which is used to crate a json format response after quereing data from the database

    Args:
        * Contains a nested class Meta which contains the column field names
    """
    class Meta:
        """
        This nested class is used to provide the Meta data of the Table tbl_user_list which is used later by flask-marshmallow
        """
        model = UserList
        fields = ("id", "firstname", "lastname", "email", "image_file", "pwd", "date_of_issue")




class ProjectSchema(ma.Schema):
    """
    This class serves to provide some meta data such as the culumn names, which is used to crate a json format response after quereing data from the database

    Args:
        * Contains a nested class Meta which contains the column field names
    """
    class Meta:
        """
        This nested class is used to provide the Meta data of the Table tbl_project_list which is used later by flask-marshmallow
        """
        model = ProjectList
        fields = ("id", "project_owner", "project_title", "project_description", "project_start_date", "project_terminator", "date_of_issue")




class TaskSchema(ma.Schema):
    """
    This class serves to provide some meta data such as the culumn names, which is used to crate a json format response after quereing data from the database

    Args:
        * Contains a nested class Meta which contains the column field names
    """
    class Meta:
        """
        This nested class is used to provide the Meta data of the Table tbl_task_list which is used later by flask-marshmallow
        """
        model = TaskList()
        fields = ("id", "task_owner", "assigned_to_project_id", "task_title", "task_description", "task_status", "task_terminator", "last_modified", "date_of_issue")

