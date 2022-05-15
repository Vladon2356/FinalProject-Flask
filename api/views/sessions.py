from flask import jsonify, request, Blueprint

from cinema.models.session import SessionModel

sessions_api_bp = Blueprint("sessions_api", __name__)


@sessions_api_bp.route("/", methods=["GET"])
def get_sessions():
    sessions = SessionModel.return_all(to_dict=True)
    return jsonify(sessions)


@sessions_api_bp.route("/<int:session_id>", methods=["GET"])
def get_session(session_id):
    session = SessionModel.find_by_id(id=session_id, to_dict=True)
    if not session:
        return jsonify({"message": "Session not found."}), 404

    return jsonify(session)
