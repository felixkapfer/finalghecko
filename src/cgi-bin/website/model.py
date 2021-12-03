"""
    author: Felix Kapfer
    date:12.11.2021
    license: private
"""

from . import db
from datetime import datetime
from flask_login.mixins import UserMixin


class UserList(db.Model, UserMixin):
    """
    This class extends from the SQLAlchemy sqlalchemy.orm.decl_api.Model class and is used to create the Database Table 'tbl_user_list'
    which contains all Users that have been registerd to this site.

    This class contains the following variables:
        * id            ([sqlalchemy.orm.attributes.InstrumentedAttribute]): Used to create column id which is used as primary key in the tabel
        * firstname     ([sqlalchemy.orm.attributes.InstrumentedAttribute]): Used to create column firstname in tabel to store the users firstname
        * lastname      ([sqlalchemy.orm.attributes.InstrumentedAttribute]): Used to create column lastname in tabel to store the users lastname
        * email         ([sqlalchemy.orm.attributes.InstrumentedAttribute]): Used to create column email in tabel to store the users email address
        * image_file    ([sqlalchemy.orm.attributes.InstrumentedAttribute]): Used to create column image_file in tabel to store link to users profile picture
        * pwd           ([sqlalchemy.orm.attributes.InstrumentedAttribute]): Used to create column pwd in tabel to store a users password which is used later for the login prcedure again
        * date_of_issue ([sqlalchemy.orm.attributes.InstrumentedAttribute]): Used to create column date_of_issue in tabel to store information about when the user first registerd
        * project_relationship ([sqlalchemy.orm.attributes.InstrumentedAttribute]): Used to create column date_of_issue in tabel to store information about when the user first registerd
        * task_relationship ([sqlalchemy.orm.attributes.InstrumentedAttribute]): Used to create column date_of_issue in tabel to store information about when the user first registerd


    Returns:
        [type]: [description]
    """



    __tablename__ = 'tbl_user_list'

    id                   = db.Column(db.Integer, primary_key=True)
    firstname            = db.Column(db.String(255), nullable=False)
    lastname             = db.Column(db.String(255), nullable=False)
    email                = db.Column(db.String(255), nullable=False)
    image_file           = db.Column(db.String(20), nullable=False, default='default.jpg')
    pwd                  = db.Column(db.String(60), nullable=False)
    date_of_issue        = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    project_relationship = db.relationship('ProjectList', backref='projectOwner')
    task_relationship    = db.relationship('TaskList', backref='taskOwner')




class ProjectList(db.Model):
    """
    This class extends from the SQLAlchemy sqlalchemy.orm.decl_api Model class and is used to create the Database Table ProjectList
    which contains all Projects that the users are going to create.

    This class contains the following variables :
    * id            ([sqlalchemy.orm.attributes.InstrumentedAttribute]): Used to create column id which is used as primary key in the tabel
    * project_owner ([sqlalchemy.orm.attributes.InstrumentedAttribute]): Used to create column project_owner which is used to store the owner (user) of this project. It contains a Foreign Key which is a Primary Key of table tbl_user_list 
        * id           : used to create a column named id
        * project_owner: used to create a column named project_owner
        * title        : 


    Returns:
        [type]: [description]
    """


    __tablename__ = 'tbl_project_list'  # set tablename to 'tbl_project_list'

    id                  = db.Column(db.Integer, primary_key=True)
    project_owner       = db.Column(db.Integer, db.ForeignKey('tbl_user_list.id'), nullable=False)
    project_title       = db.Column(db.String(1000), nullable=False)
    project_description = db.Column(db.Text, nullable=False)
    project_start_date  = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    project_terminator  = db.Column(db.DateTime, nullable=False)
    date_of_issue       = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    task_relationship   = db.relationship('TaskList', backref='Task')




class TaskList(db.Model):

    """
    This class extends from the SQLAlchemy Model class and is used to create the Database Table ProjectList
    which contains all Projects that the users are going to create.

    This class contains the following variables :
        * id           : used to create a column named id
        * project_owner: used to create a column named project_owner
        * title        : 


    Returns:
        [type]: [description]
    """
    __tablename__ = 'tbl_task_list'  # set tablename to 'tbl_project_list'

    id                     = db.Column(db.Integer, primary_key=True)
    task_owner             = db.Column(db.Integer, db.ForeignKey('tbl_user_list.id'), nullable=False)
    assigned_to_project_id = db.Column(db.Integer, db.ForeignKey('tbl_project_list.id'), nullable=False)
    task_title             = db.Column(db.String(1000), nullable=False)
    task_description       = db.Column(db.Text, nullable=False)
    task_status            = db.Column(db.String(25), nullable=False, default='open')
    task_terminator        = db.Column(db.DateTime, nullable=False)
    date_of_issue          = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_modified          = db.Column(db.Date, nullable=False, default=datetime.today)
    assigned_to_project_id = db.Column(db.String(255), unique=True, nullable=False)



