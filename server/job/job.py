import os
import json
from flask import Flask, Blueprint, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user
from utils import FileManager

from model import User, UserType, Job, Attachement, File


job_bp = Blueprint('job_bp', __name__,
                    static_folder='static', template_folder='templates')

file_mgr = FileManager(os.getenv('UPLOAD_FOLDER'))


@job_bp.route('/')
@login_required
def job():
    if current_user.user_type == UserType.EMPLOYER:
        return render_template('post_job.html')
    else:
        return render_template('filter_job.html')



@job_bp.route('/post', methods=['POST'])
@login_required
def post():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        experience_level = request.form.get("experience-level")
        budget = request.form.get("budget")
        duration = request.form.get("duration")

        new_job = Job(title=title, description=description, 
                        experience_level=experience_level,
                        budget=budget, duration=duration
        )

        db.session.add(new_job)
        db.session.commit()


@job_bp.route('/uploadfile', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return ""

    file = request.files['file']
    if file and file.filename:
        file_id = file_mgr.save(file)
        return json.dumps({'status': 'success', 'file_id': file_id})

    return json.dumps({'status': 'failure'})
