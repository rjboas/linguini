from flask import Blueprint, render_template, abort, request, #redirect, url_for, flash
from linguini.models import User, EventModel, NoticeModel
from linguini.database import db_session
from linguini.utils import has_role, in_pc

bp = Blueprint('dashboard', __name__)

@bp.route('/')
def index():
    notices_list = db_session.query(NoticeModel).all()
    events_list = db_session.query(EventModel).all()
    return render_template('dashboard/index.html', notices=notices_list, events=events_list)


@bp.route('/create', methods=['GET', 'POST'])
@has_role(['staff', 'admin'])
def create():
    if request.method == 'POST':
        return abort(501)
    return render_template('dashboard/create.html')

# Errors
@bp.errorhandler(501)
def handle501(error):
    return render_template('501.html')

# Notices
@bp.route('/notices')
def notices():
    notices_list = db_session.query(NoticeModel).all()
    return render_template('dashboard/notices.html', notices=notices_list)


@bp.route('/notice/<int:notice_id>')
def notice_detail(notice_id):
    notice = db_session.query(NoticeModel).filter_by(id=notice_id).first()
    if notice:
        return render_template('dashboard/notice_detail.html', notice=notice)
    return abort(404)


@bp.route('/notice/<int:notice_id>/update', methods=['GET', 'POST'])
@has_role(['staff', 'admin'])
def notice_update(notice_id):
    return abort(501)

# Events
@bp.route('/events')
def events():
    events_list = db_session.query(EventModel).all()
    return render_template('dashboard/events.html', events=events_list)


@bp.route('/event/<int:event_id>')
def event_detail(event_id):
    event = db_session.query(EventModel).filter_by(id=event_id).first()
    if event:
        return render_template('dashboard/event_detail.html', event=event)
    return abort(404)


@bp.route('/event/<int:event_id>/update', methods=['GET', 'POST'])
@has_role(['staff', 'admin'])
def event_update(event_id):
    return abort(501)
