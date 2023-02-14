import os
import json
from flask import Blueprint, render_template, request, jsonify, make_response, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user
from utils import FileManager
from uuid import uuid4

from model import User, UserType, Proposal, Attachement, File, db


proposal_bp = Blueprint('proposal_bp', __name__,
                        static_folder='static', template_folder='templates')

file_mgr = FileManager(os.getenv('UPLOAD_FOLDER'))


@proposal_bp.route("/")
@login_required
def get_my_proposals():
    print(current_user.proposals)
    for proposal in current_user.proposals:
        print(proposal)
    return " "
