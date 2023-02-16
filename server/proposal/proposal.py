import os
from uuid import uuid4
from flask import Blueprint, render_template, request, jsonify, make_response, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError

from utils import FileManager
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
    if current_user.user_type != UserType.FREELANCER:
        return redirect(url_for("home"))

    job_id = request.form.get("job_id")
    content = request.form.get("content")
    attachment = request.files.get("attachment")

    if Job.get(job_id):
        attachment_id = None

        file_id = None
        if attachment:
            file_id = file_mgr.save(attachment)

            attachment_id = uuid4()
            new_attachement = Attachment(attachment_id, file_id)
            db.session.add(new_attachement)

        new_proposal = Proposal(
            worker_id=current_user.id,
            job_id=job_id,
            content=content,
            attachment_id=attachment_id
        )

        try:
            db.session.add(new_proposal)
            db.session.commit()
            return "OK"
        except IntegrityError:
            db.session.rollback()
            return "NOT OK"
    return "Not ok"


@proposal_bp.route("/create/<job_id>")
@login_required
def create_proposal(job_id):
    if current_user.user_type == UserType.FREELANCER:
        job = Job.get(job_id)
        if job:
            return render_template("proposal.html", job=job)
        
    return redirect(url_for("job_bp.search"))
