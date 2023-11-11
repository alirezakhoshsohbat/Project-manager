from flask import Flask, render_template, request, url_for, redirect, flash
from threading import Timer
import codecs
from flask import jsonify


app = Flask(__name__)
app.secret_key = 'your_secret_key'
username=''
er = 0
stop_error_time = 15


class Project_Manager:
    def __init__(self):
        self.p=[]

    def add_project(self, name, team, boss, start, end, Profit, loss,about):
        with codecs.open('projects.txt', 'a+', encoding='utf-8') as file:
            file.write(f'{name}${boss}${team}${start}${end}${Profit}${loss}${int(Profit)-int(loss)}${about}${username}\n')

    def show_projects(self):
        with open('projects.txt', 'r', encoding='utf-8') as file:
            for line in file:
                name, boss, team, start, end, profit, loss, gain, about,user = line.strip().split('$')
                if user == username :
                    project = {
                        'name': name,
                        'boss': boss,
                        'team': team,
                        'start': start,
                        'end': end,
                        'profit': profit,
                        'loss': loss,
                        'gain': gain,
                        'about': about,
                        'user': user
                    }
                    self.p.append(project)
        return self.p

    def update_project(self, projects):
        with open('projects.txt', 'w', encoding='utf-8') as file:
            for project in projects:
                name = project['name']
                boss = project['boss']
                team = project['team']
                start = project['start']
                end = project['end']
                profit = project['profit']
                loss = project['loss']
                gain = project['gain']
                about = project['about']
                file.write(f'{name}${boss}${team}${start}${end}${profit}${loss}${gain}${about}${username}\n')

    def search_by_name(self,target):
        result=[]
        projects=self.show_projects()
        for project in projects :
            if target in project['name']:
                result.append(project)
        return result

    def search_by_start(self,start):
        result=[]
        projects=self.show_projects()
        for project in projects:
            if project['start'] == start:
                result.append(project)
        return result

    def search_by_end(self,end):
        result=[]
        projects=self.show_projects()
        for project in projects:
            if project['end'] == end:
                result.append(project)
        return result

    def search_by_mount(self,Y,M,Mend,Yend):
        result=[]
        projects=self.show_projects()
        for project in projects:
            year,maount,day=project['start'].split('/')
            yearend,maountend,dayend=project['end'].split('/')
            if Y<year :
                if Yend<yearend:
                    result.append(project)
                elif Yend==yearend :
                    if maountend<=Mend:
                        result.append(project)
            elif Y==year:
                if maount>=M:
                    if Yend>yearend:
                        result.append(project)
                    elif Yend==yearend :
                        if maountend<=Mend:
                            result.append(project)
        return result

    def financial_gain(self,projects):
        profit=0
        loss=0
        gain=0
        result=[]
        for project in projects:    
            profit += int(project['profit'])
            loss += int(project['loss'])
            gain += int(project['gain'])
        result.append(profit)
        result.append(loss)
        result.append(gain)
        return result





@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    global username 
    project_manager = Project_Manager()
    projects = project_manager.show_projects()
    return render_template('home.html', username=username, projects=projects , display_result_name='none',  display_result_start='none', display_result_end='none',display_all='block',display_result_mount='none',display_result_financial='none')

def login_check(username, password):
    with open('users.txt', 'r') as file:
        for line in file:
            username_list, password_list = line.strip().split(',')
            if username == username_list and password == password_list:
                return True
    return False

def register_check(username):
    with open('users.txt', 'r') as file:
        for line in file:
            username_list, password_list = line.strip().split(',')
            if username == username_list:
                return True
    return False

@app.route('/')
def index():
    global er
    if er >= 3:
        return render_template('error.html', t=stop_error_time)
    else:
        return render_template('index.html')

def reset_errors():
    global er
    er = 0

@app.route('/login', methods=['GET', 'POST'])
def login():
    global er
    global username
    if er < 3:
        username = request.form['username']
        password = request.form['password']
        if login_check(username, password):
            reset_errors() 
            return redirect(url_for('dashboard',user=username))
        else:
            er += 1
            if er >= 3:
                t = Timer(stop_error_time - 3, reset_errors)  
                t.start()
                return redirect(url_for('index'))
            flash('شما رمزعبور یا نام کاربری خود را {} بار اشتباه وارد کردید'.format(er))
            return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    new_username = request.form['new_username']
    new_password = request.form['new_password']
    if register_check(new_username):
        flash('نام کاربری شما از قبل در سیستم وجود دارد')
    else:
        with open('users.txt', 'a') as file:
            file.write(f'{new_username},{new_password}\n')
        flash('ثبت نام شما با موفقیت انجام شد')
    return redirect(url_for('index'))

@app.post("/project-register")
def register_project():
    if request.method == 'POST':
        name = request.form['project-name']
        boss = request.form['boss-name']
        team = request.form['team']
        start = request.form['start-date']
        end = request.form['end-date']
        profit = int(request.form['profit'])
        loss = int(request.form['loss'])
        about = request.form['about']
        project = Project_Manager()
        project.add_project(name, team, boss, start, end, profit, loss,about)
        flash('ثبت پروژه با موفقیت انجام شد ')
        return redirect(url_for('dashboard'))

@app.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    project_manager = Project_Manager()
    projects = project_manager.show_projects()
    if request.method == 'POST':
        projects[project_id - 1]['name'] = request.form['name']
        projects[project_id - 1]['boss'] = request.form['boss']
        projects[project_id - 1]['team'] = request.form['team']
        projects[project_id - 1]['start'] = request.form['start']
        projects[project_id - 1]['end'] = request.form['end']
        projects[project_id - 1]['profit'] = int(request.form['profit'])
        projects[project_id - 1]['loss'] = int(request.form['loss'])
        projects[project_id - 1]['gain'] = int(request.form['profit'])-int(request.form['loss'])
        projects[project_id - 1]['about'] = request.form['about']
        project_manager.update_project(projects)
        return redirect(url_for('dashboard'))
    else:
        project = projects[project_id - 1]
        return render_template('edit_project.html', project=project)

@app.get('/delete/<int:project_id>')
def remove(project_id):
    project_manager = Project_Manager()
    projects = project_manager.show_projects()
    
    projects.pop(project_id-1)
    
    project_manager.update_project(projects)
    flash('پروژه با موفقیت حذف شد')
    return redirect(url_for('dashboard'))

@app.route('/search', methods=['GET', 'POST'])
def search_name():
    value = str(request.args.get('search-name-form'))
    project_manager = Project_Manager()
    result_name=project_manager.search_by_name(value)
    return render_template('home.html', username=username , result_name=result_name , display_result_name='block',display_result_end='none',  display_result_start='none' ,display_all='none !important',display_result_mount='none',display_result_financial='none')

@app.route('/search-start', methods=['GET', 'POST'])
def search_by_start():
    value = str(request.args.get('search-start-form'))
    project_manager=Project_Manager()
    result=project_manager.search_by_start(value)
    return render_template('home.html', username=username , result_start=result , display_result_start='block',display_result_name='none', display_result_end='none',display_all='none !important',display_result_mount='none',display_result_financial='none')

@app.route('/search-end', methods=['GET', 'POST'])
def search_by_end():
    value = str(request.args.get('search-end-form'))
    project_manager=Project_Manager()
    result_end=project_manager.search_by_end(value)
    return render_template('home.html', username=username , result_end=result_end, display_result_start='none',display_result_end='block',display_result_name='none', display_all='none !important',display_result_mount='none',display_result_financial='none')

@app.route('/search-mount', methods=['GET', 'POST'])
def  search_by_mount():
    Y=str(request.args.get('year'))
    Yend=str(request.args.get('yearend'))
    M=str(request.args.get('mount'))
    Mend=str(request.args.get('mountend'))
    project_manager=Project_Manager()
    result_mount=project_manager.search_by_mount(Y,M,Mend,Yend)
    return render_template('home.html', username=username , result_mount=result_mount , display_result_start='none',display_result_end='none',display_result_name='none',display_result_mount='block', display_all='none !important',display_result_financial='none')

@app.route('/financial', methods=['GET', 'POST'])
def search_financial():
    Y=str(request.args.get('sal'))
    Yend=str(request.args.get('salend'))
    M=str(request.args.get('mah'))
    Mend=str(request.args.get('mahend'))
    project_manager=Project_Manager()
    result_mount_finance=project_manager.search_by_mount(Y,M,Mend,Yend)
    result_financial = project_manager.financial_gain(result_mount_finance)
    profit,loss,gain=result_financial
    print('profit :' ,profit)
    print('loss :',loss)
    print('gain :',gain)
    return render_template('home.html', username=username , result_mount_finance=result_mount_finance, profit=profit ,loss=loss ,gain=gain, display_result_start='none',display_result_end='none',display_result_name='none',display_result_mount='none !important', display_all='none !important',display_result_financial='block')

if __name__ == '__main__':
    app.run(port=5521, debug=True)