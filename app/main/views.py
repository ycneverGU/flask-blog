#!/usr/bin/env python
# coding=utf-8

from flask import render_template, request, flash, redirect, url_for, current_app, abort, g,jsonify
from . import main
from .. import db
from flask_login import login_required, current_user
from .forms import EditProfileForm, EditProfileAdminForm, PostForm,\
    CommentForm
from ..models import Permission, Role, User, Post, Comment,charts
from ..decorators import admin_required, permission_required
from ..data import out
from datetime import datetime
import json


@main.route('/mycharts')
def mycharts():
    return render_template('charts.html')

@main.route('/mychartstest')
def mychartstest():
    return render_template('chartstest.html')

@main.route('/data',methods=['GET','POST'])
def json():
    fs = charts.query.all()
    #s = out() 
    list = {'MQ2':[],'wendu':[],'shidu':[],'time':[]}

    for n in fs: 
        list["MQ2"].append(n["MQ2"])
        list["wendu"].append(n["wendu"])
        list["shidu"].append(n["shidu"])
        list["time"].append(n["time"])
    print(list) 
    return jsonify(list) 

    

@main.route('/')
def index():

    page_index = request.args.get('page', 1, type=int)

    query = Post.query.order_by(Post.created.desc())

    pagination = query.paginate(page_index, per_page=20, error_out=False)

    posts = pagination.items

    return render_template('index.html',
                           posts=posts,
                           pagination=pagination,
                           current_time=datetime.utcnow())


@main.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@main.route('/about')
def about():
    return render_template('about.html')


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

    SQLALCHEMY_TRACK_MODIFICATIONS = True
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


@main.route("/user/<username>")
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash(u'您的资料已更新')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash(u'用户资料已更新')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'用户不存在')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash(u'您已经关注了这个用户')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(u'您关注了 %s.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'用户不存在')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash(u'您没有关注此用户')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(u'您已取消对%s的关注' % username)
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'用户不存在')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followers of",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed_by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'用户不存在')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)


@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30 * 24 * 60 * 60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30 * 24 * 60 * 60)
    return resp


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('moderate.html', comments=comments,
                           pagination=pagination, page=page)


@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))
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
