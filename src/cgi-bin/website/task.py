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
            self.__task_setError('9')       # If there is a SQLALchemy error return false, that an exception can be returned with the index '10'
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
                tasks       = TaskList.query.filter_by(task_owner=user_id, assigned_to_project_id=project_id,  task_status=category_id).all()
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
            self.__task_setError('9')      # If there is a SQLALchemy error return false, that an exception can be returned with the index '10'
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
            self.__task_setError('10')          # If there is a SQLALchemy error return false, that an exception can be returned with the index '10'
            return False
        else:
            self.__task_setResult(output)
            return True
        finally:
            self.__task_setCountResult(count)



    # donet
    def task_getTaskById(self, user_id, task_id):
        """
        A task with the given ID should be found and returned

        Args:
			id (Integer) : ID of the user, to which task is assigned to
			id (Integer) : ID of the Task, which is searched

        Raises:
            NoResultFound: [description]
            MultipleResultsFound: [description]

        Returns:
			Integer : Returns the Task with the searched ID
        """

        try:
            count = TaskList.query.filter_by(id=task_id, task_owner=user_id).count()

            if count <= 0:
                raise NoResultFound

            if count > 1:
                raise MultipleResultsFound

            elif count == 1:
                task        = TaskList.query.filter_by(id=task_id, task_owner=user_id).one
                task_schema = TaskSchema(many=True)
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
            self.__task_setError('10') #If there is a SQLALchemy error return false, that an exception can be returned with the index '10'
            return False
        else:
            self.__task_setResult(output)
            return True
        finally:
            self.__task_setCountResult(count)





    def task_createTask(self, user_id, project_id, task):
        """
        A new task will be created.

        Args:
			task ([String]) : Class Task with all arguments on order to create a new entry

        Returns:
			[Boolean] : Returns true if the task was created successfully
        """

        try:
            date_object_end = datetime.strptime(task['task-end-date'], "%Y-%m-%d").date()
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


        

    def task_updateTaskById(self, id, Task):
        try:
            doi = datetime.now()
            update_task = TaskList.query.filter_by(taak_id=id).update(dict(project_id = Task['project-id'], task_owner = Task['owner'], task_description = Task['description'], task_status = Task['status'], task_terminator = Task['terminator']))
            db.session.commit()
        
        except NoResultFound:
            db.session.rollback()
            self.__task_setError('1')
            return False
        except IntegrityError:
            db.session.rollback()
            self.__task_setError('2')
            return False
        except CompileError:
            db.session.rollback()
            self.__task_setError('3')
            return False
        except DBAPIError:
            db.session.rollback()
            self.__task_setError('4')
            return False
        except InternalError:
            db.session.rollback()
            self.__task_setError('5')
            return False
        except MultipleResultsFound:
            db.session.rollback()
            self.__task_setError('6')
            return False
        except NoReferencedTableError:
            db.session.rollback()
            self.__task_setError('7')
            return False
        except ObjectNotExecutableError:
            db.session.rollback()
            self.__task_setError('8')
            return False
        # except PendingRollBackError:
        #     db.session.rollback()
        #     self.__task_setError('9')
        #     return False
        except SQLAlchemyError:
            db.session.rollback()
            self.__task_setError('9')
            return False
        else:
            self.__task_setResult(Task)
            return True
        

    def task_updateTaskStatusById(self, id, Task):
        try:
            update_task_status = TaskList.query.filter_by(task_id=id).update(task_status = Task['status'])
            db.session.commit()
        except NoResultFound:
            db.session.rollback()
            self.__task_setError('1')
            return False
        except IntegrityError:
            db.session.rollback()
            self.__task_setError('2')
            return False
        except CompileError:
            db.session.rollback()
            self.__task_setError('3')
            return False
        except DBAPIError:
            db.session.rollback()
            self.__task_setError('4')
            return False
        except InternalError:
            db.session.rollback()
            self.__task_setError('5')
            return False
        except MultipleResultsFound:
            db.session.rollback()
            self.__task_setError('6')
            return False
        except NoReferencedTableError:
            db.session.rollback()
            self.__task_setError('7')
            return False
        except ObjectNotExecutableError:
            db.session.rollback()
            self.__task_setError('8')
            return False
        # except PendingRollBackError:
        #     db.session.rollback()
        #     self.__task_setError('9')
        #     return False
        except SQLAlchemyError:
            db.session.rollback()
            self.__task_setError('9')
            return False
        else:
            self.__task_setResult(Task)
            return True


    def task_deleteTaskById(self, id):
        try:
            delete_task = TaskList(task_id = id)
            db.session.delete(delete_task)
            db.session.commit()
        except NoResultFound:
            db.session.rollback()
            self.__task_setError('1')
            return False
        except IntegrityError:
            db.session.rollback()
            self.__task_setError('2')
            return False
        except CompileError:
            db.session.rollback()
            self.__task_setError('3')
            return False
        except DBAPIError:
            db.session.rollback()
            self.__task_setError('4')
            return False
        except InternalError:
            db.session.rollback()
            self.__task_setError('5')
            return False
        except MultipleResultsFound:
            db.session.rollback()
            self.__task_setError('6')
            return False
        except NoReferencedTableError:
            db.session.rollback()
            self.__task_setError('7')
            return False
        except ObjectNotExecutableError:
            db.session.rollback()
            self.__task_setError('8')
            return False
        # except PendingRollBackError:
            # db.session.rollback()
            # self.__task_setError('9')
            # return False
        except SQLAlchemyError:
            db.session.rollback()
            self.__task_setError('9')
            return False
        else:
            self.__task_setResult()
            return True

    def task_getNumberOfTaskWhereStatusFinished(self, email, project_name):
        try:
            count_task_finished = select(TaskList.task_status).where(TaskList.task_status == "Finished")
            len(count_task_finished)
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
            self.__task_setResult()
            return True

    def task_getNumberOfTaskWhereStatusInProgress(self, email, project_name):
        try:
            count_task_in_progress = select(TaskList.task_status).where(TaskList.task_status == "In Progress")
            len(count_task_in_progress)
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
            self.__task_setResult()
            return True

    def task_getNumberOfTaskWhereStatusRecieved(self, email, project_name):
        try:
            count_task_recieved = select(TaskList.task_status).where(TaskList.task_status == "Recieved")
            len(count_task_recieved)
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
            self.__task_setResult()
            return True












# from enum import unique
# import flask
# from flask.app import Flask
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm.query import Query
# from sqlalchemy.sql.elements import False_
# from sqlalchemy.sql.expression import table
# from sqlalchemy.sql.sqltypes import Float, String
# from sqlalchemy.exc import CompileError, SQLAlchemyError, IntegrityError
# from sqlalchemy.orm.exc import NoResultFound
# from website.models import TaskList
# from website import db


# class Task():
#     def __init__(self):
#         self.__error = None
#         self.__result = None

#     def __task_setError(self, args):
#         self.__error = args

#     def __task_getError(self):
#         return self.__error
    
#     def __task_setResult(self, args):
#         self.__result = args

#     def __task_getResult(self):
#         return self.__result

#     Error = property(__task_getError)
#     Result = property(__task_getResult)



#     def task_getAllTasks(self):
#         try:
#             tasks = TaskList.query.all()

#         except NoResultFound:
#             self.__task_setError('2')
#             return False

#         except CompileError
#             self.__task_setError('3')


#         except Exception:
#             pass


#         except SQLAlchemyError:
#             pass
#         else:
#             self.__task_setResult(tasks)
#             return True
        

#     def task_getAllTasksByUsername(self, username):
#         pass




#     # def task_getAllTasksByCompany(self, company):
#     #     pass




#     def task_getAllTasksByUsernameGroup(self, username, group):
#         pass




#     def task_getAllTasksByUsernameProject(self, username, project_name):
#         pass


#     def task_getNumberOfTasksWhereStatusFinished(self, email, project_name):
#         try:
#             task = Query(status='finished')
            
#         except NoResultFound:
#             self.__task_setError('1')
#             return False
#         else:
#             self.__task_setResult(task)
#             return True

#     def task_getTaskByID(self, id):
#         try:
#             task = TaskList.query.get(id)
            
#         except NoResultFound:
#             self.__task_setError('1')
#             return False
#         else:
#             self.__task_setResult(task)
#             return True




#     def task_createTask(self, task):
#         try:
#             task = TaskList(project_id = task['project-id'], task_owner = task['owner'], task_description = task['description'], task_status = task['status'], task_terminator = task['terminator'], data_of_issue = '22/12/2021')
#             db.session.add(task)
#             db.session.commit()

#         except IntegrityError:
#             db.session.rollback()
#             self.__task_setError()
#             return False

#         # except PendingRollbackError()

#         else: 
#             self.__task_setResult()
#             return True
        



#     def task_updateTaskById(self, id):
#         pass
        



#     def task_deleteTaskById(self, id):
#         try:
#             delete_task = TaskList(id = id)
#             db.session.delete(delete_task)
#             db.session.commit()
#         except:
#             db.session.rollback()
#             self.__task_setError()
#             return False
#         else:
#             self.__task_setResult()
#             return True


        
# '''
# app = Flask(__name__)

# db = SQLAlchemy(app)

# app.config['SQLALCHEMY_TRACK_MODIFIKATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'Platzhalter'

# class tasks(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     task_id = db.Column(db.Integer(16), unique=True)
#     name = db.Column(db.String(150))
#     project_id = db.Column(db.Integer(16))
#     describtion = db.Column(db.String(500))
#     timeline = db.Column(db.Float(150)) # vlt berechnet?
#     status = db.Column(db.String(20))
#     owner = db.Coloumn(db.String(150))
#     date_of_issue = db.Column(db.String(50))
#     final_date = db.Column(db.String(50))
# '''

# def create_task():
#         task = TaskList(name = "Task_1", timeline= 2.25, status = "Angefangen", owner = "User1")
#         db.session.add(task)
#         db.session.commit()
#         return "Task was created successfully"

# def update_status(self, id):
#         Update_status = TaskList(status = "Erledigt")
#         db.session.refresh(Update_status) # .update gibt es nicht
#         db.session.commit()
#         return "Task status was upated successfully"

# def delete_task(id):
#         Delete_task = TaskList(id = 1)
#         db.session.delete(Delete_task)
#         db.session.commit()
#         return "Task" + id + "was deleted successfully"

# def update_timeline(id):
#         Update_timeline = TaskList(timeline = 2.5)
#         db.session.refresh(Update_timeline)
#         db.session.commit()
#         return "Timeline was updated successfully"

# def change_owner(id):
#         change = TaskList(owner = "Neuer Owner")
#         db.session.refresh(change)
#         db.session.commit()
#         return "Owner was changed sucessfully"

# def change_decribtion(id):
#         new_describtion = TaskList(descibtion = "Neue Beschreibung")
#         db.session.refresh(new_describtion)
#         db.session.commit()
#         return "Describtion of task" + id + "was changed sucessfully"

# def change_finale_date(id):
#         new_finale_date = TaskList(final_date = "28.03.2021")
#         db.session.refresh(new_finale_date)
#         db.session.commit()
#         return "Final Date was changed sucessfully"
