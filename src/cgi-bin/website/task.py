"""
    author : Lukas Jager
    date   : 04.12.2021
    license: private
"""
#module and library imports   
from datetime import date, datetime

# "internal" imports
from . import db
from .model import TaskList
from .modelMetaData import TaskSchema

# imports for Errorhandling
from sqlalchemy.orm.exc import NoResultFound            # 1 errorcode
from sqlalchemy.exc import IntegrityError               # 2
from sqlalchemy.exc import CompileError                 # 3
from sqlalchemy.exc import DBAPIError                   # 4
from sqlalchemy.exc import InternalError                # 5
from sqlalchemy.orm.exc import MultipleResultsFound     # 6
from sqlalchemy.exc import NoReferencedTableError       # 7
from sqlalchemy.exc import ObjectNotExecutableError     # 8
from sqlalchemy.exc import SQLAlchemyError              # 9



class Task(): #Initialzing the Class 'Task'
    """
    This class serves to create, delete and update tasks.
    Also it's purpose is to query the database to get data which will be shown to the user.
        
    This class contains the following variables :
        * __task      : to save an errorcode
        * __result    : to save a record set
        * __num_result: an integer to save a number of records (when using count()) #Ich denke dass Count einen int zurückgibt

    It contains the following methods
        * task_getAllTasks
        * task_getAllTasksByUsername
        * task_getAllTasksByUsernameGroup
        * task_getAllTasksByUsernameProject
        * task_getAllTasksByUsernameProject
        * task_getTaskByID
        * task_createTask
        * task_updateTaskById
        * task_updateTaskStatusById
        * task_deleteTaskById
        * task_getNumberOfTaskWhereStatusFinished
        * task_getNumberOfTaskWhereStatusInProgress
        * task_getNumberOfTaskWhereStatusRecieved	
    """


    def __init__(self):
        """
        In this function the variables 'error' and 'result' are initialized in order to store and get information out of those if needed.
        """
        self.__error      = None
        self.__num_result = None
        self.__result     = None



    def __task_setError(self, args):
        """
        In this function an error can be set, if error handling is needed

        Args:
            args (Interger): Stores a number for the specific error event, which will be lated interpretd by the API
        """
        self.__error = args

    def __task_getError(self):
        """
        In this function an error can be pulled, in order to get the relevant error informations

        Returns:
            Integer: The getter method is returning the error itself, with all information
        """
        return self.__error
    



    def __task_setResult(self, args):
        """
        In this function a result can be set

        Args:
            args (Any): Contains an array, list, number, string or JSON Object which can get accessed from without the Class by using properites
        """
        self.__result = args

    def __task_getResult(self):
        """
        In this function a Result can be pulled, in order to get relevant information

        Returns:
            Integer: The getter method is returning the result itself, with all information
        """
        return self.__result



    def __task_setCountResult(self, args):
        """
        In this function, the number of all affected rows/ entries will be stored, that are affected on db access and writing or querying process

        Args:
            args (Interger): Contains the number of affercted or retrurned rows
        """
        self.__num_result = args

    def __task_getCountResult(self):
        """
        This function cann be pulled, in order to get the relevant information about the amount of effected rows 

        Returns:
            Integer: Returns the amount of affected rows
        """
        return self.__num_result


    # Properties
    Error     = property(__task_getError)
    Result    = property(__task_getResult)
    NumResult = property(__task_getCountResult)


    # donet
    def task_getAllTasks(self):
        """
        This method is used to receive all tasks that are stored in the database

        Raises:
            NoResultFound: If there will be no entries it will raise an NoResultFound Error

        Returns:
            JSON Object: A JSON list with lots of objects will be set to the setter methode 
        """


        try:
            count = TaskList.query.count()                                  # Counting the items in the list
            if count <= 0:
                raise NoResultFound                                         # If nothing is found an exception is returned back

            elif count > 0:
                tasks       = TaskList.query.all()
                task_schema = TaskSchema(many=True)
                output      = task_schema.dump(tasks)                       # If something is found, then return the values in the given schema

        except NoResultFound:
            self.__task_setError('1')
            return False
        except IntegrityError:
            self.__task_setError('2')
            return False
        except CompileError:
            self.__task_setError('3')
            return False
        except DBAPIError:
            self.__task_setError('4')
            return False
        except InternalError:
            self.__task_setError('5')
            return False
        except MultipleResultsFound:
            self.__task_setError('6')
            return False
        except NoReferencedTableError:
            self.__task_setError('7')
            return False
        except ObjectNotExecutableError:
            self.__task_setError('8')
            return False
        except SQLAlchemyError:
            self.__task_setError('9')
            return False
        else:
            self.__task_setResult(output)
            return True
        finally:
            self.__task_setCountResult(count)
        


    # donet
    def task_getAllTasksByUsername(self, username):
        """
        All tasks which are related to the current user, should be listed

		Args:
			username (String) : Name of the user, which is currently in the session

		Returns:
			Integer : Returns the amount of tasks, which are related to the current user.
        """

        try:
            count = TaskList.query.filter_by(task_owner = username).count()

            if count <= 0:
                raise NoResultFound

            elif count > 0:
                tasks       = TaskList.query.filter_by(task_owner = username).all()
                task_schema = TaskSchema(many=True)
                output      = task_schema.dump(tasks)

        except NoResultFound:
            self.__task_setError('1')       # If no Result is found return false, that an exception can be returned with the index '1'
            return False
        except IntegrityError:
            self.__task_setError('2')       # If there is an Integrity Error return false, that an exception can be returned with the index '2'
            return False
        except CompileError:
            self.__task_setError('3')       # If there is a compile error return false, that an exception can be returned with the index '3'
            return False
        except DBAPIError:
            self.__task_setError('4')       # If there is a API error of the DB (not Supported error) then this error is returned with the index '4'
            return False
        except InternalError:
            self.__task_setError('5')       # If there is an internal error return false, that an exception can be returned with the index '5'
            return False
        except MultipleResultsFound:
            self.__task_setError('6')       # If there are multiple possible results found return false, that an exception can be returned with the index '6'
            return False
        except NoReferencedTableError:
            self.__task_setError('7')       # If there is no table to reference to return false, that an exception can be returned with the index '7'
            return False
        except ObjectNotExecutableError:
            self.__task_setError('8')       # If the object can't be processed return false, that an exception can be returned with the index '8'
            return False
        except SQLAlchemyError:
            self.__task_setError('9')       # If there is a SQLALchemy error return false, that an exception can be returned with the index '9'
            return False
        else:
            self.__task_setResult(output)
            return True
        finally:
            self.__task_setCountResult(count)


    # donet
    def task_getAllTasksByUsernameGroup(self, user_id, project_id, category_id):
        """
        All Tasks, which are related to the group of the current user, should get listed

        Args:
			username (String) : Name of the user, which is currently in the session
			group (String) : The group of the current user

        Raises:
            NoResultFound: If no results are returned by the database this method will raise a NoResultFound Exception

        Returns:
			Integer : Returns the amount of tasks, which are related to the group of the current user.
        """

        try:
            count = TaskList.query.filter_by(task_owner=user_id, assigned_to_project_id=project_id,  task_status=category_id).count()

            if count <= 0:
                raise NoResultFound

            elif count > 0:
                tasks       = TaskList.query.filter_by(task_owner=user_id, assigned_to_project_id=project_id, task_status=category_id).all()
                task_schema = TaskSchema(many=True)
                output      = task_schema.dump(tasks)

        except NoResultFound:
            self.__task_setError('1')       # If no Result is found return false, that an exception can be returned with the index '1'
            return False
        except IntegrityError:
            self.__task_setError('2')       # If there is an Integrity Error return false, that an exception can be returned with the index '2'
            return False
        except CompileError:
            self.__task_setError('3')       # If there is a compile error return false, that an exception can be returned with the index '3'
            return False
        except DBAPIError:
            self.__task_setError('4')       # If there is a API error of the DB (not Supported error) then this error is returned with the index '4'
            return False
        except InternalError:
            self.__task_setError('5')       # If there is an internal error return false, that an exception can be returned with the index '5'
            return False
        except MultipleResultsFound:
            self.__task_setError('6')       # If there are multiple possible results found return false, that an exception can be returned with the index '6'
            return False
        except NoReferencedTableError:
            self.__task_setError('7')       # If there is no table to reference to return false, that an exception can be returned with the index '7'
            return False
        except ObjectNotExecutableError:
            self.__task_setError('8')       # If the object can't be processed return false, that an exception can be returned with the index '8'
            return False
        except SQLAlchemyError:
            self.__task_setError('9')      # If there is a SQLALchemy error return false, that an exception can be returned with the index '9'
            return False
        else:
            self.__task_setResult(output)
            return True
        finally:
            self.__task_setCountResult(count)



    # donet
    def task_getAllTasksByUsernameProject(self, username, project_name):
        
        """
        The tasks, which are related to the current user and their current project should be listed.

        Args:
			username ([String]) : Name of the user, which is currently in the session
			project_name ([String]) : Name of the project, to which the tasks are related

        Raises:
            NoResultFound: [description]
            NoResultFound: [description]
            MultipleResultsFound: [description]

        Returns:
			[Integer] : Returns the amount of tasks, which are related to the current user and the specific project.
        """

        try:
            count = TaskList.query.filter_by(task_owner=username, assigned_to_project_id=project_name).count()

            if count <= 0:
                raise NoResultFound

            elif count > 0:
                tasks = TaskList.query.filter_by(task_owner=username, assigned_to_project_id=project_name).all()
                task_schema = TaskSchema(many=True)
                output = task_schema.dump(tasks)

        except NoResultFound:
            self.__task_setError('1')           # If no Result is found return false, that an exception can be returned with the index '1'
            return False
        except IntegrityError:
            self.__task_setError('2')           # If there is an Integrity Error return false, that an exception can be returned with the index '2'
            return False
        except CompileError:
            self.__task_setError('3')           # If there is a compile error return false, that an exception can be returned with the index '3'
            return False
        except DBAPIError:
            self.__task_setError('4')           # If there is a API error of the DB (not Supported error) then this error is returned with the index '4'
            return False
        except InternalError:
            self.__task_setError('5')           # If there is an internal error return false, that an exception can be returned with the index '5'
            return False
        except MultipleResultsFound:
            self.__task_setError('6')           # If there are multiple possible results found return false, that an exception can be returned with the index '6'
            return False
        except NoReferencedTableError:
            self.__task_setError('7')           # If there is no table to reference to return false, that an exception can be returned with the index '7'
            return False
        except ObjectNotExecutableError:
            self.__task_setError('8')           # If the object can't be processed return false, that an exception can be returned with the index '8'
            return False
        except SQLAlchemyError:
            self.__task_setError('9')          # If there is a SQLALchemy error return false, that an exception can be returned with the index '9'
            return False
        else:
            self.__task_setResult(output)
            return True
        finally:
            self.__task_setCountResult(count)



    # donet
    def task_getTaskById(self, user_id, task_id, project_id):
        """
        A task with the given ID should be found and returned

        Args:
			user_id (Integer) : ID of the user, to which task is assigned to
			task_id (Integer) : ID of the Task, which is searched
			project_id (Integer) : ID of the Project, which is searched

        Raises:
            NoResultFound: [description]
            MultipleResultsFound: [description]

        Returns:
			Integer : Returns the Task with the searched ID
        """

        try:
            count = TaskList.query.filter_by(id=task_id, task_owner=user_id, assigned_to_project_id=project_id).count()

            if count <= 0:
                raise NoResultFound

            if count > 1:
                raise MultipleResultsFound

            elif count == 1:
                task        = TaskList.query.filter_by(id=task_id, task_owner=user_id, assigned_to_project_id=project_id).one()
                task_schema = TaskSchema(many=False)
                output      = task_schema.dump(task)
            
        except NoResultFound:
            self.__task_setError('1') #If no Result is found return false, that an exception can be returned with the index '1'
            return False
        except IntegrityError:
            self.__task_setError('2') #If there is an Integrity Error return false, that an exception can be returned with the index '2'
            return False
        except CompileError:
            self.__task_setError('3') #If there is a compile error return false, that an exception can be returned with the index '3'
            return False
        except DBAPIError:
            self.__task_setError('4') #If there is a API error of the DB (not Supported error) then this error is returned with the index '4'
            return False
        except InternalError:
            self.__task_setError('5') #If there is an internal error return false, that an exception can be returned with the index '5'
            return False
        except MultipleResultsFound:
            self.__task_setError('6') #If there are multiple possible results found return false, that an exception can be returned with the index '6'
            return False
        except NoReferencedTableError:
            self.__task_setError('7') #If there is no table to reference to return false, that an exception can be returned with the index '7'
            return False
        except ObjectNotExecutableError:
            self.__task_setError('8') #If the object can't be processed return false, that an exception can be returned with the index '8'
            return False
        except SQLAlchemyError:
            self.__task_setError('9') #If there is a SQLALchemy error return false, that an exception can be returned with the index '9'
            return False
        else:
            self.__task_setResult(output)
            return True
        finally:
            self.__task_setCountResult(count)




    # donet
    def task_createTask(self, user_id, project_id, task):
        """
        A new task will be created.

        Args:
			task ([String]) : Class Task with all arguments on order to create a new entry

        Returns:
			[Boolean] : Returns true if the task was created successfully
        """
        try: 
            date_object_end = datetime.strptime(str(task['task-end-date']), "%Y-%m-%d").date()
            task            = TaskList(task_owner=user_id, assigned_to_project_id=project_id, task_title=task['task-title'], task_description=task['task-description'], task_status=task['task-status'], task_terminator=date_object_end)
            db.session.add(task)
            db.session.commit()

            task_schema = TaskSchema()
            output      = task_schema.dump(task)

        except NoResultFound:
            db.session.rollback()
            self.__task_setError('1')   # If no Result is found return false, that an exception can be returned with the index '1'
            return False
        except IntegrityError:
            db.session.rollback()
            self.__task_setError('2')   # If there is an Integrity Error return false, that an exception can be returned with the index '2'
            return False
        except CompileError:
            db.session.rollback()
            self.__task_setError('3')   # If there is a compile error return false, that an exception can be returned with the index '3'
            return False
        except DBAPIError:
            db.session.rollback()
            self.__task_setError('4')   # If there is a API error of the DB (not Supported error) then this error is returned with the index '4'
            return False
        except InternalError:
            db.session.rollback()
            self.__task_setError('5')   # If there is an internal error return false, that an exception can be returned with the index '5'
            return False
        except MultipleResultsFound:
            db.session.rollback()
            self.__task_setError('6')   # If there are multiple possible results found return false, that an exception can be returned with the index '6'
            return False
        except NoReferencedTableError:
            db.session.rollback()
            self.__task_setError('7')   # If there is no table to reference to return false, that an exception can be returned with the index '7'
            return False
        except ObjectNotExecutableError:
            db.session.rollback()
            self.__task_setError('8')   # If the object can't be processed return false, that an exception can be returned with the index '8'
            return False
        except SQLAlchemyError:
            db.session.rollback()
            self.__task_setError('9')   # If there is a SQLALchemy error return false, that an exception can be returned with the index '9'
            return False
        else:
            self.__task_setResult(output)
            return True


        
    # donet
    def task_updateTaskById(self, user_id, task_id, project_id, task):
        """
        A task with a specific ID should get updated

        Args:
			task_id ([Integer]) : ID of the entry, which should get updated
			task ([String]) : Class Task with all arguments on order to update an entry

        Returns:
			[Boolean] : Returns true if the task was updated successfully
        """

        try:
            last_modified   = datetime.now()
            date_object_end = datetime.strptime(str(task['task-end-date']), "%Y-%m-%d").date()
            update_task     = TaskList.query.filter_by(task_owner=user_id, id=task_id, assigned_to_project_id=project_id ).update(dict(task_title=task['task-title'], task_description=task['task-description'], task_status=task['task-status'], task_terminator=date_object_end, last_modified=last_modified))
            db.session.commit()
        
        except NoResultFound:
            db.session.rollback()
            self.__task_setError('1')   # If no Result is found return false, that an exception can be returned with the index '1'
            return False
        except IntegrityError:
            db.session.rollback()
            self.__task_setError('2')   # If there is an Integrity Error return false, that an exception can be returned with the index '2'
            return False
        except CompileError:
            db.session.rollback()
            self.__task_setError('3')   # If there is a compile error return false, that an exception can be returned with the index '3'
            return False
        except DBAPIError:
            db.session.rollback()
            self.__task_setError('4')   # If there is a API error of the DB (not Supported error) then this error is returned with the index '4'
            return False
        except InternalError:
            db.session.rollback()
            self.__task_setError('5')   # If there is an internal error return false, that an exception can be returned with the index '5'
            return False
        except MultipleResultsFound:
            db.session.rollback()
            self.__task_setError('6')   # If there are multiple possible results found return false, that an exception can be returned with the index '6'
            return False
        except NoReferencedTableError:
            db.session.rollback()
            self.__task_setError('7')   # If there is no table to reference to return false, that an exception can be returned with the index '7'
            return False
        except ObjectNotExecutableError:
            db.session.rollback()
            self.__task_setError('8')   # If the object can't be processed return false, that an exception can be returned with the index '8'
            return False
        except SQLAlchemyError:
            db.session.rollback()
            self.__task_setError('9')   # If there is a SQLALchemy error return false, that an exception can be returned with the index '9'
            return False
        else:
            self.__task_setResult(update_task)
            return True
        
    # donet
    def task_updateTaskStatusById(self, user_id, task_id, task):
        """
        The Tasks status should get updated. The task is specified with a given ID

        Args:
			id ([Integer]) : ID of the entry, which should get updated
			task ([String]) : Class Task with all arguments on order to update an entries status

        Returns:
			[Boolean] : Returns true if the task was updated successfully
        """

        try:
            # update_task_status = TaskList.query.filter_by(task_owner=user_id, id=task_id).update(task_status=args['task-status'])
            last_modified = datetime.now()
            update_task   = TaskList.query.filter_by(task_owner=user_id, id=task_id).update(dict(task_status=task['task-status'], last_modified=last_modified))
            db.session.commit()

        except NoResultFound:
            db.session.rollback()
            self.__task_setError('1')   # If no Result is found return false, that an exception can be returned with the index '1'
            return False
        except IntegrityError:
            db.session.rollback()
            self.__task_setError('2')   # If there is an Integrity Error return false, that an exception can be returned with the index '2'
            return False
        except CompileError:
            db.session.rollback()
            self.__task_setError('3')   # If there is a compile error return false, that an exception can be returned with the index '3'
            return False
        except DBAPIError:
            db.session.rollback()
            self.__task_setError('4')   # If there is a API error of the DB (not Supported error) then this error is returned with the index '4'
            return False
        except InternalError:
            db.session.rollback()
            self.__task_setError('5')   # If there is an internal error return false, that an exception can be returned with the index '5'
            return False
        except MultipleResultsFound:
            db.session.rollback()
            self.__task_setError('6')   # If there are multiple possible results found return false, that an exception can be returned with the index '6'
            return False
        except NoReferencedTableError:
            db.session.rollback()
            self.__task_setError('7')   # If there is no table to reference to return false, that an exception can be returned with the index '7'
            return False
        except ObjectNotExecutableError:
            db.session.rollback()
            self.__task_setError('8')   # If the object can't be processed return false, that an exception can be returned with the index '8'
            return False
        # except SQLAlchemyError:
        #     db.session.rollback()
        #     self.__task_setError('9')   # If there is a SQLALchemy error return false, that an exception can be returned with the index '9'
        #     return False
        else:
            self.__task_setResult(update_task)
            return True


    # donet
    def task_deleteTaskById(self, user_id, task_id, project_id):
        """
        A given Task should get deleted

        Args:
			id (Integer) : ID of the entry, which should get deleted

        Returns:
			Boolean : Returns true if the task was deleted successfully
        """

        try:
            delete_task = TaskList.query.filter_by(id=task_id, task_owner=user_id, assigned_to_project_id=project_id).one()
            db.session.delete(delete_task)
            db.session.commit()

        except NoResultFound:
            db.session.rollback()
            self.__task_setError('1')   # If no Result is found return false, that an exception can be returned with the index '1'
            return False
        except IntegrityError:
            db.session.rollback()
            self.__task_setError('2')   # If there is an Integrity Error return false, that an exception can be returned with the index '2'
            return False
        except CompileError:
            db.session.rollback()
            self.__task_setError('3')   # If there is a compile error return false, that an exception can be returned with the index '3'
            return False
        except DBAPIError:
            db.session.rollback()
            self.__task_setError('4')   # If there is a API error of the DB (not Supported error) then this error is returned with the index '4'
            return False
        except InternalError:
            db.session.rollback()
            self.__task_setError('5')   # If there is an internal error return false, that an exception can be returned with the index '5'
            return False
        except MultipleResultsFound:
            db.session.rollback()
            self.__task_setError('6')   # If there are multiple possible results found return false, that an exception can be returned with the index '6'
            return False
        except NoReferencedTableError:
            db.session.rollback()
            self.__task_setError('7')   # If there is no table to reference to return false, that an exception can be returned with the index '7'
            return False
        except ObjectNotExecutableError:
            db.session.rollback()
            self.__task_setError('8')   # If the object can't be processed return false, that an exception can be returned with the index '8'
            return False
        except SQLAlchemyError:
            db.session.rollback()
            self.__task_setError('9')   # If there is a SQLALchemy error return false, that an exception can be returned with the index '9'
            return False
        else:
            return True



    def task_getNumberofTasksWhereStatus(self, user_id, task_status, project_id=None):
        """
        Count all tasks in the DB that have the given task_status

        Args:
			user_id (Interger)  : Contains User-Id to identify all projects that belongs to the loged in user
			task_status (String): Contains Task-Status to identify all projects that have this task_status that is given
			project_id (Integer): Contains Project-Id to filte result and only select entries with the same task_status in a specific Project. If it is None, all Projects with the status of this users will be counted

        Returns:
			Integer : Returns the amount of tasks with the status `Finished`
        """

        try:
            if project_id != None:
                num_result = TaskList.query.filter_by(task_owner=user_id, task_status=task_status, assigned_to_project_id=project_id).count()
            elif project_id == None:
                num_result = TaskList.query.filter_by(task_owner=user_id, task_status=task_status).count()
            else:
                raise NoResultFound


        except NoResultFound:
            self.__task_setError('1') #If no Result is found return false, that an exception can be returned with the index '1'
            return False
        except IntegrityError:
            self.__task_setError('2') #If there is an Integrity Error return false, that an exception can be returned with the index '2'
            return False
        except CompileError:
            self.__task_setError('3') #If there is a compile error return false, that an exception can be returned with the index '3'
            return False
        except DBAPIError:
            self.__task_setError('4') #If there is a API error of the DB (not Supported error) then this error is returned with the index '4'
            return False
        except InternalError:
            self.__task_setError('5') #If there is an internal error return false, that an exception can be returned with the index '5'
            return False
        except MultipleResultsFound:
            self.__task_setError('6') #If there are multiple possible results found return false, that an exception can be returned with the index '6'
            return False
        except NoReferencedTableError:
            self.__task_setError('7') #If there is no table to reference to return false, that an exception can be returned with the index '7'
            return False
        except ObjectNotExecutableError:
            self.__task_setError('8') #If the object can't be processed return false, that an exception can be returned with the index '8'
            return False
        except SQLAlchemyError:
            self.__task_setError('9') #If there is a SQLALchemy error return false, that an exception can be returned with the index '9'
            return False
        else:
            self.__task_setResult(num_result)
            return True
