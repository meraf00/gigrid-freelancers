import os
import json
from flask import Blueprint, render_template, request, jsonify, make_response, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError

from utils import FileManager
from uuid import uuid4
from model import User, Job, UserType, Proposal, Attachment, File, db


proposal_bp = Blueprint('proposal_bp', __name__,
                        static_folder='static', template_folder='templates')

file_mgr = FileManager(os.getenv('UPLOAD_FOLDER'))


@proposal_bp.route("/")
@login_required
def get_my_proposals():
    proposals = []

    if current_user.user_type == UserType.FREELANCER:
        for proposal in current_user.proposals:
            files = []
            if proposal.attachments:
                file_ids = [
                    attachment.file_id for attachment in proposal.attachments]

                files = map(File.get, file_ids)
                files = [
                    {
                        "file_name": file.file_name,
                        "file_link": url_for('files', id=file.id)
                    }
                    for file in files
                ]
            proposals.append(
                {
                    "job_id": proposal.job_id,
                    "sent_time": proposal.sent_time,
                    "content": proposal.content,
                    "files": files
                }
            )

        response = make_response(
            jsonify(proposals),
            200
        )
        response.headers["Content-Type"] = "application/json"

        return response

    response = make_response(
        jsonify("Unauthorized"),
        401
    )

    return response


@proposal_bp.route("/<job_id>")
@login_required
def get_job_proposals(job_id):
    if current_user.user_type == UserType.EMPLOYER:
        job = Job.query.filter(
            Job.owner_id == current_user.id,
            Job.id == job_id
        ).one()

        proposals = []

        for proposal in job.proposals:
            file_ids = [
                attachment.file_id for attachment in proposal.attachments]

            files = map(File.get, file_ids)
            files = [
                {
                    "file_name": file.file_name,
                    "file_link": url_for('files', id=file.id)
                }
                for file in files
            ]
            proposals.append(
                {
                    "job_id": proposal.job_id,
                    "sent_time": proposal.sent_time,
                    "content": proposal.content,
                    "files": files
                }
            )

        response = make_response(
            jsonify(proposals),
            200
        )
        response.headers["Content-Type"] = "application/json"

        return response

    response = make_response(
        jsonify("Unauthorized"),
        401
    )

    return response


@proposal_bp.route("/", methods=['POST'])
@login_required
def send_proposal():
    if current_user.user_type == UserType.FREELANCER:
        job_id = request.form.get("job_id")
        content = request.form.get("content")

        if Job.get(job_id):
            new_proposal = Proposal(
                worker_id=current_user.id,
                job_id=job_id,
                content=content
            )

            try:
                db.session.add(new_proposal)
                db.session.commit()
                return "OK"
            except IntegrityError:
                db.session.rollback()
                return "NOT OK"
        return "Not ok"

    return "Unauthorized"