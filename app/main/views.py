#!/usr/bin/env python
# coding=utf-8

from flask import render_template, request, flash, redirect, url_for, current_app, abort, g
from . import main
from .. import db
from ..models import Post, Comment, User
from flask_login import login_required, current_user
from .forms import CommentForm, PostForm
import json


@main.route('/')
def index():
    # posts=Post.query.all()

    page_index = request.args.get('page', 1, type=int)

    query = Post.query.order_by(Post.created.desc())

    pagination = query.paginate(page_index, per_page=20, error_out=False)

    posts = pagination.items

    return render_template('index.html',
                           title=u'你好，世界',
                           posts=posts,
                           pagination=pagination)


@main.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@main.route('/about')
def about():
    return render_template('about.html', title=u'关于')


@main.route('/posts/<int:id>', methods=['GET', 'POST'])
def post(id):
    # Detail 详情页
    post = Post.query.get_or_404(id)

    # 评论窗体
    form = CommentForm()

    # 保存评论
    if form.validate_on_submit():
        comment = Comment(author=current_user,
                          body=form.body.data,
                          post=post)
        db.session.add(comment)
        db.session.commit()

    return render_template('posts/detail.html',
                           title=post.title,
                           form=form,
                           post=post)


@main.route('/edit', methods=['GET', 'POST'])
@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id=0):
    form = PostForm()

    if id == 0:
        post = Post(author_id=current_user.id)
    else:
        post = Post.query.get_or_404(id)

    if form.validate_on_submit():
        post.body = form.body.data
        post.title = form.title.data

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('.post', id=post.id))

    form.title.data = post.title
    form.body.data = post.body

    title = (u'添加新文章')
    if id > 0:
        title = u'编辑 - %s' % post.title

    return render_template('posts/edit.html',
                           title=title,
                           form=form,
                           post=post)


@main.route('/shoutdown')
def shutdown():
    if not current_app.testing:
        abort(404)

    shoutdown = request.environ.get('werkzeug.server.shutdown')
    if not shoutdown:
        abort(500)

    shoutdown()
    return u'正在关闭服务端进程...'


@main.route("/projects")
def projects():
    return "hello world"


@main.route("/post_delete/<int:post_id>")
def post_delete(post_id):
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect(url_for('main.index'))


@main.errorhandler(500)
def internet_server_error(e):
    return render_template('500.html'), 500


@main.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

#@main.route('/post/<int:post_id>/delete',methods=['GET','POST'])
# def post_delete(post_id):
#    res = {
#        "status": 1,
#        "message": "success"
#    }
#    post = Post.query.get(post_id)
#    if not post:
#        res['status'] = 404
#        res["message"] = "Post Not Found"
#        return json.dumps(res)
#
#    Post.query.filter_by(id = post_id).delete()
#    db.session.commit()
#    return json.dumps(res)
