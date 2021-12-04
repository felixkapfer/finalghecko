from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('auth/sign-in.html')

@views.route('/dashboard')
def dashboard():
    return render_template('project/dashboard.html')

@views.route('/new-project')
def newproject():
    return render_template('project/new-project.html')

@views.route('/kanban')
def kanban():
    return render_template('project/kanban.html')

@views.route('/profile')
def profile():
    return render_template('project/profile.html')

@views.route('/statistics')
def statistics():
    return render_template('project/statistics.html')

@views.route('/settings')
def settings():
    return render_template('project/settings.html')

@views.route('/projectsettings')
def projectsettings():
    return render_template('project/project_settings.html')

@views.route('/newtask')
def newtask():
    return render_template('project/new-task.html')

@views.route('/statisticsproject')
def statisticsproject():
    return render_template('project/statistics_project.html')