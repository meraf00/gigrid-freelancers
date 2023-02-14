from uuid import uuid4
from flask import Blueprint, render_template, request, jsonify, make_response, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from model import User, Job, ContractStatus, Contract, db


contract_bp = Blueprint('contract_bp', __name__,
                        static_folder='static', template_folder='templates')


@contract_bp.route("/", methods=["POST"])
@login_required
def create_contract():
    job_id = request.form.get("job_id")
    worker_id = request.form.get("worker_id")
    deadline = datetime.strptime(request.form.get("deadline"), "%Y-%m-%d")

    job = Job.get(job_id)
    worker = User.get(worker_id)

    if job.owner.id != current_user.id:
        return "Unauthorized"

    if job and worker and not Contract.already_exists(job_id, worker_id):
        new_contract = Contract(id=uuid4(),
                                job_id=job_id, worker_id=worker_id, deadline=deadline)

        try:
            db.session.add(new_contract)
            db.session.commit()
        except IntegrityError:
            return "Contract exists"

        return "OK"

    return "Error"


@contract_bp.route("/<contract_id>/<response>")
@login_required
def accept_or_reject_contract(contract_id, response):
    contract = Contract.get(contract_id)

    if contract.status != None:
        return "Unauthorized"

    if contract.worker_id == current_user.worker_id:
        if response == "accept":
            contract.status = ContractStatus.ACCEPTED
        elif response == "reject":
            contract.status = ContractStatus.REJECTED
        db.session.commit()

        return redirect(url_for("contract_bp.contracts"))

    return "Unauthorized"
