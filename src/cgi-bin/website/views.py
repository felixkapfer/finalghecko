import asyncio
import httpx
from flask_login import current_user
from flask import Blueprint, render_template, url_for, redirect, flash


views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('auth/sign-in.html')

@views.route('/dashboard')
def emptyDashboard():
    return render_template('project/start-project.html')

@views.route('/dashboard/<project_id>')
async def dashboard(project_id):
    project_id = int(project_id)
    if current_user.is_authenticated:
        user_id = current_user.id
        count_date_since_start = httpx.get(f'http://127.0.0.1:5000/api/get-date-difference-stt-by-project-id?user-id={{user_id}}&project-id={project_id}')            # get date differences between project start date and current date

        async with httpx.AsyncClient() as client:
            all_projects_by_user        = await client.get(f"http://127.0.0.1:5000/api/get-all-projects-by-user?user-id={user_id}")                                                                                 # get all projects that belongs to the loged in user
            current_project             = await client.get(f"http://127.0.0.1:5000/api/get-single-project-by-users-project-id?user-id={user_id}&project-id={project_id}")                                           # get only the project, the user is looking for to see prject details
            all_tasks_by_user_obj       = await client.get(f"http://127.0.0.1:5000/api/get-all-tasks-by-user?user-id={user_id}")                                                                                    # get all tasks that belongs to a user --> needed for statistics
            all_tasks_by_project        = await client.get(f"http://127.0.0.1:5000/api/get-all-task-by-username-and-project?user-id={user_id}&project-id={project_id}")                                                                     # get all tasks that belongs to a user and the project the user is looking for
            all_tasks_status_toto       = await client.get(f"http://127.0.0.1:5000/api/get-all-tasks-by-username-group-by?user-id={user_id}&project-id={project_id}&status-id=todo")                         # get all tasks that belongs to a user and the project the user is looking for and groups them by status todo
            all_tasks_status_inprogress = await client.get(f"http://127.0.0.1:5000/api/get-all-tasks-by-username-group-by?user-id={user_id}&project-id={project_id}&status-id=inprogress")                         # get all tasks that belongs to a user and the project the user is looking for and groups them by status todo
            all_tasks_status_finished   = await client.get(f"http://127.0.0.1:5000/api/get-all-tasks-by-username-group-by?user-id={user_id}&project-id={project_id}&status-id=finished")                         # get all tasks that belongs to a user and the project the user is looking for and groups them by status todo
        print(count_date_since_start.json())
        print(user_id)
        print(current_project.json())

        return render_template(
                'project/dashboard.html',
                projects                      = all_projects_by_user.json(),
                current_project               = current_project.json(), 
                all_tasks                     = all_tasks_by_user_obj.json(),
                project_tasks                 = all_tasks_by_project.json(),
                project_tasks_todo            = all_tasks_status_toto.json(),
                project_tasks_in_progress     = all_tasks_status_inprogress.json(),
                project_tasks_finished        = all_tasks_status_finished.json(),
                project_diff_date_start_today = count_date_since_start.json()
            )
    else:
        flash('To get access to this page, you need to sign-in first!', 'alert-danger')
        return redirect(url_for('auth.auth_login'))





@views.route('/new-project')
async def newproject():
    if current_user.is_authenticated:
        user_id = current_user.id
        return render_template('project/new-project.html')
    else:
        flash('To get access to this page, you need to sign-in first!', 'alert-danger')
        return redirect(url_for('auth.auth_login'))




@views.route('/kanban/<project_id>')
async def kanban(project_id):
    project_id = int(project_id)
    if current_user.is_authenticated:
        user_id                = current_user.id
        count_date_since_start = httpx.get(f'http://127.0.0.1:5000/api/get-date-difference-stt-by-project-id?user-id={{user_id}}&project-id={project_id}')            # get date differences between project start date and current date

        async with httpx.AsyncClient() as client:
            all_projects_by_user        = await client.get(f"http://127.0.0.1:5000/api/get-all-projects-by-user?user-id={user_id}")                                                                                 # get all projects that belongs to the loged in user
            current_project             = await client.get(f"http://127.0.0.1:5000/api/get-single-project-by-users-project-id?user-id={user_id}&project-id={project_id}")                                           # get only the project, the user is looking for to see prject details
            all_tasks_by_user_obj       = await client.get(f"http://127.0.0.1:5000/api/get-all-tasks-by-user?user-id={user_id}")                                                                                    # get all tasks that belongs to a user --> needed for statistics
            all_tasks_by_project        = await client.get(f"http://127.0.0.1:5000/api/get-all-task-by-username-and-project?user-id={user_id}&project-id={project_id}")                                                                     # get all tasks that belongs to a user and the project the user is looking for
            all_tasks_status_toto       = await client.get(f"http://127.0.0.1:5000/api/get-all-tasks-by-username-group-by?user-id={user_id}&project-id={project_id}&status-id=todo")                         # get all tasks that belongs to a user and the project the user is looking for and groups them by status todo
            all_tasks_status_inprogress = await client.get(f"http://127.0.0.1:5000/api/get-all-tasks-by-username-group-by?user-id={user_id}&project-id={project_id}&status-id=inprogress")                         # get all tasks that belongs to a user and the project the user is looking for and groups them by status todo
            all_tasks_status_finished   = await client.get(f"http://127.0.0.1:5000/api/get-all-tasks-by-username-group-by?user-id={user_id}&project-id={project_id}&status-id=finished")                         # get all tasks that belongs to a user and the project the user is looking for and groups them by status todo
        print(count_date_since_start.json())
        print(user_id)
        print(current_project.json())

        return render_template(
                'project/kanban.html',
                projects                      = all_projects_by_user.json(),
                current_project               = current_project.json(), 
                all_tasks                     = all_tasks_by_user_obj.json(),
                project_tasks                 = all_tasks_by_project.json(),
                project_tasks_todo            = all_tasks_status_toto.json(),
                project_tasks_in_progress     = all_tasks_status_inprogress.json(),
                project_tasks_finished        = all_tasks_status_finished.json(),
                project_diff_date_start_today = count_date_since_start.json()
            )
    else:
        flash('To get access to this page, you need to sign-in first!', 'alert-danger')
        return redirect(url_for('auth.auth_login'))



@views.route('/profile')
async def profile():
    if current_user.is_authenticated:
        user_id                = current_user.id
       
        async with httpx.AsyncClient() as client:
            all_projects_by_user        = await client.get(f"http://127.0.0.1:5000/api/get-all-projects-by-user?user-id={user_id}")                                                                                 # get all projects that belongs to the loged in user

        return render_template(
                'project/profile.html',
                projects                      = all_projects_by_user.json(),
            )
    else:
        flash('To get access to this page, you need to sign-in first!', 'alert-danger')
        return redirect(url_for('auth.auth_login'))



@views.route('/statistics')
def statistics():
    return render_template('project/statistics.html')




@views.route('/settings/<project_id>')
async def settings(project_id):
    project_id = int(project_id)
    if current_user.is_authenticated:
        user_id = current_user.id
       
        async with httpx.AsyncClient() as client:
           current_project = await client.get(f"http://127.0.0.1:5000/api/get-single-project-by-users-project-id?user-id={user_id}&project-id={project_id}")                                           # get only the project, the user is looking for to see prject details                                                                             # get all projects that belongs to the loged in user

        return render_template(
                'project/settings.html',
                current_project = current_project.json(),
            )
    else:
        flash('To get access to this page, you need to sign-in first!', 'alert-danger')
        return redirect(url_for('auth.auth_login'))



@views.route('/projectsettings/<project_id>')
async def projectsettings():
    project_id = int(project_id)
    if current_user.is_authenticated:
        user_id = current_user.id
       
        async with httpx.AsyncClient() as client:
           current_project = await client.get(f"http://127.0.0.1:5000/api/get-single-project-by-users-project-id?user-id={user_id}&project-id={project_id}")                                           # get only the project, the user is looking for to see prject details                                                                             # get all projects that belongs to the loged in user

        return render_template(
                'project/project_settings.html',
                current_project = current_project.json(),
            )
    else:
        flash('To get access to this page, you need to sign-in first!', 'alert-danger')
        return redirect(url_for('auth.auth_login'))



@views.route('/newtask/<project_id>')
async def newtask(project_id):
    project_id = int(project_id)
    if current_user.is_authenticated:
        user_id = current_user.id
        count_date_since_start = httpx.get(f'http://127.0.0.1:5000/api/get-date-difference-stt-by-project-id?user-id={{user_id}}&project-id={project_id}')            # get date differences between project start date and current date

        async with httpx.AsyncClient() as client:
            all_projects_by_user        = await client.get(f"http://127.0.0.1:5000/api/get-all-projects-by-user?user-id={user_id}")                                                                                 # get all projects that belongs to the loged in user
            current_project             = await client.get(f"http://127.0.0.1:5000/api/get-single-project-by-users-project-id?user-id={user_id}&project-id={project_id}")                                           # get only the project, the user is looking for to see prject details
            all_tasks_by_user_obj       = await client.get(f"http://127.0.0.1:5000/api/get-all-tasks-by-user?user-id={user_id}")                                                                                    # get all tasks that belongs to a user --> needed for statistics
            all_tasks_by_project        = await client.get(f"http://127.0.0.1:5000/api/get-all-task-by-username-and-project?user-id={user_id}&project-id={project_id}")                                                                     # get all tasks that belongs to a user and the project the user is looking for
            all_tasks_status_toto       = await client.get(f"http://127.0.0.1:5000/api/get-all-tasks-by-username-group-by?user-id={user_id}&project-id={project_id}&status-id=todo")                         # get all tasks that belongs to a user and the project the user is looking for and groups them by status todo
            all_tasks_status_inprogress = await client.get(f"http://127.0.0.1:5000/api/get-all-tasks-by-username-group-by?user-id={user_id}&project-id={project_id}&status-id=inprogress")                         # get all tasks that belongs to a user and the project the user is looking for and groups them by status todo
            all_tasks_status_finished   = await client.get(f"http://127.0.0.1:5000/api/get-all-tasks-by-username-group-by?user-id={user_id}&project-id={project_id}&status-id=finished")                         # get all tasks that belongs to a user and the project the user is looking for and groups them by status todo
        print(count_date_since_start.json())
        print(current_project.json())
        print(current_project.json())

        return render_template(
                'project/new-task.html',
                projects                      = all_projects_by_user.json(),
                current_project               = current_project.json(), 
                all_tasks                     = all_tasks_by_user_obj.json(),
                project_tasks                 = all_tasks_by_project.json(),
                project_tasks_todo            = all_tasks_status_toto.json(),
                project_tasks_in_progress     = all_tasks_status_inprogress.json(),
                project_tasks_finished        = all_tasks_status_finished.json(),
                project_diff_date_start_today = count_date_since_start.json(),
                page_project_id=project_id
            )
    else:
        flash('To get access to this page, you need to sign-in first!', 'alert-danger')
        return redirect(url_for('auth.auth_login'))




@views.route('/statisticsproject/<project_id>')
async def statisticsproject(project_id):
    project_id = int(project_id)
    if current_user.is_authenticated:
        user_id                = current_user.id
        count_date_since_start = httpx.get(f'http://127.0.0.1:5000/api/get-date-difference-stt-by-project-id?user-id={{user_id}}&project-id={project_id}')            # get date differences between project start date and current date

        async with httpx.AsyncClient() as client:
            all_projects_by_user        = await client.get(f"http://127.0.0.1:5000/api/get-all-projects-by-user?user-id={user_id}")                                                                                 # get all projects that belongs to the loged in user
            current_project             = await client.get(f"http://127.0.0.1:5000/api/get-single-project-by-users-project-id?user-id={user_id}&project-id={project_id}")                                           # get only the project, the user is looking for to see prject details
            all_tasks_by_user_obj       = await client.get(f"http://127.0.0.1:5000/api/get-all-tasks-by-user?user-id={user_id}")                                                                                    # get all tasks that belongs to a user --> needed for statistics
            all_tasks_by_project        = await client.get(f"http://127.0.0.1:5000/api/get-all-task-by-username-and-project?user-id={user_id}&project-id={project_id}")                                                                     # get all tasks that belongs to a user and the project the user is looking for
            all_tasks_status_toto       = await client.get(f"http://127.0.0.1:5000/api/get-all-tasks-by-username-group-by?user-id={user_id}&project-id={project_id}&status-id=todo")                         # get all tasks that belongs to a user and the project the user is looking for and groups them by status todo
            all_tasks_status_inprogress = await client.get(f"http://127.0.0.1:5000/api/get-all-tasks-by-username-group-by?user-id={user_id}&project-id={project_id}&status-id=inprogress")                         # get all tasks that belongs to a user and the project the user is looking for and groups them by status todo
            all_tasks_status_finished   = await client.get(f"http://127.0.0.1:5000/api/get-all-tasks-by-username-group-by?user-id={user_id}&project-id={project_id}&status-id=finished")                         # get all tasks that belongs to a user and the project the user is looking for and groups them by status todo
        print(count_date_since_start.json())
        print(user_id)
        print(current_project.json())

        return render_template(
                'project/kanban.html',
                projects                      = all_projects_by_user.json(),
                current_project               = current_project.json(), 
                all_tasks                     = all_tasks_by_user_obj.json(),
                project_tasks                 = all_tasks_by_project.json(),
                project_tasks_todo            = all_tasks_status_toto.json(),
                project_tasks_in_progress     = all_tasks_status_inprogress.json(),
                project_tasks_finished        = all_tasks_status_finished.json(),
                project_diff_date_start_today = count_date_since_start.json()
            )
    else:
        flash('To get access to this page, you need to sign-in first!', 'alert-danger')
        return redirect(url_for('auth.auth_login'))