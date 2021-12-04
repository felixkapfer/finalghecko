import asyncio
import httpx
from flask_login import current_user
from flask import Blueprint, render_template, url_for, redirect, flash


views = Blueprint('views', __name__)

@views.route('/')
def home():
    """This functions renders the authentification sign-in page when the base URL is called 

    Returns:
        html: the authentification sign-in page
        
    Test: calling the url and see if it renders the right template
    """
    return render_template('auth/sign-in.html')

@views.route('/dashboard')
def emptyDashboard():
    """This functions renders the project start-project page when the /dashboard URL is called 

    Returns:
        html: the project start-project page
        
    Test: calling the url and see if it renders the right template
    """
    return render_template('project/start-project.html')

@views.route('/dashboard/<project_id>')
async def dashboard(project_id):
    """This functions renders the project page with the id that is given through the parameter  

    Args:
        project_id (int): the id of the project

    Returns:
        html: the project page with the id that is given through the parameter 
        
    Test 1: calling the url with a certain project id and see if it renders the right template with the right project
    Test 2: calling the url with a wrong id and see if it throws an error
    """
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
def newproject():
    """This functions renders the new project page when the /new-project URL is called 

    Returns:
        html: the new project page
        
    Test: calling the url and see if it renders the right template
    """
    return render_template('project/new-project.html')

@views.route('/kanban')
def kanban():
    """This functions renders the kanban page when the /kanban URL is called 

    Returns:
        html: the kanban page
        
    Test: calling the url and see if it renders the right template
    """
    return render_template('project/kanban.html')

@views.route('/profile')
def profile():
    """This functions renders the profile page when the /profile URL is called 

    Returns:
        html: the profile page
        
    Test: calling the url and see if it renders the right template
    """
    return render_template('project/profile.html')

@views.route('/statistics')
def statistics():
    """This functions renders the statistics page when the /statistics URL is called 

    Returns:
        html: the statistics page
        
    Test: calling the url and see if it renders the right template
    """
    return render_template('project/statistics.html')

@views.route('/settings')
def settings():
    """This functions renders the settings page when the /settings URL is called 

    Returns:
        html: the settings page
        
    Test: calling the url and see if it renders the right template
    """
    return render_template('project/settings.html')

@views.route('/projectsettings')
def projectsettings():
    """This functions renders the projectsettings page when the /projectsettings URL is called 

    Returns:
        html: the projectsettings page
        
    Test: calling the url and see if it renders the right template
    """
    return render_template('project/project_settings.html')

@views.route('/newtask')
def newtask():
    """This functions renders the new task page when the /newtask URL is called

    Returns:
        html: the new task page
        
    Test: calling the url and see if it renders the right template
    """
    return render_template('project/new-task.html')

@views.route('/statisticsproject')
def statisticsproject():
    """This functions renders the new task page when the /newtask URL is called

    Returns:
        html: the new task page
        
    Test: calling the url and see if it renders the right template
    """
    return render_template('project/statistics_project.html')