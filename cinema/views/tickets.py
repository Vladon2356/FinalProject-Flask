from flask import Blueprint, render_template, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from cinema.models.users import UserModel
from cinema.models.session import SessionModel
from cinema.models.tickets import TicketModel
from ..decorators import admin_group_required

tickets_bp = Blueprint("tickets", __name__)


@tickets_bp.route("/<int:ticket_id>", methods=["GET"])
def get_ticket_by_id(ticket_id):
    """Return page with ticket by id"""
    ticket = TicketModel.find_by_id(id=ticket_id, to_dict=False)

    return render_template("cinema/tickets/ticket_detail.html", ticket=ticket)


@tickets_bp.route("/buy/<int:session_id>", methods=["GET", "POST"])
@jwt_required
def buy_ticket_for_session(session_id):
    """Return page with ticket by sessein with id - session_id"""
    session = SessionModel.find_by_id(id=session_id, to_dict=False)
    current_user_identity = get_jwt_identity()
    user = UserModel.find_by_first_and_last_name(current_user_identity, to_dict=False)

    if request.method == "GET":
        return render_template("cinema/tickets/ticket_buy.html", session=session)

    row = int(request.form.get("row"))
    column = int(request.form.get("column"))
    message = TicketModel.reserve_ticket(
        session_id=session_id, row=row, column=column, owner_id=user.id
    )
    return render_template(
        "cinema/tickets/ticket_message.html", message=message, user=user
    )


@tickets_bp.route("/sold/", methods=["GET"])
@jwt_required()
@admin_group_required
def get_all_sold_tickets():
    """Return page with all sold tickets"""

    tickets = TicketModel.return_all_sold(to_dict=False)

    return render_template("cinema/tickets/ticket_list.html", tickets=tickets)


@tickets_bp.route("/active/", methods=["GET"])
@jwt_required()
@admin_group_required
def get_all_active_tickets():
    """Return page with all active tickets"""

    tickets = TicketModel.return_all_active(to_dict=False)
    return render_template("cinema/tickets/ticket_list.html", tickets=tickets)
