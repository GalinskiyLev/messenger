from flask import Flask, render_template, request, make_response, session, redirect, abort
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from data import db_session
from data.users import User
from data.messages import Message
from data.friends import Friend
from forms.user_forms import RegisterForm, LoginForm, SendMessageForm
from sqlalchemy import desc



app = Flask(__name__)
app.config["SECRET_KEY"] = "My messanger"
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    if not current_user.is_authenticated:
        return redirect("/login")
    all_messages = db_sess.query(Message).filter(Message.to_id == current_user.id).order_by(Message.created_date.desc()).all()
    resp = render_template("index.html", all_messages=all_messages)
    return resp


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user:
            if user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
            return render_template("login.html", form=form, title="Авторизация", message="Неверный пароль!")
        return render_template("login.html", form=form, title="Авторизация", message="Неверный email!")

    return render_template("login.html", form=form, title="Авторизация")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            fio=form.fio.data,
            email=form.email.data,
            info=form.info.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect("/")
    return render_template("register.html", form=form, title="Регистрация")


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route("/send_message", methods=["GET", "POST"])
@login_required
def send_message():
    form = SendMessageForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if not user:
            return render_template('send_message.html', title='Отправление сообщения', form=form,
                                   message="Такого пользователя нет")
        if not form.text.data:
            return render_template('send_message.html', title='Отправление сообщения', form=form,
                                   message="Введите сообщение")
        message = Message(text=form.text.data,
                          to_id=user.id,
                          from_id=current_user.id)
        db_sess.add(message)
        db_sess.commit()
        return redirect('/')
    return render_template('send_message.html', title='Отправление сообщения', form=form)


if __name__ == "__main__":
    db_session.global_init("db/messanger.db")
    #app.register_blueprint(news_api.blueprint)
    app.run("localhost", 8080)
