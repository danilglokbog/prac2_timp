from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key'

DB = {
    'rules': [
        {'id': 1, 'title': 'Использование СИЗ', 'description': 'Все работники обязаны использовать каски, очки, перчатки и спецобувь.', 'category': 'Общие'},
        {'id': 2, 'title': 'Работа на высоте', 'description': 'При работе выше 1.8 м обязательно применение страховочных систем.', 'category': 'Высотные работы'},
        {'id': 3, 'title': 'Электробезопасность', 'description': 'Запрещено работать с электроустановками без допуска и снятия напряжения.', 'category': 'Электрика'}
    ],
    'incidents': [
        {'id': 1, 'date': '2025-03-15', 'location': 'Цех №3', 'description': 'Падение груза с крана, без пострадавших', 'severity': 'Средняя'},
        {'id': 2, 'date': '2025-03-10', 'location': 'Склад ГСМ', 'description': 'Разлив масла, устранено', 'severity': 'Низкая'}
    ],
    'trainings': [
        {'id': 1, 'name': 'Охрана труда для новичков', 'date': '2025-04-10', 'participants': 15},
        {'id': 2, 'name': 'Пожаротушение и эвакуация', 'date': '2025-04-15', 'participants': 25}
    ],
    'counters': {'rules': 3, 'incidents': 2, 'trainings': 2}
}

# ---------- Pages ----------
@app.route('/')
def index():
    return render_template('index.html', rules=DB['rules'], incidents=DB['incidents'], trainings=DB['trainings'])

@app.route('/admin')
def admin():
    return render_template('admin.html', rules=DB['rules'], incidents=DB['incidents'], trainings=DB['trainings'])

@app.route('/admin/rule/add', methods=['GET', 'POST'])
def add_rule():
    if request.method == 'POST':
        DB['counters']['rules'] += 1
        new_rule = {
            'id': DB['counters']['rules'],
            'title': request.form['title'],
            'description': request.form['description'],
            'category': request.form['category']
        }
        DB['rules'].insert(0, new_rule)
        return redirect(url_for('admin'))
    return render_template('add_rule.html')

@app.route('/admin/rule/edit/<int:id>', methods=['GET', 'POST'])
def edit_rule(id):
    rule = next((r for r in DB['rules'] if r['id'] == id), None)
    if not rule:
        return redirect(url_for('admin'))
    if request.method == 'POST':
        rule['title'] = request.form['title']
        rule['description'] = request.form['description']
        rule['category'] = request.form['category']
        return redirect(url_for('admin'))
    return render_template('edit_rule.html', rule=rule)

@app.route('/admin/rule/delete/<int:id>', methods=['GET', 'POST'])
def delete_rule(id):
    if request.method == 'POST':
        DB['rules'] = [r for r in DB['rules'] if r['id'] != id]
        return redirect(url_for('admin'))
    rule = next((r for r in DB['rules'] if r['id'] == id), None)
    return render_template('delete_rule.html', rule=rule)


@app.route('/admin/incident/add', methods=['GET', 'POST'])
def add_incident():
    if request.method == 'POST':
        DB['counters']['incidents'] += 1
        new_inc = {
            'id': DB['counters']['incidents'],
            'date': request.form['date'],
            'location': request.form['location'],
            'description': request.form['description'],
            'severity': request.form['severity']
        }
        DB['incidents'].insert(0, new_inc)
        return redirect(url_for('admin'))
    return render_template('add_incident.html')

@app.route('/admin/incident/edit/<int:id>', methods=['GET', 'POST'])
def edit_incident(id):
    inc = next((i for i in DB['incidents'] if i['id'] == id), None)
    if not inc:
        return redirect(url_for('admin'))
    if request.method == 'POST':
        inc['date'] = request.form['date']
        inc['location'] = request.form['location']
        inc['description'] = request.form['description']
        inc['severity'] = request.form['severity']
        return redirect(url_for('admin'))
    return render_template('edit_incident.html', inc=inc)

@app.route('/admin/incident/delete/<int:id>', methods=['GET', 'POST'])
def delete_incident(id):
    if request.method == 'POST':
        DB['incidents'] = [i for i in DB['incidents'] if i['id'] != id]
        return redirect(url_for('admin'))
    inc = next((i for i in DB['incidents'] if i['id'] == id), None)
    return render_template('delete_incident.html', inc=inc)

@app.route('/admin/training/add', methods=['GET', 'POST'])
def add_training():
    if request.method == 'POST':
        DB['counters']['trainings'] += 1
        new_train = {
            'id': DB['counters']['trainings'],
            'name': request.form['name'],
            'date': request.form['date'],
            'participants': int(request.form['participants'])
        }
        DB['trainings'].insert(0, new_train)
        return redirect(url_for('admin'))
    return render_template('add_training.html')

@app.route('/admin/training/edit/<int:id>', methods=['GET', 'POST'])
def edit_training(id):
    train = next((t for t in DB['trainings'] if t['id'] == id), None)
    if not train:
        return redirect(url_for('admin'))
    if request.method == 'POST':
        train['name'] = request.form['name']
        train['date'] = request.form['date']
        train['participants'] = int(request.form['participants'])
        return redirect(url_for('admin'))
    return render_template('edit_training.html', train=train)

@app.route('/admin/training/delete/<int:id>', methods=['GET', 'POST'])
def delete_training(id):
    if request.method == 'POST':
        DB['trainings'] = [t for t in DB['trainings'] if t['id'] != id]
        return redirect(url_for('admin'))
    train = next((t for t in DB['trainings'] if t['id'] == id), None)
    return render_template('delete_training.html', train=train)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
