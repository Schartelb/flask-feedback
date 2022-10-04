from flask import Flask, request, render_template,  redirect, flash, session
from models import db,  connect_db, User, Feedback
from forms import UserForm, FeedbackForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "dumdumusers"

connect_db(app)


@app.route("/")
def home_page_go():
    """Homepage redirect"""
    return redirect("/register")

########################################################################
# User register, login, logout


@app.route("/register", methods=["GET", "POST"])
def register_user():
    """New User register"""
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        pwd = User.register(password)
        new_user = User(username=username, password=pwd.password,
                        first_name=first_name, last_name=last_name, email=email)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('register.html', form=form)
        session['username'] = new_user.username
        flash('Welcome! Successfully Created Your Account!')
        return redirect(f'/users/{username}')

    return render_template('register.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login_user():
    """User Login routes"""
    form = UserForm()
    user = User.query.filter_by(username=form.username.data).first()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        form.email.data = user.email
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!")
            session['username'] = user.username
            return redirect(f'/users/{username}')
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)


@app.route("/logout")
def logout_user():
    """Logout User"""
    session.pop('username')
    return redirect("/login")

#####################################################################
# /user routes


@app.route('/users/<username>')
def user_info_display(username):
    """Display User Info"""
    if 'username' not in session:
        return redirect('/login')
    user = User.query.filter_by(username=username).first()
    feedback = Feedback.query.all()
    return render_template('user.html', user=user, feedback=feedback)


@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    """Delete User"""
    session_user = session["username"]
    if ('username' not in session):
        return redirect('/login')
    if username != session["username"]:
        return redirect(f"/users/{session_user}")
    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    session.pop('username')
    return redirect('/')

################################################################
# feedback routes


@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def opine_needlessly(username):
    """User Spouts Nonsense"""
    if ('username' not in session):
        return redirect('/login')
    session_user = session["username"]
    if username != session["username"]:
        return redirect(f"/users/{session_user}/feedback/add")
    user = User.query.filter_by(username=username).first()
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        opinion = Feedback(title=title, content=content, username=username)
        db.session.add(opinion)
        db.session.commit()
        return redirect(f'/users/{username}')
    return render_template('feedback.html', user=user, form=form)


@app.route('/feedback/<feedbackid>/update', methods=['GET', 'POST'])
def update_opinion(feedbackid):
    """User changes opinion"""
    if ('username' not in session):
        return redirect('/login')
    session_user = session["username"]
    feedback = Feedback.query.get_or_404(feedbackid)
    if feedback.username != session["username"]:
        return redirect(f"/users/{session_user}/feedback/add")
    form = FeedbackForm(obj=feedback)
    user = User.query.filter_by(username=feedback.username).first()
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{feedback.username}')
    return render_template('editfeedback.html', user=user, form=form, feedback=feedback)


@app.route('/feedback/<feedbackid>/delete', methods=["POST"])
def retract_statement(feedbackid):
    """"Delete user feedback"""
    session_user = session["username"]
    feedback = Feedback.query.get_or_404(feedbackid)
    if ('username' not in session):
        return redirect('/login')
    if feedback.username != session["username"]:
        return redirect(f"/users/{session_user}")
    db.session.delete(feedback)
    db.session.commit()
    return redirect(f'/users/{session_user}')


# @app.route("/secret")
# def secret():
#     if 'username' not in session:
#         flash("NO TOUCHY")
#         return redirect('/login')
#     return (f"You did it!")
