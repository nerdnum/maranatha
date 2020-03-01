from app import bcrypt, db
from app.geography.utils import country_query, subdivision_by_country_query, populated_area_by_subdivision_query
from app.messages.forms import MessageForm
from app.messages.models import Message, UserMessage
from app.messages.utils import create_welcome_message
from app.users.forms import (RegisterForm, LoginForm, InviteUserForm, ChangePasswordForm,
                             ForgotPasswordForm, ForgotPasswordFormWithReset, UserProfileForm, ResetPasswordForm)
from app.users.models import User
from app.users.utils import send_invitation, send_password_reset, get_user_by_login
from app.utils import is_valid_email
from app.token_manager import TokenManager
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask import current_app as app
from flask_login import logout_user, login_user, login_required, current_user
from sqlalchemy import or_, and_, func

users = Blueprint('users', __name__, template_folder='templates')


@users.route('/user/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter(or_(
            User.mobile_phone == form.login.data, func.lower(User.email) == func.lower(form.login.data))).first()
        if not user:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(password=hashed_password, is_active=True, user_confirmed_at=datetime.utcnow())
            if form.is_phone_login:
                user.mobile_phone = form.login.data
            else:
                user.email = form.login.data
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=False)
            flash(f'Your account was successfully created and you have been logged in.', 'success')
            return redirect(url_for('users.profile'))
        else:
            flash('A user with that login already exists', 'danger')
    return render_template('register.html', form=form)


@users.route('/user/register_with_token/<string:token>', methods=['GET', 'POST'])
def register_with_token(token):
    form = RegisterForm()
    token_manager = TokenManager(app)
    invited_by_id, login = token_manager.verify_token(token, expiration_in_seconds=app.config['INVITE_EXPIRATION_TIME'])
    if invited_by_id is None or login is None:
        flash('The token is invalid or has expired. Please ask the person who '
              'sent the invitation to send a new invitation')
    elif form.validate_on_submit():
        if form.login.data.lower() != login.lower():
            flash('The email address or phone number you used does not match the one of your invitation. Please '
                  'check if you used the correct one.')
        else:
            user = User.query.filter(or_(
                User.mobile_phone == form.login.data, User.email == form.login.data)).first()
            if not user:
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user = User(password=hashed_password, is_active=True, user_confirmed_at=datetime.utcnow(),
                            invited_by=invited_by_id)
                if is_valid_email(form.login.data):
                    user.email = form.login.data
                else:
                    user.mobile_phone = form.login.data
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=False)
                flash('Your account was successfully created. Please fill in your '
                      'details below so that we can communicate effectively in the future.', 'success')
                return redirect(url_for('users.profile'))
            else:
                flash('A user with that login already exists', 'danger')
    return render_template('register.html', form=form)


def initialise_profile_form(form):
    form.country_id.choices = country_query(db)
    if not form.country_id.data:
        form.country_id.data = 154
    form.subdivision_id.choices = subdivision_by_country_query(db, form.country_id.data)
    if not form.subdivision_id.data:
        if form.country_id.data == 154:
            form.subdivision_id.data = 6
        elif form.subdivision_id.data == 0:
            form.subdivision_id.choices.append((0, 'Nothing registered'))
        else:
            form.subdivision_id.data = form.subdivision_id.choices[0][0]

    form.populated_area_id.choices = populated_area_by_subdivision_query(db, form.subdivision_id.data)
    if not form.populated_area_id.data:
        if form.subdivision_id.data == 6:
            form.populated_area_id.data = 1
        elif form.subdivision_id.data == 0:
            form.populated_area_id.choices.append((0, 'Nothing registered'))
        else:
            form.populated_area_id.data = form.populated_area_id.choices[0][0]


@users.route('/user/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.get(current_user.id)
    if request.method == 'GET':
        form = UserProfileForm(obj=user)
        initialise_profile_form(form)
    if request.method == 'POST':
        form = UserProfileForm()
        initialise_profile_form(form)
        form.mobile_phone.data = form.mobile_phone.data.strip()
        form.email.data = form.email.data.strip()
    if form.validate_on_submit():
        all_ok = True
        if form.mobile_phone.data.strip() != "":
            duplicate_phone_user = User.query.filter(
                and_(User.mobile_phone == form.mobile_phone.data, User.id != current_user.id))\
                .first()
            if duplicate_phone_user is not None:
                flash_message = "That phone number is already used by another user."
                all_ok = False
        if form.email.data.strip() is not None:
            duplicate_email_user = User.query.filter(
                and_(User.email == form.email.data, User.id != current_user.id))\
                .first()
            if duplicate_email_user is not None:
                flash_message = "That e-mail is already used by another user."
                all_ok = False
        if all_ok:
            form.populate_obj(user)
            db.session.commit()
            flash('You profile has been saved.', 'info')
            if user.login_count is None:
                message_id = create_welcome_message(current_user.id)
                return redirect(url_for('messages.view_messages', private=1, id=current_user.id))
            return render_template('profile.html', form=form)
        flash(flash_message, 'error')
    return render_template('profile.html', form=form)


@users.route('/user/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_login(form.login.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user.is_active:
                login_user(user, remember=form.remember.data)
                user.last_login = datetime.utcnow()
                if user.login_count:
                    user.login_count += 1
                else:
                    user.login_count = 1
                db.session.commit()
                next_url = request.args.get('next', None)
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect(url_for('main.home'))
            else:
                flash('This account is not not active. If you want to reactivate you account, please click '
                      '<a href={}>here</a>'.format(url_for('users.forgot_password', with_reset=1)), 'error')
        else:
            flash('Log in unsuccessful. Please check login and password.', 'error')
    return render_template('login.html', form=form, forgot_password=True)


@users.route('/user/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', 'info')
    return redirect(url_for('main.home'))


@users.route('/user/forgot_password/', defaults={'with_reset': 0}, methods=['GET', 'POST'])
@users.route('/user/forgot_password/<int:with_reset>', methods=['GET', 'POST'])
def forgot_password(with_reset):
    if with_reset:
        form = ForgotPasswordFormWithReset()
    else:
        form = ForgotPasswordForm()
    if form.validate_on_submit():
        submitted_login = form.login.data
        user = get_user_by_login(submitted_login)
        if not user:
            flash('There is no account with that login.', 'danger')
        else:
            try:
                if form.reactivate_account.data:
                    user.is_active = True
                    db.session.commit()
            except AttributeError:
                pass
            send_password_reset(submitted_login)
            flash_message = "{} with password reset instructions have been sent to you."\
                .format('An email' if is_valid_email(submitted_login) else 'A sms')
            flash(flash_message, 'info')
            return redirect(url_for('main.home'))
    return render_template('forgot_password.html', form=form)


@users.route('/user/reset_password/<string:token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm()
    user_id = User.verify_reset_token(token)
    if not user_id:
        flash('That is not a valid reset token or its has expired.')
    if form.validate_on_submit():
        user = User.query.get(user_id)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been reset. You can now log in.')
        login_user(user)
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', form=form)


@users.route('/user/change_password', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        hashed_old_password = bcrypt.generate_password_hash(form.old_password.data).decode('utf-8')
        if not form.old_password.data:
            flash_message = 'You must provide your old password, please.'
        elif not bcrypt.check_password_hash(current_user.password, form.old_password.data):
            flash_message = 'The password your provided does not match your old password'
        else:
            new_hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            current_user.password = new_hashed_password
            db.session.commit()
            flash('You have successfully changed your password', 'info')
            return redirect(url_for('users.profile'))
        flash(flash_message, "danger")
    return render_template('change_password.html', form=form)


@users.route('/user/invite', methods=['GET', 'POST'])
def invite_user():
    form = InviteUserForm()
    if form.validate_on_submit():
        user = get_user_by_login(form.login.data)
        if not user:
            send_invitation(form.login.data, current_user)
            flash('The invitation was sent', 'info')
            return redirect(url_for('main.home'))
        else:
            flash('A user with that login information already exists.')
    return render_template('invite.html', form=form)


@users.route('/user/unsubscribe', methods=['POST'])
@login_required
def unsubscribe():
    current_user.is_active = False
    db.session.commit()
    logout_user()
    flash('You have been unsubscribed', 'info')
    return redirect(url_for('main.home'))


@users.route('/user/my_network/', methods=['GET', 'POST'])
def team_members():
    enlister = User.query.filter_by(id=current_user.invited_by).first()
    partners = []
    if enlister is not None:
        partners = User.query.filter_by(invited_by=enlister.id, is_active=True).order_by('first_name').all()
        for user in partners:
            if user.id == current_user.id:
                partners.remove(user)
        partners.append(enlister)
    enlistees = User.query.filter_by(invited_by=current_user.id).all()
    form = MessageForm()
    if form.validate_on_submit():
        user_ids = form.user_list.data
        message = Message(subject=form.subject.data, content=form.content.data,
                          is_private=True, created_by=current_user.id, is_urgent=False)
        db.session.add(message)
        db.session.commit()
        message_id = message.id
        for id in user_ids.split(","):
            user_message = UserMessage(message_id=message_id, user_id=int(id))
            db.session.add(user_message)
        db.session.commit()
        flash('Message was successfully submitted', 'success')
        return redirect(url_for('main.home'))
    return render_template('my_team.html', enlister=enlister, partners=partners, enlistees=enlistees, form=form)


@users.route('/user/admin')
@login_required
def admin_view():
    if current_user.has_any_role(['admin']):
        return redirect(app.config['ADMIN_URL'])
    else:
        flash('You are not authorised to view do this.')
        return redirect(url_for('main.home'))


