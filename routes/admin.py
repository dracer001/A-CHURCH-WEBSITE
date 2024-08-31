import functools
import io
import json
from flask import Blueprint, url_for, render_template, request, redirect, flash, g, session, \
    send_file, make_response
from controllers import admin as Admin
from controllers import ebook as Ebook
from controllers import audio as Audio
from controllers import event as Event

admin = Blueprint('admin', 'admin', url_prefix='/admin')


def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.admin is None:
            return redirect(url_for('admin.login_route'))
        elif g.admin["barn"]:
            return redirect(url_for("admin.barn_error_route"))
        return view(**kwargs)
    return wrapped_view


def check_super_user(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.admin["s_user"]:
            flash("super admin user auth required")
            return redirect(url_for('admin.login_route'))
        return view(**kwargs)

    return wrapped_view


@admin.before_app_request
def authUser():
    return Admin.authAdmin()


@admin.route('/error')
@admin_required
def barn_error_route():
    return render_template('error/barn.html', user=g.admin)


@admin.route('')
@admin_required
def index_admin():
    return render_template('admin/home.html', user=g.admin)


@admin.route('/reset/<field>/<value>')
def reset_route(field, value):
    return "reset successful" if Admin.reset(field, list()) else "error occured"

@admin.route('/audio/reset/<field>/<value>')
def audio_reset(field, value):
    return "reset successful" if Audio.reset(field, "") else "error occured"


@admin.route('/event/reset/')
def event_reset():
    return "reset successful" if Event.reset("form_id", None) else "error occured"


@admin.route('/auth/login', methods=('POST', 'GET'))
def login_route():
    if request.method == 'POST':
        if (message := Admin.loginAdmin(request.form)) != True:
            flash(message, category="error")
            return redirect(url_for('admin.login_route'))
        flash("login successful", category="success")
        return redirect(url_for('admin.index_admin'))
    return render_template('admin/login.html')


@admin.route('/logout')
def logout_route():
    session.clear()
    return redirect(url_for('admin.index_admin'))


@admin.route('/auth/create-super', methods=('POST', 'GET'))
def create_super_route():
    if request.method == 'POST':
        if (message := Admin.createAdminUser(request.form, True)) != True:
            flash(message, category="error")
            return redirect(url_for('admin.login_route'))
        flash("Super User Created", category="success")
        return redirect(url_for('admin.login_route'))
    if message := Admin.getSuperUser():
        return redirect(url_for('admin.login_route'))
    return render_template('admin/create_super.html')


@admin.route('/profile', methods=('POST', 'GET'))
@admin_required
def edit_admin_route():
    if request.method == 'POST':
        if (message := Admin.editAdminUser(request.form, g.admin["_id"])) != True:
            flash(message, category="errror")
            return redirect(url_for('admin.edit_admin_route'))
        flash("Profile updated successfully", category="success")
        return redirect(url_for('admin.edit_admin_route'))
    return render_template('admin/profile.html', user=g.admin)

@admin.route('/delete-info', methods=('POST', 'GET'))
def delete_admin_route():
    if request.method == 'POST':
        if (message := Admin.deleteAdminUser(g.admin._id)) != True:
            flash(message)
            return redirect(url_for('admin.delete_admin_route'))
        flash("delete succesful")
        return redirect(url_for('admin.login_route'))
    return render_template('admin/delete_admin.html')


@admin.route('/super/get-admins')
@admin_required
@check_super_user
def get_admin_route():
    admins = [admin for admin in Admin.getAdminUsers() if not admin.get("s_user")]
    return render_template('admin/get_admins.html', user=g.admin, admins=admins)


@admin.route('/super/add-admin', methods=('POST', 'GET'))
@admin_required
@check_super_user
def add_admin_route():
    if request.method == 'POST':
        if (message := Admin.createAdminUser(request.form)) != True:
            flash(message, category="error")
            return redirect(url_for('admin.add_admin_route'))
        flash("Admin added succesfully", category="success")
        flash("password = <code> <username> + 123</code>", category="success")
        return redirect(url_for('admin.add_admin_route'))
    return render_template('admin/add_admin.html', user=g.admin)


@admin.route('/super/barn-admin/<barn_id>', methods=('POST', 'GET'))
@admin_required
@check_super_user
def barn_admin_route(barn_id):
    barn_ids = barn_id.split(',')
    if (message := Admin.barnAdminUser(barn_ids)) == False:
        flash(message, category="error")
        return redirect(url_for('admin.get_admin_route'))
        # flash("delete succesful")
    return redirect(url_for('admin.get_admin_route'))


@admin.route('/super/unbarn-admin/<barn_id>', methods=('POST', 'GET'))
@admin_required
@check_super_user
def unbarn_admin_route(barn_id):
    barn_ids = barn_id.split(',')
    if (message := Admin.unBarnAdminUser(barn_ids)) == False:
        flash(message, category="error")
        return redirect(url_for('admin.get_admin_route'))
        # flash("delete succesful")
    return redirect(url_for('admin.get_admin_route'))


@admin.route('/e-books')
def get_ebooks_route():
    ebooks = Ebook.getAllEbook()
    return render_template("admin/ebooks.html", user=g.admin, ebooks=ebooks)


@admin.route('/e-book/<book_id>')
def get_ebook_route(book_id):
    ebook = Ebook.getEbook(book_id)
    return render_template("admin/ebook_detail.html", ebook=ebook)


@admin.route('/e-book/add', methods=("GET", "POST"))
def add_ebook_route():
    if request.method == 'POST':
        if (message := Ebook.addEbook(request.form.to_dict(), request.files.to_dict())) != True:
            flash(message, category="error")
            return redirect(url_for('admin.add_ebook_route'))
        flash("1 record added", category="success")
        return redirect(url_for('admin.add_ebook_route'))
    return render_template("admin/ebook_add.html", user=g.admin)


@admin.route('/e-book/edit/<book_id>', methods=("GET", "POST"))
def edit_ebook_route(book_id):
    if request.method == 'POST':
        if (message := Ebook.editEbook(book_id, request.form.to_dict(), request.files.to_dict())) != True:
            flash(message, category="error")
            return redirect(url_for('admin.edit_ebook_route', book_id=book_id))
        flash("edith successful", category="success")
        return redirect(url_for('admin.edit_ebook_route', book_id=book_id))
    ebook = Ebook.getEbook(book_id)
    return render_template("admin/ebook_edit.html", user=g.admin, ebook=ebook)


@admin.route('/e-book/delete/<book_id>', methods=("GET", "POST"))
def delete_ebook_route(book_id):
    if (message := Ebook.deleteEbook(book_id)) != True:
        flash(message, category="error")
    flash("delete successful", category="success")
    return redirect(url_for('admin.get_ebooks_route', book_id=book_id))


@admin.route('/ebook/download/<ebook_id>')
def download_ebook_route(ebook_id):
    file_data, grid_out = Ebook.get_file(ebook_id)
    if file_data and grid_out:
        content_type = grid_out.content_type
        response = make_response(file_data)
        response.headers.set('Content-Type', content_type)
        response.headers.set('Content-Disposition', 'inline', filename=grid_out.filename)
        return response
    else:
        return "File not found", 404



@admin.route('/audio')
@admin_required
def get_audios_route():
    audios = Audio.getAllAudio()
    return render_template("admin/audios.html", user=g.admin, audios=audios)


@admin.route('/audio/<audio_id>')
@admin_required
def get_audio_route(audio_id):
    audio = Audio.getAudio(audio_id)
    return render_template("admin/audio_detail.html", audio=audio)


@admin.route('/audio/add', methods=("GET", "POST"))
@admin_required
def add_audio_route():
    if request.method == 'POST':
        if (message := Audio.addAudio(request.form.to_dict(), request.files.to_dict())) != True:
            flash(message, category="error")
            return redirect(url_for('admin.add_audio_route'))
        flash("1 record added", category="success")
        return redirect(url_for('admin.add_audio_route'))
    return render_template("admin/add_audio.html", user=g.admin)


@admin.route('/audio/edit/<audio_id>', methods=("GET", "POST"))
def edit_audio_route(audio_id):
    if request.method == 'POST':
        if (message := Audio.editAudio(audio_id, request.form.to_dict(), request.files.to_dict())) != True:
            flash(message, category="error")
            return redirect(url_for('admin.edit_audio_route', audio_id=audio_id))
        flash("edith successful", category="success")
        return redirect(url_for('admin.edit_audio_route', audio_id=audio_id))
    audio = Audio.getAudio(audio_id)
    return render_template("admin/edit_audio.html", user=g.admin, audio=audio)


@admin.route('/audio/delete/<audio_id>', methods=("GET", "POST"))
def delete_audio_route(audio_id):
    if (message := Audio.deleteAudio(audio_id)) != True:
        flash(message, category="error")
    flash("delete successful", category="success")
    return redirect(url_for('admin.get_audios_route'))


@admin.route('/audio/download/<audio_id>')
def download_audio_route(audio_id):
    file_data, grid_out = Audio.get_file(audio_id)
    if file_data and grid_out:
        content_type = grid_out.content_type
        response = make_response(file_data)
        response.headers.set('Content-Type', content_type)
        response.headers.set('Content-Disposition', 'inline', filename=grid_out.filename)
        return response
    else:
        return "File not found", 404

    # audio_data = Audio.get_file(audio_id)
    # return send_file(io.BytesIO(audio_data.read()), as_attachment=True)


### EVENTS ###


@admin.route('/events')
@admin_required
def get_events_route():
    events = Event.getAllEvents()
    return render_template("admin/events.html", user=g.admin, events=events)

@admin.route('/event/add', defaults={'action_page': None}, methods=("GET", "POST"))
@admin.route('/event/add/<action_page>', methods=("GET", "POST"))
@admin_required
def add_event_route(action_page):
    if request.method == 'POST':
        message, event_id = Event.addEvent(request.form.to_dict(), request.files.to_dict())
        if message != True:
            flash(message, category="error")
            return redirect(url_for('admin.add_event_route'))
        flash("1 record added", category="success")
        return redirect(url_for('admin.add_reg_form_route', event_id=event_id)) if(action_page == 'next') else redirect(url_for('admin.add_event_route'))
    return render_template("admin/event_add.html", user=g.admin)


@admin.route('/event-reg/add/<event_id>', methods=("GET", "POST"))
@admin_required
def add_reg_form_route(event_id):
    if request.method == 'POST':
        json_data = request.form['reg-form']
        parsed_data = json.loads(json_data)  # Convert JSON string to Python dictionary
        message, form_id = Event.createEventForm(parsed_data, event_id)
        if message != True:
            flash(message, category="error")
            return redirect(url_for('admin.add_event_route'))
        flash("1 record added", category="success")
        return redirect(url_for("admin.event_complete_route", event_id=event_id))
    return render_template("admin/event_add_reg.html", user=g.admin, event_id=event_id)


@admin.route('/event/preview/<event_id>')
@admin_required
def event_complete_route(event_id):
    event = Event.getEvent(event_id)
    form = Event.getEventFormByEvent_id(event_id)
    return render_template("admin/event_regform_preview.html", user=g.admin, event=event, form=form)


@admin.route('/event/edit/<event_id>', methods=("GET", "POST"))
@admin_required
def edit_event_route(event_id):
    if request.method == 'POST':
        message = Event.editEvent(event_id, request.form.to_dict(), request.files.to_dict())
        if message != True:
            flash(message, category="error")
            return redirect(url_for('admin.edit_event_route', event_id=event_id))
        flash("event edit successfull", category="success")
        return redirect(url_for('admin.edit_event_route', event_id=event_id))

    event = Event.getEvent(event_id)
    return render_template("admin/event_edit.html", user=g.admin, event=event)


@admin.route('/event-reg/edit/<event_id>', methods=("GET", "POST"))
@admin_required
def edit_reg_form_route(event_id):
    if request.method == 'POST':
        json_data = request.form['reg-form']
        form_id = request.form['form_id']
        parsed_data = json.loads(json_data)  # Convert JSON string to Python dictionary
        message = Event.editEventForm(form_id, {"form": parsed_data})
        if message != True:
            flash(message, category="error")
            return redirect(url_for('admin.edit_reg_form_route', event_id=event_id))
        flash("Event Registration form edited successful", category="success")
        return redirect(url_for('admin.edit_reg_form_route', event_id=event_id))
    form = Event.getEventFormByEvent_id(event_id)
    return render_template("admin/event_edit_reg.html", user=g.admin, form=form, event_id=event_id)


@admin.route('/event/delete/<event_id>', methods=("GET", "POST"))
def delete_event_route(event_id):
    if (message := Event.deleteEvent(event_id)) != True:
        flash(message, category="error")
        return redirect(url_for('admin.get_events_route'))
    flash("delete successful", category="success")
    return redirect(url_for('admin.get_events_route'))


@admin.route('/event-reg/delete/<form_id>/<event_id>', methods=("GET", "POST"))
def delete_event_reg_route(form_id, event_id=None):
    if (message := Event.deleteEventForm(form_id)) != True:
        flash(message, category="error")
        return redirect(url_for('admin.event_complete_route', event_id=event_id)) if event_id else \
            redirect(url_for('admin.get_events_route'))
    flash("form delete successful", category="success")
    return redirect(url_for('admin.event_complete_route', event_id=event_id)) if event_id else \
        redirect(url_for('admin.get_events_route'))


@admin.route('/event/download/<event_id>')
def download_event_route(event_id):
    file_data, grid_out = Event.get_file(event_id)
    if file_data and grid_out:
        content_type = grid_out.content_type
        response = make_response(file_data)
        response.headers.set('Content-Type', content_type)
        response.headers.set('Content-Disposition', 'inline', filename=grid_out.filename)
        return response
    else:
        return "File not found", 404


@admin.route('/event/register/', methods=('POST',))
def register_for_event_route():
    form_data = request.form.to_dict()
    event_id = form_data['event_id']
    del form_data['event_id']
    form_id = form_data['form_id']
    del form_data['form_id']
    if (message := Event.addEventReg(event_id, form_id, form_data)) != True:
        flash(message, category="error")
        return redirect(url_for('admin.event_complete_route', event_id=event_id))
    flash("registration successful", category="success")
    return redirect(url_for('admin.event_complete_route', event_id=event_id))


@admin.route('/event/get-registrations/<event_id>')
def get_event_registration_route(event_id):
    registration = Event.getAllEventReg(event_id)
    form = Event.getEventFormByEvent_id(event_id)
    return render_template('admin/event_registrations.html', user=g.admin, form=form, registration=registration)
