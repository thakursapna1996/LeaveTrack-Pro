"""
LeaveTrack-Pro: A Simple Leave Management System
For Elastic Beanstalk deployment
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Initialize Flask app - Elastic Beanstalk looks for 'application'
application = Flask(__name__)
application.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leaves.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(application)


# Database Model
class LeaveRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    leave_type = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Create tables
with application.app_context():
    db.create_all()


# HOME - View all leaves
@application.route('/')
def index():
    leaves = LeaveRequest.query.order_by(LeaveRequest.created_at.desc()).all()
    return render_template('index.html', leaves=leaves)


# CREATE - Add leave
@application.route('/add', methods=['GET', 'POST'])
def add_leave():
    if request.method == 'POST':
        employee_name = request.form.get('employee_name', '').strip()
        email = request.form.get('email', '').strip()
        leave_type = request.form.get('leave_type', '').strip()
        start_date = request.form.get('start_date', '')
        end_date = request.form.get('end_date', '')
        reason = request.form.get('reason', '').strip()

        # Validation
        errors = []
        if not employee_name or len(employee_name) < 2:
            errors.append('Employee name must be at least 2 characters')
        if not email or '@' not in email:
            errors.append('Please enter a valid email')
        if not leave_type:
            errors.append('Please select leave type')
        if not start_date or not end_date:
            errors.append('Please select dates')
        else:
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d').date()
                end = datetime.strptime(end_date, '%Y-%m-%d').date()
                if end < start:
                    errors.append('End date cannot be before start date')
            except:
                errors.append('Invalid date')
        if not reason or len(reason) < 10:
            errors.append('Reason must be at least 10 characters')

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('add_leave.html')

        new_leave = LeaveRequest(
            employee_name=employee_name,
            email=email,
            leave_type=leave_type,
            start_date=start,
            end_date=end,
            reason=reason
        )
        db.session.add(new_leave)
        db.session.commit()
        flash('Leave request submitted!', 'success')
        return redirect(url_for('index'))

    return render_template('add_leave.html')


# READ - View single leave
@application.route('/view/<int:id>')
def view_leave(id):
    leave = LeaveRequest.query.get_or_404(id)
    return render_template('view_leave.html', leave=leave)


# UPDATE - Edit leave
@application.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_leave(id):
    leave = LeaveRequest.query.get_or_404(id)

    if request.method == 'POST':
        leave.employee_name = request.form.get('employee_name', '').strip()
        leave.email = request.form.get('email', '').strip()
        leave.leave_type = request.form.get('leave_type', '').strip()
        leave.start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
        leave.end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
        leave.reason = request.form.get('reason', '').strip()
        leave.status = request.form.get('status', 'Pending')

        db.session.commit()
        flash('Leave updated!', 'success')
        return redirect(url_for('index'))

    return render_template('edit_leave.html', leave=leave)


# DELETE - Remove leave
@application.route('/delete/<int:id>', methods=['POST'])
def delete_leave(id):
    leave = LeaveRequest.query.get_or_404(id)
    db.session.delete(leave)
    db.session.commit()
    flash('Leave deleted!', 'success')
    return redirect(url_for('index'))


# Health check
@application.route('/health')
def health():
    return {'status': 'healthy', 'app': 'LeaveTrack-Pro'}, 200


if __name__ == '__main__':
    application.run(debug=True)

