from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import TimeProc,User
from app.classes.forms import TimeProcForm
from flask_login import login_required
import datetime as dt

@app.route('/time/list')
def timeList():
    times = TimeProc.objects()
    return render_template('times.html', time=time)

@app.route('/time/<timeID>')
def time(timeID):
    thisTime = TimeProc.objects.get(id=timeID)
    return render_template('time.html',time=thisTime)

@app.route('/time/edit/<timeID>', methods=['GET', 'POST'])
def timeEdit():
    editTime = TimeProc.objects.get(id=timeID)
    if current_user !=editTime.author:
            flash("You can't edit a time timeID you don't own.")
            return redirect(url_for('time',timeID=timeID))
    form = TimeProcForm()
    if form.validate_on_submit():
        editTime.update(
            subject = form.subject.data,
            content = form.content.data,
            modifydate = dt.datetime.utcnow
        )
        return redirect(url_for('post',timeID=timeID))
    form.subject.data = editTime.subject
    form.content.data = editTime.content
    return render_template('timeprocform.html',form=form)

@app.route('/time/new', methods=['GET', 'POST'])
@login_required
def timeNew():
    currUser = User.objects.get(id=current_user.id)

    form = TimeProcForm()
    if form.validate_on_submit():
        print("validated")
        currUser.update(
            procrastinatedTime = form.procrastinatedTime.data,
            proc = form.proc.data
        )
        return redirect(url_for('myProfile'))

    form.proc.data = current_user.proc
    form.procrastinatedTime.data = current_user.procrastinatedTime

    return render_template('timeprocform.html',form=form)