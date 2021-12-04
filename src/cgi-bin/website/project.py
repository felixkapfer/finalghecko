#module and library imports   
from datetime import date, datetime

# "internal" imports
from . import db
from .model import ProjectList
from .modelMetaData import ProjectList, ProjectSchema

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

class Project():
    
    """This class serves to create, delete and update projects.
        Also it's purpose is to query the database to get data which will be shown to the user.
       
       An instance of this class contains the following variables :
        * __error(int): to save an errorcode
        * __result(query object): to save a record set when querying the database
        *__num_result(int): to save a number of records 

       It contains the following methods
        * Get and set methods for the above mentioned variables
        * project_getAllProjects
        * project_getAllProjectsByUser
        * project_getProjectByProjectId
        * project_getNumberOfDaysFromStartToEndByProjectId
        * project_getNumberOfDaysFromStartToTodayByProjectId
        * project_getNumberOfDaysFromTodayToEndByProjectId
        * project_createProject
        * project_deleteProjectByProjectId
        * project_updateProjectbyProjectId
    """

    
    # Constructor 
    def __init__(self):                      
        """Constructor that initializes an instance of the class    
            Arguments: No Arguments   
            Tests:   
                * test if the values are set correctly
                * test if all variables are set
                """
        
        # Instance variables
        self.__result     = None                # to save a result set 
        self.__num_result = None                # to save a number of result sets  
        self.__error      = None                # to save an error code    
       
    
    #Get and Set Methods 
    def __project_getResult(self):
        """This method can be called to get a result set which was previously retrieved from the database.
        Arguments: No Arguments
        Returns:
            result (query object): a from the database retrieved result set         
        """
        return self.__result
       
    def __project_setResult(self, result):
        """This method serves to save the outcome of a query into the class variable __result.  
        Arguments:
            result (query object):  a result set created within a query to the db
        Returns: No return value    
        """
        self.__result= result

    def __project_getNumResult(self): 
        """This method can be called to get a number of projects which was previously retrieved from the database.
        Arguments: No Arguments
        Returns:
            Integer: a number of projects
        """
        return self.__num_result
       
    def __project_setNumResult(self, num_result): 
        """This method serves to save the outcome of a query (regarding a number of projects) into the class variable __num_ result.  
        Arguments:
            num_result (Integer): variable that holds a number of projects
        Returns: No return value  
        """
        self.__num_result= num_result
        
    def __project_getError(self):
        """This method serves to be called to get an errorcode
        Arguments: No Arguments
        Returns:
            error(Integer): the errorcode
            
             # 1  = NoResultFound
             # 2  = Integrity Error 
             # 3  = Compile Error 
             # 4  = DBAPIE Error
             # 5  = Internal Error
             # 6  = MultipleResults Found
             # 7  = No referenced Table Error
             # 8  = Object not Executable
             # 9  = SQLAlchemyError 
        """
        return self.__error
    
    def __project_setError(self, error):
        """This method serves to set an Error Code. It saves it into the error variable.
        Args:
            error (Integer): number for an occured error
        Returns: No return value     
        """
        self.__error = error



    # Property Objects: 
    Error     = property(__project_getError)   
    Result    = property(__project_getResult)
    NumResult = property(__project_getNumResult)
        
    # donet
    # Query Methods for retrieving data    
    def project_getAllProjects(self):
        """This function serves to retrieve all projects from all users from the database. When calling this function ensure admin rights exist.
            The results set containing the projects  is saved into the class variable result.
            Furthermore this function also counts the number of all  projects  in the databse and saves that information into the variable num_result.

        Raises:
            NoResultFound, Integrity Error , Compile Error , DBAPIE Error, Internal Error, MultipleResults Found, 
            No referenced Table Error, Object not Executable, SQLAlchemyError 

        Arguments: No Arguments
        
        Returns:
            Boolean: returns true if the data could be retrieved, returns false if an error occured
            
        Test:
            * test if all projects and their number could be retrieved correctly (also after adding, deleting, updating projects)
            * test if the exceptions are raised when the associated error occurs
            * test if the access to the saved result and num_result works correctly, that it is not overwritten by multipe functioncalls before getting displayed to the user
        """
        
        try:
            num_result = ProjectList.query.count()
            if num_result <= 0:
                raise NoResultFound

            elif num_result > 0:
                projects       = ProjectList.query.all()
                project_schema = ProjectSchema(many=True)
                output         = project_schema.dump(projects)
        
        except NoResultFound:
            self.__project_setError("1")
            db.session.rollback
            return False
        except IntegrityError:
            self.__project_setError("2")
            db.session.rollback
            return False
        except CompileError:
            self.__project_setError("3")
            db.session.rollback
            return False
        except DBAPIError:
            self.__project_setError("4")
            db.session.rollback
            return False
        except InternalError:
            self.__project_setError("5")
            db.session.rollback
            return False
        except MultipleResultsFound:
            self.__project_setError("6")
            db.session.rollback
            return False
        except NoReferencedTableError:
            self.__project_setError("7")
            db.session.rollback
            return False
        except ObjectNotExecutableError:
            self.__project_setError("8")
            db.session.rollback
            return False
        except SQLAlchemyError:
            self.__project_setError("9")
            db.session.rollback
            return False
        else: 
            self.__project_setResult(output)
            return True
        finally:
            self.__project_setNumResult(num_result)   
          


    # donet
    def project_getAllProjectsByUser(self, user_id):
        """This function serves to retrieve all projects of one user from the database. 
            The results set containing the projects  is saved into the class variable result.
            Furthermore this function also counts the number of  projects of that user and saves that information into the variable num_result.

        Raises:
            NoResultFound, Integrity Error , Compile Error , DBAPIE Error, Internal Error, MultipleResults Found, 
            No referenced Table Error, Object not Executable, SQLAlchemyError 

        Arguments:
            * user_id (Integer): the associated user, who owns these projects

        Returns:
            Boolean: returns true if the data could be retrieved, returns false if an error occured
            
        Test:
            * test if the users projects and their number could be identified and retrieved as expected (also after adding, deleting, updating projects)
            * test if the exceptions are raised when the associated error occurs
            * test if the access to the saved result and num_result works correctly
        """
        try:
            num_result = ProjectList.query.filter_by(project_owner=user_id).count()
            if num_result <= 0:
                raise NoResultFound

            elif num_result> 0:
                projects       = ProjectList.query.filter_by(project_owner=user_id).all()
                project_schema = ProjectSchema(many=True)
                output         = project_schema.dump(projects)
           
        except NoResultFound:
            self.__project_setError("1")
            db.session.rollback
            return False
        except IntegrityError:
            self.__project_setError("2")
            db.session.rollback
            return False
        except CompileError:
            self.__project_setError("3")
            db.session.rollback
            return False
        except DBAPIError:
            self.__project_setError("4")
            db.session.rollback
            return False
        except InternalError:
            self.__project_setError("5")
            db.session.rollback
            return False
        except MultipleResultsFound:
            self.__project_setError("6")
            db.session.rollback
            return False
        except NoReferencedTableError:
            self.__project_setError("7")
            db.session.rollback
            return False
        except ObjectNotExecutableError:
            self.__project_setError("8")
            db.session.rollback
            return False
        except SQLAlchemyError:
            self.__project_setError("9")
            db.session.rollback
            return False
        else: 
            self.__project_setResult(output)
            return True
        finally:
            self.__project_setNumResult(num_result) 
        



    # donet
    #Allgemeine Funktionen bzw. User- unabhängig  
    def project_getProjectByProjectId(self, user_id, project_id):
        """This function retrieves a specific project of one specific user from the database by the project id and saves it into the variable result.
            Furthermore this function also saves the number of the  projects  into the variable num_result. Generally this is expected to be 1.
        
        Raises:
            NoResultFound, Integrity Error , Compile Error , DBAPIE Error, Internal Error, MultipleResults Found, 
            No referenced Table Error, Object not Executable, SQLAlchemyError 

        Argument:
            project_id (Integer): The Project's Id
            user_id (Integer): the associated user, who owns this project

        Returns:
            Boolean: returns false if an error occured, returns true if the data could be retrieved
            
        Tests:
            * test the behaviour when the exceptions are raised and the associated error occurs 
                for example give a random integer as the project id and test if no result found exception is raised
            * test if the retreived data were stored in the variables and access to the saved result and num_result works correctly
        """
        try:
            num_result = ProjectList.query.filter_by(id=project_id, project_owner=user_id).count()
            if num_result <= 0:
                raise NoResultFound

            if num_result > 1:
                raise MultipleResultsFound

            elif num_result == 1:
                project        = ProjectList.query.filter_by(id=project_id, project_owner=user_id).all()
                project_schema = ProjectSchema(many=True)
                output         = project_schema.dump(project)
        
        except NoResultFound:
            self.__project_setError("1")
            db.session.rollback
            return False
        except IntegrityError:
            self.__project_setError("2")
            db.session.rollback
            return False
        except CompileError:
            self.__project_setError("3")
            db.session.rollback
            return False
        except DBAPIError:
            self.__project_setError("4")
            db.session.rollback
            return False
        except InternalError:
            self.__project_setError("5")
            db.session.rollback
            return False
        except MultipleResultsFound:
            self.__project_setError("6")
            db.session.rollback
            return False
        except NoReferencedTableError:
            self.__project_setError("7")
            db.session.rollback
            return False
        except ObjectNotExecutableError:
            self.__project_setError("8")
            db.session.rollback
            return False
        except SQLAlchemyError:
            self.__project_setError("9")
            db.session.rollback
            return False
        else: 
            self.__project_setResult(output)
            return True
        finally:
            self.__project_setNumResult(num_result)     

      
      
    # donet
    def project_getNumberOfDaysFromStartToEndByProjectId(self, user_id, project_id): # wird als int zurückgeben oder trotzdem ein Result Set??
        """This function calculates the number of days between a project's start and end date. It saves it into the variable Result
        
        Raises:
            NoResultFound, Integrity Error , Compile Error , DBAPIE Error, Internal Error, MultipleResults Found, 
            No referenced Table Error, Object not Executable, SQLAlchemyError 
        
        Arguments:
            project_id (Integer): a project's id
            user_id (Integer): the associated user, who owns this project
            
        Returns:
            Boolean: returns false if an error occured, returns true if the data could be retrieved and 
            the number of days between a project's start and end date could be calculated
            
         Tests:
            * test the behaviour when the exceptions are raised and the associated error occurs 
            * test if the difference between the dates is calculated correctly in the correct units
            * test what happens if the order or the form of the dates is not as expected
        """
        try: 
            #number_between_start_and_end_of_a_project
            num_result                           = ProjectList.query.filter_by(id=project_id, project_owner=user_id).count()
            if num_result == 0:
                raise NoResultFound
            
            elif num_result > 0:
                dates                                = ProjectList.query.with_entities(ProjectList.project_start_date, ProjectList.project_terminator).filter(ProjectList.id==project_id, ProjectList.project_owner==user_id).first()
                start_date                           = dates.project_start_date
                end_date                             = dates.project_terminator
                project_date_difference_start_to_end = end_date - start_date

                diff_seconds = int(project_date_difference_start_to_end.seconds)
                diff_minutes = int(diff_seconds//60)%60
                diff_hours   = int(diff_seconds//3600)
                diff_days    = int(project_date_difference_start_to_end.days)
                diff_months  = int(diff_days//30)
                diff_years   = int(diff_days//365)

                tmp_result                = {
                    'Difference-of-Seconds': diff_seconds,
                    'Difference-in-Minutes': diff_minutes,
                    'Difference-in-Hours'  : diff_hours,
                    'Difference-of-Days'   : diff_days,
                    'Difference-in-Months' : diff_months,
                    'Difference-in-Seconds': diff_years
                }
            

        except NoResultFound:
            self.__project_setError("1")
            db.session.rollback
            return False
        except IntegrityError:
            self.__project_setError("2")
            db.session.rollback
            return False
        except CompileError:
            self.__project_setError("3")
            db.session.rollback
            return False
        except DBAPIError:
            self.__project_setError("4")
            db.session.rollback
            return False
        except InternalError:
            self.__project_setError("5")
            db.session.rollback
            return False
        except MultipleResultsFound:
            self.__project_setError("6")
            db.session.rollback
            return False
        except NoReferencedTableError:
            self.__project_setError("7")
            db.session.rollback
            return False
        except ObjectNotExecutableError:
            self.__project_setError("8")
            db.session.rollback
            return False
        except SQLAlchemyError:
            self.__project_setError("9")
            db.session.rollback
            return False
        else:
            self.__project_setResult(tmp_result)
            return True




    # donet
    def project_getNumberOfDaysFromStartToTodayByProjectId(self, user_id, project_id):
        """This function calculates the number of days between a project's start date and the current date.
            It saves it into the variable Result
        
        Raises:
            NoResultFound, Integrity Error , Compile Error , DBAPIE Error, Internal Error, MultipleResults Found, 
            No referenced Table Error, Object not Executable, SQLAlchemyError 
        
        Arguments:
            project_id (Integer): a project's id
            user_id (Integer): the associated user, who owns this project
            
        Returns:
            Boolean: returns false if an error occured, returns true if the data could be retrieved and 
            the number of days between a project's start date and today could be calculated 
            
         Tests:
            * test the behaviour when the exceptions are raised and  the associated error occurs 
            for example test the behaviour if the project, rather the project  id, is not associated  to the user given and see if the no referenced table exception is raised
            * test if the difference between the dates is calculated correctly in the correct units
                   
        """
        try: 
            num_result                           = ProjectList.query.filter_by(id=project_id, project_owner=user_id).count()
            if num_result == 0:
                raise NoResultFound

            elif num_result > 0:
                dates                                = ProjectList.query.with_entities(ProjectList.project_start_date).filter(ProjectList.id==project_id, ProjectList.project_owner==user_id).first()
                start_date                           = dates.project_start_date
                today                                = date.today()
                project_date_difference_start_to_end = today - start_date

                diff_seconds = int(project_date_difference_start_to_end.seconds)
                diff_minutes = int(diff_seconds//60)%60
                diff_hours   = int(diff_seconds//3600)
                diff_days    = int(project_date_difference_start_to_end.days)
                diff_months  = int(diff_days//30)
                diff_years   = int(diff_days//365)

                tmp_result                = {
                    'Difference-of-Seconds': diff_seconds,
                    'Difference-in-Minutes': diff_minutes,
                    'Difference-in-Hours'  : diff_hours,
                    'Difference-of-Days'   : diff_days,
                    'Difference-in-Months' : diff_months,
                    'Difference-in-Seconds': diff_years
                }
        
        except NoResultFound:
            self.__project_setError("1")
            db.session.rollback
            return False
        except IntegrityError:
            self.__project_setError("2")
            db.session.rollback
            return False
        except CompileError:
            self.__project_setError("3")
            db.session.rollback
            return False
        except DBAPIError:
            self.__project_setError("4")
            db.session.rollback
            return False
        except InternalError:
            self.__project_setError("5")
            db.session.rollback
            return False
        except MultipleResultsFound:
            self.__project_setError("6")
            db.session.rollback
            return False
        except NoReferencedTableError:
            self.__project_setError("7")
            db.session.rollback
            return False
        except ObjectNotExecutableError:
            self.__project_setError("8")
            db.session.rollback
            return False
        except SQLAlchemyError:
            self.__project_setError("9")
            db.session.rollback
            return False
        else:
            self.__project_setResult(tmp_result)
            return True




    # donet
    def project_getNumberOfDaysFromTodayToEndByProjectId(self, user_id, project_id):
        """This function calculates the number of days between today and a project's end date.
            It saves it into the variable Result.
        
         Raises:
            NoResultFound, Integrity Error , Compile Error , DBAPIE Error, Internal Error, MultipleResults Found, 
            No referenced Table Error, Object not Executable, SQLAlchemyError 
        
        Arguments:
            project_id (Integer): a project's id
            user_id (Integer): the associated user, who owns this project
            
         Returns:
            Boolean: returns false if an error occured, returns true if the data could be retrieved and 
            the number of days between  today and a project's end date could be calculated
        
        Tests:
            * test the behaviour when the exceptions are raised and  the associated error occurs 
            * test if the difference between the dates is calculated correctly in the correct units for example  test the behaviour if the current date is the end date and if the current date is after the end date
           
        """
        try: 
            num_result = ProjectList.query.filter_by(id=project_id, project_owner=user_id).count()
            if num_result == 0:
                raise NoResultFound

            elif num_result > 0:
                dates                                = ProjectList.query.with_entities(ProjectList.project_terminator).filter(ProjectList.id==project_id, ProjectList.project_owner==user_id).first()
                today                                = date.today()
                end_date                             = dates.project_terminator
                project_date_difference_start_to_end = end_date - today

                diff_seconds = int(project_date_difference_start_to_end.seconds)
                diff_minutes = int(diff_seconds//60)%60
                diff_hours   = int(diff_seconds//3600)
                diff_days    = int(project_date_difference_start_to_end.days)
                diff_months  = int(diff_days//30)
                diff_years   = int(diff_days//365)

                tmp_result                = {
                    'Difference-of-Seconds': diff_seconds,
                    'Difference-in-Minutes': diff_minutes,
                    'Difference-in-Hours'  : diff_hours,
                    'Difference-of-Days'   : diff_days,
                    'Difference-in-Months' : diff_months,
                    'Difference-in-Seconds': diff_years
                }


            
        except NoResultFound:
            self.__project_setError("1")
            db.session.rollback
            return False
        except IntegrityError:
            self.__project_setError("2")
            db.session.rollback
            return False
        except CompileError:
            self.__project_setError("3")
            db.session.rollback
            return False
        except DBAPIError:
            self.__project_setError("4")
            db.session.rollback
            return False
        except InternalError:
            self.__project_setError("5")
            db.session.rollback
            return False
        except MultipleResultsFound:
            self.__project_setError("6")
            db.session.rollback
            return False
        except NoReferencedTableError:
            self.__project_setError("7")
            db.session.rollback
            return False
        except ObjectNotExecutableError:
            self.__project_setError("8")
            db.session.rollback
            return False
        except SQLAlchemyError:
            self.__project_setError("9")
            db.session.rollback
            return False
        else:
            self.__project_setResult(tmp_result)
            return True
    
      
    

    # DML Functions  
    # ggf erzeugbare Anzahl an Projekten pro User beschränken?
    # donet
    def project_createProject(self, project_owner, project): 
        """This function creates a project with the users input and adds it to the database.

        Raises:
            NoResultFound, Integrity Error , Compile Error , DBAPIE Error, Internal Error, MultipleResults Found, 
            No referenced Table Error, Object not Executable, SQLAlchemyError 

        Args:
            * project_owner (Integer): user who wants to create the project 
            * project: an array containing the information about the project to be created given by the user
            
        Returns:   
            Boolean: returns false if an error occured, returns true if the project could be added.  
            
        Tests:
            * test if all the input data is added to the database in the right format
            * test the behaviour when not all data is given in the project array, for example no title for the project
        """
        try: 
            date_object_start = datetime.strptime(project['project-start-date'], "%Y-%m-%d").date()
            date_object_end   = datetime.strptime(project['project-end-date'], "%Y-%m-%d").date()
            project           = ProjectList(project_owner=project_owner, project_title=project['project-title'], project_description=project['project-description'], project_start_date=date_object_start, project_terminator=date_object_end)
            
            db.session.add(project)
            db.session.commit()
            
            project_schema = ProjectSchema()
            output         = project_schema.dump(project)

        except NoResultFound:
            self.__project_setError("1")
            db.session.rollback
            return False
        except IntegrityError:
            self.__project_setError("2")
            db.session.rollback
            return False
        except CompileError:
            self.__project_setError("3")
            db.session.rollback
            return False
        except DBAPIError:
            self.__project_setError("4")
            db.session.rollback
            return False
        except InternalError:
            self.__project_setError("5")
            db.session.rollback
            return False
        except MultipleResultsFound:
            self.__project_setError("6")
            db.session.rollback
            return False
        except NoReferencedTableError:
            self.__project_setError("7")
            db.session.rollback
            return False
        except ObjectNotExecutableError:
            self.__project_setError("8")
            db.session.rollback
            return False
        else:
            self.__project_setResult(output)
            return True
            
     
       
    # donet
    def project_deleteProjectByProjectId(self, user_id, project_id):
        """This function deletes a specified project. 
        
        Raises:
            NoResultFound, Integrity Error , Compile Error , DBAPIE Error, Internal Error, MultipleResults Found, 
            No referenced Table Error, Object not Executable, SQLAlchemyError 

        Args:
            id (Integer): a projects Id
            user (Integer): the associated user, who owns this project

        Returns:
            Boolean: returns false if an error occured, returns true if the project could be deleted.
            
        Tests:
            * test the behaviour when an exception is raised and  the associated error occurs eg the NoResultFound Error
              and test if the rollback works when an error ocurred
            * test the behaviour when user id and project id do not belong together meaning that the user does not own this project
        """
        try:
            project_to_be_deleted = db.session.query(ProjectList).filter_by(id=project_id, project_owner=user_id).one()
            db.session.delete(project_to_be_deleted)
            db.session.commit()

            project_schema = ProjectSchema(many=False)
            output         = project_schema.dump(project_to_be_deleted)


        except NoResultFound:
            self.__project_setError("1")
            db.session.rollback
            return False
        except IntegrityError:
            self.__project_setError("2")
            db.session.rollback
            return False
        except CompileError:
            self.__project_setError("3")
            db.session.rollback
            return False
        except DBAPIError:
            self.__project_setError("4")
            db.session.rollback
            return False
        except InternalError:
            self.__project_setError("5")
            db.session.rollback
            return False
        except MultipleResultsFound:
            self.__project_setError("6")
            db.session.rollback
            return False
        except NoReferencedTableError:
            self.__project_setError("7")
            db.session.rollback
            return False
        except ObjectNotExecutableError:
            self.__project_setError("8")
            db.session.rollback
            return False
        except SQLAlchemyError:
            self.__project_setError("9")
            db.session.rollback
            return False
        else:
            self.__project_setResult(output)
            return True
    
    

    # donet
    # stmt = (update(user_table).where(user_table.c.id == 5).values(name='user #5'))
    def project_updateProjectbyProjectId(self, user_id, project): 
        """This function serves to update a specific project identified by its id. 
        
        Raises:
            NoResultFound, Integrity Error , Compile Error , DBAPIE Error, Internal Error, MultipleResults Found, 
            No referenced Table Error, Object not Executable, SQLAlchemyError 

        Args:
            project: an array containing the information about the project to be created given by the user
            user_id (Integer): the associated user, who owns this projectt

        Returns:
            Boolean: returns false if an error occured, returns true if the project could be updated.
            
        Tests:
            *  test the behaviour when an exception is raised and  the associated error occurs
              and test if the rollback works when an error ocurred
            * test if all the input data is added to the database in the right format
            * test the behaviour when not all data is given in the project array, so the user just wants to update some parts of the project
            
        """
        try:
            project_id            = project['project-id']
            project_title         = project['project-title']
            project_description   = project['project-description']
            date_object_start     = datetime.strptime(project['project-start-date'], "%Y-%m-%d").date()
            date_object_end       = datetime.strptime(project['project-end-date'], "%Y-%m-%d").date()
            
            project_to_be_updated = db.session.query(ProjectList).filter_by(id=project_id, project_owner=user_id).update(dict(project_title=project_title, project_description=project_description, project_start_date=date_object_start, project_terminator=date_object_end))
            db.session.commit()

        except NoResultFound:
            self.__project_setError("1")
            db.session.rollback
            return False
        except IntegrityError:
            self.__project_setError("2")
            db.session.rollback
            return False
        except CompileError:
            self.__project_setError("3")
            db.session.rollback
            return False
        except DBAPIError:
            self.__project_setError("4")
            db.session.rollback
            return False
        except InternalError:
            self.__project_setError("5")
            db.session.rollback
            return False
        except MultipleResultsFound:
            self.__project_setError("6")
            db.session.rollback
            return False
        except NoReferencedTableError:
            self.__project_setError("7")
            db.session.rollback
            return False
        except ObjectNotExecutableError:
            self.__project_setError("8")
            db.session.rollback
            return False
        except SQLAlchemyError:
            self.__project_setError("9")
            db.session.rollback
            return False
        else: 
            self.__project_setResult(project_to_be_updated)
            return True
         
    
        
        
        
        
    
