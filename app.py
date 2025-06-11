from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24) # Strong secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlclient://YOUR_MYSQL_USER:YOUR_MYSQL_PASSWORD@localhost/voting_db' # IMPORTANT: Replace with your MySQL username and password!
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # The route for login

# --- Database Models ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class VoteOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    # Add any other relevant fields for vote options, e.g., category, image_url

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('vote_option.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('votes', lazy=True))
    option = db.relationship('VoteOption', backref=db.backref('votes', lazy=True))

    # Ensure a user can vote for an option only once (if that's the requirement)
    __table_args__ = (db.UniqueConstraint('user_id', 'option_id', name='_user_option_uc'),)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Routes ---
@app.route('/')
def index():
    # This will eventually render the votes.html or a new landing page
    # For now, let's redirect to login if not authenticated, or to a dashboard/vote page
    if current_user.is_authenticated:
        return redirect(url_for('vote_page'))
    return render_template('login.html', current_user=current_user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username and password are required.', 'danger')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'warning')
            return redirect(url_for('register'))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', current_user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            # Redirect to the page they were trying to access, or to the main vote page
            next_page = request.args.get('next')
            return redirect(next_page or url_for('vote_page'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', current_user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/vote', methods=['GET', 'POST'])
@login_required
def vote_page():
    # This will be the main page for voting, using a modified votes.html
    # For now, it's a placeholder
    if request.method == 'POST':
        # Process vote submission
        option_id = request.form.get('option_id')
        if not option_id:
            flash('Please select an option to vote.', 'warning')
            return redirect(url_for('vote_page'))

        # Check if user has already voted for this option (if unique constraint is not enough or for specific logic)
        existing_vote = Vote.query.filter_by(user_id=current_user.id, option_id=option_id).first()
        if existing_vote:
            flash('You have already voted for this option.', 'info')
            return redirect(url_for('vote_page'))

        vote_option = VoteOption.query.get(option_id)
        if not vote_option:
            flash('Invalid voting option.', 'danger')
            return redirect(url_for('vote_page'))

        new_vote = Vote(user_id=current_user.id, option_id=option_id)
        db.session.add(new_vote)
        db.session.commit()
        flash(f'Successfully voted for {vote_option.name}!', 'success')
        return redirect(url_for('results')) # Or back to vote_page with updated status

    options = VoteOption.query.all()
    return render_template('votes_dynamic.html', options=options, current_user=current_user)

@app.route('/results')
@login_required # Or make it public
def results():
    # Display voting results
    # This is a simplified version. You'd typically aggregate votes.
    all_votes = Vote.query.join(VoteOption).add_columns(VoteOption.name, db.func.count(Vote.id).label('vote_count')).group_by(VoteOption.name).all()
    # `all_votes` will be a list of tuples like: (option_name, vote_count)
    return render_template('results.html', votes_data=all_votes, current_user=current_user)

@app.route('/admin/upload_options', methods=['POST'])
@login_required # Add admin role check later
def upload_options():
    # This route will handle the Excel file upload from votes.html (or a new admin page)
    # For now, it's a placeholder. We'll need to integrate the Excel parsing logic.
    if 'excel_file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['excel_file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        # Process the file (parse Excel, add options to VoteOption table)
        # This part needs to be implemented, similar to the JS logic in votes.html
        # For example, using openpyxl or pandas
        # For now, just a success message
        # Make sure to clear existing options or handle updates carefully
        # VoteOption.query.delete() # Example: clear old options before adding new ones
        # db.session.commit()
        # ... parsing logic ...
        # new_option = VoteOption(name=row_data['name_column'], description=row_data['desc_column'])
        # db.session.add(new_option)
        # db.session.commit()
        return jsonify({'message': 'Options uploaded successfully (backend placeholder).'}), 200
    return jsonify({'error': 'File processing failed'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Create database tables if they don't exist
    app.run(debug=True)