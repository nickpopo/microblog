from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, \
	jsonify, g, current_app
from flask_babel import _, get_locale
from flask_login import current_user, login_required
from app import db
from app.models import User, Post
from app.translate import translate, detect_language
from .forms import EditProfileForm, PostForm
from . import bp


# Middleware (Before Request)
@bp.before_app_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()

	# Pass get_locale to g then it is possible to get in templates.
	g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	form = PostForm()
	if form.validate_on_submit():
		language = detect_language(form.post.data)
		if language == 'UNKNOWN' or len(language) > 5:
			language = ''
		post = Post(body=form.post.data, author=current_user,
					language=language)
		db.session.add(post)
		db.session.commit()
		flash(_('Your post is now live!'))
		return redirect(url_for('.index'))
	page = request.args.get('page', 1, type=int)
	posts = current_user.followed_posts().paginate(
		page, current_app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('.index', page=posts.next_num) \
		if posts.has_next else None
	prev_url = url_for('.index', page=posts.prev_num) \
		if posts.has_prev else None
	return render_template('index.html', title='Home', form=form,
						   posts=posts.items, next_url=next_url,
						   prev_url=prev_url)


@bp.route('/explore')
@login_required
def explore():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.timestamp.desc()).paginate(
		page, current_app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('.explore', page=posts.next_num) \
		if posts.has_next else None
	prev_url = url_for('.explore', page=posts.prev_num) \
		if posts.has_prev else None
	return render_template('index.html', title='Explore', posts=posts.items,
						   next_url=next_url, prev_url=prev_url)



@bp.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	page = request.args.get('page', 1, type=int)
	posts = user.posts.order_by(Post.timestamp.desc()).paginate(
		page, current_app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('.user', username=user.username, page=posts.next_num) \
		if posts.has_next else None
	prev_url = url_for('.user', username=user.username, page=posts.prev_num) \
		if posts.has_prev else None
	return render_template('user.html', user=user, posts=posts.items,
						   next_url=next_url, prev_url=prev_url)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user.username)
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash(_('Your changes have been saved.'))
		return redirect(url_for('.edit_profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', title='Edit Profile', form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash(_('User %(username)s not found.', username=username))
		return redirect(url_for('index'))
	if user == current_user:
		flash(_('You cannot follow yourself!'))
		return redirect(url_for('.user', username=username))
	current_user.follow(user)
	db.session.commit()
	flash(_('You are following %(username)s!', username=username))
	return redirect(url_for('.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash(_('User %(username)s not found.', username=username))
		return redirect(url_for('index'))
	if user == current_user:
		flash(_('You cannot unfollow yourself!'))
		return redirect(url_for('.user', username=username))
	current_user.unfollow(user)
	db.session.commit()
	flash(_('You are not following %(username)s.', username=username))
	return redirect(url_for('.user', username=username))


# Translation
@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
	return jsonify({'text': translate(request.form['text'], request.form['dest_language'])})