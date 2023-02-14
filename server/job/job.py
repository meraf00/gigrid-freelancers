import os
import json
from flask import Blueprint, render_template, request, jsonify, make_response, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user
from utils import FileManager
from uuid import uuid4

from model import User, UserType, Job, Attachment, File, db


job_bp = Blueprint('job_bp', __name__,
                   static_folder='static', template_folder='templates')

file_mgr = FileManager(os.getenv('UPLOAD_FOLDER'))


@job_bp.route('/')
@login_required
def job():
    message = request.args.get("message")
    if current_user.user_type == UserType.EMPLOYER:
        return render_template('post_job.html', message=message)
    else:
        return render_template('filter_job.html', message=message)


@job_bp.route('/', methods=['POST'])
@login_required
def post():
    id = uuid4()
    title = request.form.get("title")
    description = request.form.get("description")
    experience_level = request.form.get("experience-level")
    budget = request.form.get("budget")
    owner_id = current_user.id

    new_job = Job(id=id, title=title, description=description,
                  experience_level=experience_level,
                  budget=budget, owner_id=owner_id
                  )

    db.session.add(new_job)
    db.session.commit()

    return redirect(url_for('job_bp.job', message="Job posted successfully."))


@job_bp.route('/myjobs', methods=['GET'])
@login_required
def see_posted_jobs():
    jobs = current_user.get_posted_jobs()
    jsonList = []

    for job in jobs:
        jsonList.append({"id": job.id,
                         "title": job.title,
                         "description": job.description,
                         "experience_level": job.experience_level,
                         "owner_id": job.owner_id,
                         "budget": job.budget
                         })
    response = make_response(
        jsonify(jsonList),
        200
    )
    response.headers["Content-Type"] = "application/json"
    return response


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
