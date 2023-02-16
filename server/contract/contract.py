from uuid import uuid4
from flask import Blueprint, render_template, request, jsonify, make_response, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from model import User, Job, ContractStatus, Contract, Escrow, UserType, db


contract_bp = Blueprint('contract_bp', __name__,
                        static_folder='static', template_folder='templates')


@contract_bp.route("/", methods=["POST"])
@login_required
def create_contract():
    job_id = request.form.get("job_id")
    worker_id = request.form.get("worker_id")
    budget = request.form.get("budget")
    deadline = datetime.strptime(request.form.get("deadline"), "%Y-%m-%d")

    try:
        if current_user.balance < float(budget):
            return render_template("contract.html", message="Insufficient balance to set up escrow.", status=400)
    except:
        return render_template("contract.html", message="Insufficient balance to set up escrow.", status=400)

    job = Job.get(job_id)
    worker = User.get(worker_id)

    if job.owner.id != current_user.id:
        return redirect(url_for('login'))

    if job and worker and not Contract.already_exists(job_id, worker_id):
        contract_id = uuid4()

        new_contract = Contract(id=contract_id,
                                job_id=job_id, worker_id=worker_id, deadline=deadline)

        new_escrow = Escrow(id=uuid4(),
                            contract_id=contract_id, amount=float(budget))

        try:
            db.session.add(new_contract)
            db.session.add(new_escrow)
            current_user.balance -= float(budget)
            db.session.commit()

        except IntegrityError:
            return render_template("contract.html", message="Contract already exists.", status=400)

        return render_template("contract.html", status=200, worker=worker)

    return render_template("contract.html", message="Contract already exists.", status=400)


@contract_bp.route("/<contract_id>/<response>")
@login_required
def accept_or_reject_contract(contract_id, response):
    contract = Contract.get(contract_id)

    if contract.status != None:
        return "Unauthorized"

    if contract.worker_id == current_user.id:
        if response == "accept":
            contract.status = ContractStatus.ACCEPTED
            contract.escrow[0].date_of_initiation = datetime.now()
        elif response == "reject":
            contract.status = ContractStatus.REJECTED
            db.session.delete(contract)
        db.session.commit()

        return redirect(url_for("contract_bp.contracts"))

    return "Unauthorized"


@contract_bp.route("/")
@login_required
def contracts():
    if current_user.user_type == UserType.EMPLOYER:
        return render_template("employer.html")

    return render_template("freelancer.html")
