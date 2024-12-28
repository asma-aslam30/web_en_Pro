from flask import Blueprint,render_template,flash,redirect
from flask_login import login_user, login_required, logout_user

from .forms import SignUpForm, LoginForm, PasswordChangeForm
from .models import Customer
from . import db

auth = Blueprint('auth',__name__)


@auth.route('/sign-up',methods=['GET','POST'])
def SignUp():
    form=SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        if password == confirm_password:
            new_customer = Customer()
            new_customer.email = email
            new_customer.username = username
            new_customer.password = confirm_password

            # Adding the customer into database
            try:
                db.session.add(new_customer)
                db.session.commit()
                flash("Account has been created successfully.You can now login!")
                return redirect('/login')
            except Exception as e:
                print(e)
                flash('Account Not Created!!, Email already exists')
            form.email.data = ''
            form.username.data = ''
            form.password.data = ''
            form.confirm_password.data = ''

    return render_template('signup.html',form=form) # form=form indicates that passing the value of forms to our frontend from our backend


@auth.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # it will first check if this particular customer exists
        customer = Customer.query.filter_by(email=email).first()

        # if exists then verify password using verify_pass function defined in models.py file
        if customer:
            if customer.verify_password(password=password):
                login_user(customer)
                return redirect('/')
            else:
                flash('Incorrect Email or Password')

        else:
            flash('Account does not exist please Sign Up')

    return render_template('login.html', form=form)

@auth.route('/logout',methods=['GET','POST'])
@login_required
def log_out():
    logout_user()
    return redirect('/')

@auth.route('/profile/<int:customer_id>') # profile/1,2,3,4,(profile for customer 1,2,3,4...
@login_required
def profile(customer_id):
    customer = Customer.query.get(customer_id)
    print(f"Customer Id: {customer_id}")
    return render_template('profile.html', customer=customer)

@auth.route('/change_password/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def change_password(customer_id):
    form = PasswordChangeForm()
    customer = Customer.query.get(customer_id)
    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data
        confirm_new_password = form.confirm_new_password.data

        if customer.verify_password(current_password):
            if new_password == confirm_new_password:
                customer.password = confirm_new_password
                db.session.commit()
                flash('Password Updated Successfully')
                return redirect(f'/profile/{customer.id}')
            else:
                flash('New Passwords do not match!!')

        else:
            flash('Current Password is Incorrect')

    return render_template('change_password.html', form=form)

