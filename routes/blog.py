import functools
import json
from datetime import datetime

from flask import Blueprint, url_for, render_template, request, redirect, flash, g, session, make_response, jsonify

from controllers import blog as Blog
blog = Blueprint('blog', 'blog', url_prefix='/blog')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('blog.login_route'))
        return view(**kwargs)
    return wrapped_view


@blog.before_app_request
def authUser():
    return Blog.authBlogger()


@blog.route('/reset')
def resetBlogger():
    return "successful" if Blog.resetAllBlogger() else "error"


@blog.route('/register', methods=('GET', 'POST'))
def register_route():
    if request.method == 'POST':
        data = request.form.to_dict()
        status, message = Blog.createBlogger(data)
        if not status:
            flash(message, category="error")
            return redirect(url_for('blog.register_route'))
        session['blogger_id'] = str(message)
        return redirect(url_for('blog.home_route'))
    return render_template("/blog/register.html")


@blog.route('/sign-in', methods=('GET', 'POST'))
def login_route():
    if request.method == 'POST':
        data = request.form.to_dict()
        status, message = Blog.loginBlogger(data)
        if not status:
            flash(message, category="error")
            return redirect(url_for('blog.login_route'))
        flash("login successful", category="success")
        session['blogger_id'] = str(message)
        return redirect(url_for('blog.home_route'))

    return render_template("/blog/login.html")


@blog.route('/sign-out')
def signout_route():
    session.clear()
    return redirect(url_for('blog.home_route'))


@blog.route('/')
def home_route():
    order = sort = value = ''
    search = request.args.get('search', '')
    if search == 'true':
        sort = request.args.get('field', '')
        fields = ('title', 'tags', 'post-date')
        value = request.args.get('query', '')
        order = request.args.get('order', '')

        if sort == 'a-z':
            sort_key = 'title'
        elif sort == 'most read':
            sort_key = 'title'
        else:
            sort_key = 'post-date'

        reverse = True if order == 'on' else False
        blogs = Blog.searchBlog(value, fields, sort_key, order)
        possible_blogger = Blog.searchBlogger(value, ('full-name', 'username'))
        print(possible_blogger)
        for x in possible_blogger:
            x_blog = Blog.getBloggerBlog(x['_id'])
            blogs = blogs + x_blog
            blogs = list({d['_id']: d for d in sorted(blogs, key=lambda i: i[sort_key], reverse=reverse)}.values())
            print(x['_id'], x_blog)
            # blogs.extend(x_blog)
            # for i in x_blog:
            #     blogs.append(i) if i not in blogs else ''
            # blogs.sort()
    else:
        blogs = Blog.getAllBlog()
    return render_template("/blog/home.html", user=g.user, blogs=blogs, id="blog-view-page",
                           order=order, sort=sort, query=value)


@blog.route('/create', methods=('GET', 'POST'))
@login_required
def create_blog_route():
    if request.method == 'POST':
        data = request.form.to_dict()
        blog_content = data["blog-content"]
        blog_content = json.loads(blog_content)  # Convert JSON string to Python dictionary
        data["content"] = blog_content
        del data["blog-content"]
        files = request.files.to_dict()
        status, message = Blog.addBlog(data, files)
        if not status:
            flash(message, category="error")
            return redirect(url_for('blog.create_blog_route'))
        return redirect(url_for('blog.view_blog_route', blog_id=message))
    return render_template('/blog/create.html', user=g.user)


@blog.route('/view/<blog_id>')
def view_blog_route(blog_id):
    blog_post = Blog.getBlog(blog_id)
    blogger = Blog.getBlogger(blog_post['blogger'])
    return render_template('/blog/view.html', user=g.user, blog=blog_post, blogger=blogger)


@blog.route('/my-blog-space')
@login_required
def blog_space_route():
    order = sort = value = ''
    search = request.args.get('search', '')
    if search == 'true':
        sort = request.args.get('field', '')
        fields = ('title', 'tags', 'post-date')
        value = request.args.get('query', '')
        order = request.args.get('order', '')

        if sort == 'a-z':
            sort_key = 'title'
        elif sort == 'most read':
            sort_key = 'title'
        else:
            sort_key = 'post-date'

        blogs = Blog.searchBloggerBlog(g.user['_id'], value, fields, sort_key, order)
    else:
        blogs = Blog.getBloggerBlog(g.user['_id'])
    return render_template('/blog/home.html', user=g.user, blogs=blogs, id="blogger-space-page",
                           order=order, sort=sort, query=value)


@blog.route('/profile/<blogger_id>', methods=('GET', 'POST'))
def view_profile_route(blogger_id):
    if request.method == 'POST':
        if 'user' in g:
            if str(g.user['_id']) == blogger_id:
                data = request.form.to_dict()
                files = request.files.to_dict()
                if (message := Blog.editBlogger(blogger_id, data, files)) != True:
                    flash(message, category="error")
                    return redirect(url_for('blog.view_profile_route', blogger_id=blogger_id))
                flash("update successful", category="success")
                return redirect(url_for('blog.view_profile_route', blogger_id=blogger_id))
            flash("unauthorized access", category="error")
            return redirect(url_for('blog.view_profile_route', blogger_id=blogger_id))
        return redirect(url_for('blog.login_route'))
    blogger = Blog.getBlogger(blogger_id)
    return render_template('/blog/profile.html', user=g.user, blogger=blogger)


@blog.route('/profile/change-password', methods=('GET', 'POST'))
@login_required
def password_route():
    if request.method == 'POST':
        old_password = request.form['old-password']
        new_password = request.form['new-password']
        if (message := Blog.changePassword(str(g.user['_id']), old_password, new_password)) != True:
            flash(message, category="error")
            return redirect(url_for('blog.password_route'))
        flash("update successful", category="success")
        return redirect(url_for('blog.password_route'))
    return render_template('/blog/password.html', user=g.user)


@blog.route('/blog_image_download/<image_id>')
def blog_image_download(image_id):
    file_data, grid_out = Blog.get_blog_img(image_id)
    if file_data and grid_out:
        content_type = grid_out.content_type
        response = make_response(file_data)
        response.headers.set('Content-Type', content_type)
        response.headers.set('Content-Disposition', 'inline', filename=grid_out.filename)
        return response
    else:
        return "File not found", 404
