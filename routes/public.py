from flask import Blueprint, url_for, render_template, request, redirect, flash
from controllers import event as Event
from controllers import blog as Blog
from controllers import audio as Audio
from controllers import ebook as Ebook
from controllers import counseling as CS
public = Blueprint('public', 'public', url_prefix='')


@public.route('/')
def index_route():
    blog = Blog.getBlog("66aaac3606feeffa6d3456d9")
    audio = Audio.getAllAudio()[0]
    ebook = Ebook.getAllEbook()[2]
    # ebook = Ebook.getEbook("669854629ca849e3082829f0")
    return render_template("/public/index.html", blog=blog, audio=audio, ebook=ebook)


@public.route('/about')
def about_route():
    return render_template("/public/about.html")


# @public.route('/event')
# def event_route():
#     events = Event.getAllEvents()
#     return render_template("/public/event.html", events=events)


@public.route('/event/<event_id>')
def view_event_route(event_id):
    event = Event.getEvent(event_id)
    form = Event.getEventFormByEvent_id(event_id)
    return render_template("/public/event_page.html", event=event, form=form)


@public.route('/event')
def event_route():
    order = sort = value = ''
    search = request.args.get('search', '')
    if search == 'true':
        sort = request.args.get('field', '')
        fields = ('title', 'tags', 'post-date')
        value = request.args.get('query', '')
        order = request.args.get('order', '')

        if sort == 'a-z':
            sort_key = 'title'
        else:
            sort_key = 'date'
            print(value)
        events = Event.searchEvent(value, fields, sort_key, order)
    else:
        events = Event.getAllEvents()
    for event in events:
        print(event['date'] == '2024-07-01')
    return render_template("/public/event.html", events=events,
                           order=order, sort=sort, query=value)


@public.route('/audios')
def audios_route():
    audios = Audio.getAllAudio()
    return render_template("/public/audios.html", audios=audios)


@public.route('/e-books')
def ebooks_route():
    order = sort = value = ''
    search = request.args.get('search', '')
    if search == 'true':
        sort = request.args.get('field', '')
        fields = ('title', 'tags')
        value = request.args.get('query', '')
        order = request.args.get('order', '')

        if sort == 'author':
            sort_key = 'author'
        elif sort == 'most downloaded':
            sort_key = 'views'
        else:
            sort_key = 'title'
            print(value)
        ebooks = Ebook.searchEbooks(value, fields, sort_key, order)
    else:
        ebooks = Ebook.getAllEbook()
    return render_template("/public/ebooks.html", ebooks=ebooks,
                           order=order, sort=sort, query=value)


@public.route('/book-counseling', methods=('POST',))
def book_counseling():
    data = request.form.to_dict()
    message = CS.addSession(data)
    if message != True:
        flash(message, category="error")
        return redirect('/about#book-session')
    flash("Session as been booked and a confirmation mail will be sent to your email", category="success")
    return redirect('/about#book-session')
