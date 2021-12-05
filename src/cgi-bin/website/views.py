import asyncio
import httpx
from flask_login import current_user
from flask import Blueprint, render_template, url_for, redirect, flash, json, jsonify


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
async def emptyDashboard():
    """This functions renders the login page when the /dashboard URL is called and if the user is not logged in. If the user is logged in and has no projects created, then the functions renders the start project page. If the user already has projects, then the functions renders the dashboard page

    Returns:
        html: the page that is rendered
        
    Test 1: calling the url and see if it renders the right template
    Test 2: try to create a project if no user is logged in
    """
    if current_user.is_authenticated:
        user_id = current_user.id

        async with httpx.AsyncClient() as client:
            all_projects_by_user = await client.get(f"http://127.0.0.1:5000/api/get-all-projects-by-user?user-id={user_id}") 

        count_projects = all_projects_by_user.json()
        
        print(all_projects_by_user.json())
        if not 'count-result-set' in count_projects:
            return render_template('project/start-project.html')

        elif 'count-result-set' in count_projects:
            print(count_projects['count-result-set'])
            if count_projects['count-result-set'] > 0:
                first_project = all_projects_by_user.json()['result-set-data'][0]['id']
                return redirect(url_for('views.dashboard', project_id=first_project))
        else:
            return render_template('project/start-project.html')
    
    else:
        redirect(url_for('auth.auth_login'))



@views.route('/dashboard/<project_id>')
async def dashboard(project_id):
    """This functions renders the project page with the id that is given through the parameter  

    Args:
        project_id (int): the id of the project

    Returns:
        html: the page that is rendered
        
    Test 1: calling the url with a certain project id and see if it renders the right template with the right project
    Test 2: calling the url with a wrong id and see if it throws an error
    """
    project_id = int(project_id)
    if current_user.is_authenticated:
        user_id = current_user.id

        count_date_since_start = httpx.get(f'http://127.0.0.1:5000/api/get-date-difference-stt-by-project-id?user-id={user_id}&project-id={project_id}')                   # get date differences between project start date and current date

        async with httpx.AsyncClient() as client:
            all_projects_by_user        = await client.get(f"http://127.0.0.1:5000/api/get-all-projects-by-user?user-id={user_id}")                                                                                 # get all projects that belongs to the loged in user
            current_project             = await client.get(f"http://127.0.0.1:5000/api/get-single-project-by-users-project-id?user-id={user_id}&project-id={project_id}")                                           # get only the project, the user is looking for to see prject details
            all_tasks_by_user_obj       = await client.get(f"http://127.0.0.1:5000/api/get-all-tasks-by-user?user-id={user_id}")                                                                                    # get all tasks that belongs to a user --> needed for statistics
            all_tasks_by_project        = await client.get(f"http://127.0.0.1:5000/api/get-all-task-by-username-and-project?user-id={user_id}&project-id={project_id}")                                                                     # get all tasks that belongs to a user and the project the user is looking for
            all_tasks_status_todo       = await client.get(f"http://127.0.0.1:5000/api/get-all-tasks-by-username-group-by?user-id={user_id}&project-id={project_id}&status-id=todo")                         # get all tasks that belongs to a user and the project the user is looking for and groups them by status todo
            all_tasks_status_inprogress = await client.get(f"http://127.0.0.1:5000/api/get-all-tasks-by-username-group-by?user-id={user_id}&project-id={project_id}&status-id=inprogress")                         # get all tasks that belongs to a user and the project the user is looking for and groups them by status todo
            all_tasks_status_finished   = await client.get(f"http://127.0.0.1:5000/api/get-all-tasks-by-username-group-by?user-id={user_id}&project-id={project_id}&status-id=finished")                         # get all tasks that belongs to a user and the project the user is looking for and groups them by status todo

            count_tasks_status_todo       = await client.get(f"http://127.0.0.1:5000/api/get-number-of-tasks-where-status-is?user-id={user_id}&project-id={project_id}&category-id=todo")                         # get all tasks that belongs to a user and the project the user is looking for and groups them by status todo
            count_tasks_status_inprogress = await client.get(f"http://127.0.0.1:5000/api/get-number-of-tasks-where-status-is?user-id={user_id}&project-id={project_id}&category-id=inprogress")                         # get all tasks that belongs to a user and the project the user is looking for and groups them by status todo
            count_tasks_status_finished   = await client.get(f"http://127.0.0.1:5000/api/get-number-of-tasks-where-status-is?user-id={user_id}&project-id={project_id}&category-id=finished")

            count_all_tasks_finished_by_project = await client.get(f"http://127.0.0.1:5000/api/get-number-of-tasks-where-status-is?user-id={user_id}&category-id=finished") 
        
        print(count_all_tasks_finished_by_project.json())
        print(user_id)
        print(count_all_tasks_finished_by_project.json())

        return render_template(
                'project/dashboard.html',
                projects                            = all_projects_by_user.json(),
                current_project                     = current_project.json(), 
                all_tasks                           = all_tasks_by_user_obj.json(),
                project_tasks                       = all_tasks_by_project.json(),
                project_tasks_todo                  = all_tasks_status_todo.json(),
                project_tasks_in_progress           = all_tasks_status_inprogress.json(),
                project_tasks_finished              = all_tasks_status_finished.json(),
                project_diff_date_start_today       = count_date_since_start.json(),
                count_all_tasks_finished_by_project = count_all_tasks_finished_by_project.json(),
                count_todo                          = count_tasks_status_todo.json(),
                count_inprogress                     = count_tasks_status_inprogress.json(),
                count_finished                      = count_tasks_status_finished.json()
            )
    else:
        flash('Um Zugriff auf diese Seite zu erhalten, müssen Sie sich zuerst anmelden', 'alert-danger')
        return redirect(url_for('auth.auth_login'))




@views.route('/new-project')
async def newproject():
    """This functions renders the new project page when the /new-project URL is called and if the user is logged in, but if the user is not logged in the functions renders the login page

   Returns:
        html: the page that is rendered
        
    Test 1: calling the url with a certain project id and see if it renders the right template with the right project
    Test 2: calling the url with a wrong id and see if it throws an error
    """
    if current_user.is_authenticated:
        user_id = current_user.id
        return render_template('project/new-project.html')
    else:
        flash('Um Zugriff auf diese Seite zu erhalten, müssen Sie sich zuerst anmelden', 'alert-danger')
        return redirect(url_for('auth.auth_login'))




@views.route('/kanban/<project_id>')
async def kanban(project_id):
    """This functions renders the kanban page when the /kanban URL is called and if the user is logged in, but if the user is not logged the function renders the login page

    Returns:
        html: the page that is rendered
        
    Test 1: calling the url with a certain project id and see if it renders the right template with the right project
    Test 2: calling the url with a wrong id and see if it throws an error
    """
    project_id = int(project_id)
    if current_user.is_authenticated:
        user_id                = current_user.id
        count_date_since_start = httpx.get(f'http://127.0.0.1:5000/api/get-date-difference-stt-by-project-id?user-id={user_id}&project-id={project_id}')             # get date differences between project start date and current date

        async with httpx.AsyncClient() as client:
            all_projects_by_user        = await client.get(f"http://127.0.0.1:5000/api/get-all-projects-by-user?user-id={user_id}")                                                                                 # get all projects that belongs to the loged in user
            current_project             = await client.get(f"http://127.0.0.1:5000/api/get-single-project-by-users-project-id?user-id={user_id}&project-id={project_id}")                                           # get only the project, the user is looking for to see prject details
            all_tasks_by_user_obj       = await client.get(f"http://127.0.0.1:5000/api/get-all-tasks-by-user?user-id={user_id}")                                                                                    # get all tasks that belongs to a user --> needed for statistics
            all_tasks_by_project        = await client.get(f"http://127.0.0.1:5000/api/get-all-task-by-username-and-project?user-id={user_id}&project-id={project_id}")                                                                     # get all tasks that belongs to a user and the project the user is looking for
            all_tasks_status_todo       = await client.get(f"http://127.0.0.1:5000/api/get-all-tasks-by-username-group-by?user-id={user_id}&project-id={project_id}&status-id=todo")                         # get all tasks that belongs to a user and the project the user is looking for and groups them by status todo
            all_tasks_status_inprogress = await client.get(f"http://127.0.0.1:5000/api/get-all-tasks-by-username-group-by?user-id={user_id}&project-id={project_id}&status-id=inprogress")                         # get all tasks that belongs to a user and the project the user is looking for and groups them by status todo
            all_tasks_status_finished   = await client.get(f"http://127.0.0.1:5000/api/get-all-tasks-by-username-group-by?user-id={user_id}&project-id={project_id}&status-id=finished")                         # get all tasks that belongs to a user and the project the user is looking for and groups them by status todo


        return render_template(
                'project/kanban.html',
                projects                      = all_projects_by_user.json(),
                current_project               = current_project.json(), 
                all_tasks                     = all_tasks_by_user_obj.json(),
                project_tasks                 = all_tasks_by_project.json(),
                project_tasks_todo            = all_tasks_status_todo.json(),
                project_tasks_in_progress     = all_tasks_status_inprogress.json(),
                project_tasks_finished        = all_tasks_status_finished.json(),
                project_diff_date_start_today = count_date_since_start.json()
            )
    else:
        flash('Um Zugriff auf diese Seite zu erhalten, müssen Sie sich zuerst anmelden', 'alert-danger')
        return redirect(url_for('auth.auth_login'))



@views.route('/profile')
async def profile():
    """This functions renders the profile page when the /profile URL is called and if the user is logged in, but if the user is not logged the function renders the ling page

    Returns:
        html: the page that is rendered
        
    Test 1: calling the url with a certain project id and see if it renders the right template with the right project
    Test 2: calling the url with a wrong id and see if it throws an error
    """
    if current_user.is_authenticated:
        user_id = current_user.id
       
        async with httpx.AsyncClient() as client:
            all_projects_by_user = await client.get(f"http://127.0.0.1:5000/api/get-all-projects-by-user?user-id={user_id}")                                                                                 # get all projects that belongs to the loged in user

        return render_template(
                'project/profile.html',
                projects = all_projects_by_user.json(),
            )
    else:
        flash('Um Zugriff auf diese Seite zu erhalten, müssen Sie sich zuerst anmelden', 'alert-danger')
        return redirect(url_for('auth.auth_login'))



@views.route('/statistics/<project_id>')
async def statistics(project_id):
    """This functions renders the statistics page for a certain id when the /statistics/<project_id> URL is called and if the user is logged in, but if the user is not logged the function renders the ling page
    Returns:
        html: the page that is rendered
        
    Test 1: calling the url with a certain project id and see if it renders the right template with the right project
    Test 2: calling the url with a wrong id and see if it throws an error
    """
    if current_user.is_authenticated:
        user_id = current_user.id
        count_date_since_start = httpx.get(f'http://127.0.0.1:5000/api/get-date-difference-stt-by-project-id?user-id={user_id}&project-id={project_id}')
        async with httpx.AsyncClient() as client:
            all_projects_by_user        = await client.get(f"http://127.0.0.1:5000/api/get-all-projects-by-user?user-id={user_id}")                                                                                 # get all projects that belongs to the loged in user
            current_project             = await client.get(f"http://127.0.0.1:5000/api/get-single-project-by-users-project-id?user-id={user_id}&project-id={project_id}")                                           # get only the project, the user is looking for to see prject details
            all_tasks_by_user_obj       = await client.get(f"http://127.0.0.1:5000/api/get-all-tasks-by-user?user-id={user_id}")                                                                                    # get all tasks that belongs to a user --> needed for statistics
            all_tasks_by_project        = await client.get(f"http://127.0.0.1:5000/api/get-all-task-by-username-and-project?user-id={user_id}&project-id={project_id}")                                                                     # get all tasks that belongs to a user and the project the user is looking for
            all_tasks_status_todo       = await client.get(f"http://127.0.0.1:5000/api/get-all-tasks-by-username-group-by?user-id={user_id}&project-id={project_id}&status-id=todo")                         # get all tasks that belongs to a user and the project the user is looking for and groups them by status todo
            all_tasks_status_inprogress = await client.get(f"http://127.0.0.1:5000/api/get-all-tasks-by-username-group-by?user-id={user_id}&project-id={project_id}&status-id=inprogress")                         # get all tasks that belongs to a user and the project the user is looking for and groups them by status todo
            all_tasks_status_finished   = await client.get(f"http://127.0.0.1:5000/api/get-all-tasks-by-username-group-by?user-id={user_id}&project-id={project_id}&status-id=finished")


            count_tasks_status_todo       = await client.get(f"http://127.0.0.1:5000/api/get-number-of-tasks-where-status-is?user-id={user_id}&project-id={project_id}&category-id=todo")                         # get all tasks that belongs to a user and the project the user is looking for and groups them by status todo
            count_tasks_status_inprogress = await client.get(f"http://127.0.0.1:5000/api/get-number-of-tasks-where-status-is?user-id={user_id}&project-id={project_id}&category-id=inprogress")                         # get all tasks that belongs to a user and the project the user is looking for and groups them by status todo
            count_tasks_status_finished   = await client.get(f"http://127.0.0.1:5000/api/get-number-of-tasks-where-status-is?user-id={user_id}&project-id={project_id}&category-id=finished")
            # count_all_tasks_finished_by_project = await client.get(f"http://127.0.0.1:5000/api/get-number-of-tasks-where-status-is?user-id={user_id}&category-id=finished")
        
        print(user_id)
        print(count_tasks_status_todo.json()['result-set-data'])
        print(count_tasks_status_inprogress.json()['result-set-data'])
        print(count_tasks_status_finished.json()['result-set-data'])
        return render_template(
                'project/statistics.html',
                projects                            = all_projects_by_user.json(),
                current_project                     = current_project.json(), 
                all_tasks                           = all_tasks_by_user_obj.json(),
                project_tasks                       = all_tasks_by_project.json(),
                project_tasks_todo                  = all_tasks_status_todo.json(),
                project_tasks_in_progress           = all_tasks_status_inprogress.json(),
                project_diff_date_start_today       = count_date_since_start.json(),
                project_tasks_finished              = all_tasks_status_finished.json(),
                count_todo                          = count_tasks_status_todo.json(),
                count_inprogress                     = count_tasks_status_inprogress.json(),
                count_finished                      = count_tasks_status_finished.json()
            
            )
    else:
        flash('Um Zugriff auf diese Seite zu erhalten, müssen Sie sich zuerst anmelden', 'alert-danger')
        return redirect(url_for('auth.auth_login'))


@views.route('/settings/')
async def settings():
    """This functions renders the settings page when the /settings/ URL is called and if the user is logged in, but if the user is not logged the function renders the ling page
    Returns:
        html: the page that is rendered
        
    Test 1: calling the url with a certain project id and see if it renders the right template with the right project
    Test 2: calling the url with a wrong id and see if it throws an error
    """
    if current_user.is_authenticated:
        user_id = current_user.id
       
        async with httpx.AsyncClient() as client:
            all_projects_by_user = await client.get(f"http://127.0.0.1:5000/api/get-all-projects-by-user?user-id={user_id}")                                                                                 # get all projects that belongs to the loged in user

        return render_template(
                'project/settings.html',
                projects = all_projects_by_user.json(),
            )
    else:
        flash('Um Zugriff auf diese Seite zu erhalten, müssen Sie sich zuerst anmelden', 'alert-danger')
        return redirect(url_for('auth.auth_login'))



@views.route('/projectsettings/<project_id>')
async def projectsettings(project_id):
    """This functions renders the projectsettings üage for a certain project when the /projectsettings/<project_id> URL is called and if the user is logged in, but if the user is not logged the function renders the ling page
    Returns:
        html: the page that is rendered
        
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

        return render_template(
                'project/project_settings.html',
                projects                      = all_projects_by_user.json(),
                current_project               = current_project.json(), 
                project_diff_date_start_today = count_date_since_start.json()
            )
    else:
        flash('Um Zugriff auf diese Seite zu erhalten, müssen Sie sich zuerst anmelden', 'alert-danger')
        return redirect(url_for('auth.auth_login'))



@views.route('/newtask/<project_id>')
async def newtask(project_id):
    """This functions renders the new task page for a certain project when the /newtask/<project_id> URL is called and if the user is logged in, but if the user is not logged the function renders the ling page
    Returns:
        html: the page that is rendered
        
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
            all_tasks_status_todo       = await client.get(f"http://127.0.0.1:5000/api/get-all-tasks-by-username-group-by?user-id={user_id}&project-id={project_id}&status-id=todo")                         # get all tasks that belongs to a user and the project the user is looking for and groups them by status todo
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
                project_tasks_todo            = all_tasks_status_todo.json(),
                project_tasks_in_progress     = all_tasks_status_inprogress.json(),
                project_tasks_finished        = all_tasks_status_finished.json(),
                project_diff_date_start_today = count_date_since_start.json()
            )
    else:
        flash('Um Zugriff auf diese Seite zu erhalten, müssen Sie sich zuerst anmelden', 'alert-danger')
        return redirect(url_for('auth.auth_login'))

@views.route('/delete-project/<project_id>')
async def delete_project(project_id):
    """This functions renders the view profile page when the /delete-project/<project_id> URL is called and if the user is logged in, but if the user is not logged the function renders the ling page
    Returns:
        html: the page that is rendered
        
    Test 1: calling the url with a certain project id and see if it renders the right template with the right project
    Test 2: calling the url with a wrong id and see if it throws an error
    """
    project_id = int (project_id)
    if current_user.is_authenticated:
        user_id = current_user.id

        async with httpx.AsyncClient() as client:
            all_tasks_by_user_obj = await client.get(f"http://127.0.0.1:5000/api/get-all-tasks-by-user?user-id={user_id}")                                                                          # get all tasks that belongs to a user --> needed for statistics
            all_task_obj = all_tasks_by_user_obj.json()
            if 'result-set-data' in all_task_obj:
                print(True)
                i=0
                for task in all_task_obj['result-set-data']:
                    i=i+1
                    task_id   = task['id']
                    temp_task = await client.delete(f"http://127.0.0.1:5000/api/delete-task-by-id?user-id={user_id}&task-id={task_id}")
                    # print(task_id, ' löschen erfolgreich')
            
        deleted_project = httpx.delete(f"http://127.0.0.1:5000/api/delete-project?user-id={user_id}&project-id={project_id}")
        
        return redirect(url_for('views.profile')) 
    
            

    

