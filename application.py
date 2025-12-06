"""
==============================================
LeaveTrack-Pro - Leave Management System
==============================================
This is a simple web application where employees 
can apply for leave and managers can approve/reject.

Technologies Used:
- Python (Programming Language)
- Flask (Web Framework)
- SQLite (Database)
- SQLAlchemy (Database ORM)
==============================================
"""

# Import required libraries
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# ==============================================
# APP CONFIGURATION
# ==============================================

# Create Flask application
# Note: We use 'application' (not 'app') because AWS Elastic Beanstalk looks for this name
application = Flask(__name__)

# Secret key for security (used for sessions and flash messages)
application.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'leavetrack-secret-key')

# Database configuration - using SQLite (a simple file-based database)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leaves.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database connection
db = SQLAlchemy(application)


# ==============================================
# DATABASE MODEL (Table Structure)
# ==============================================

class LeaveRequest(db.Model):
    """
    This is our database table for storing leave requests.
    Each row in this table represents one leave application.
    
    Columns:
    - id: Unique identifier for each leave request
    - employee_name: Name of the employee applying for leave
    - email: Employee's email address
    - leave_type: Type of leave (Annual, Sick, Personal, etc.)
    - start_date: When the leave starts
    - end_date: When the leave ends
    - reason: Why the employee needs leave
    - status: Pending, Approved, or Rejected
    - created_at: When this request was submitted
    """
    id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    leave_type = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Pending')  # Default status is Pending
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Create database tables when app starts
with application.app_context():
    db.create_all()


# ==============================================
# ROUTES (Web Pages)
# ==============================================

# ----------------------------------------------
# HOME PAGE - Shows all leave requests
# URL: http://yourapp.com/
# ----------------------------------------------
@application.route('/')
def index():
    """
    This is the home page.
    It fetches all leave requests from database and displays them.
    The requests are sorted by newest first (desc = descending order).
    """
    # Get all leaves from database, newest first
    leaves = LeaveRequest.query.order_by(LeaveRequest.created_at.desc()).all()
    
    # Show the index.html page with the leave data
    return render_template('index.html', leaves=leaves)


# ----------------------------------------------
# ADD LEAVE - Form to submit new leave request
# URL: http://yourapp.com/add
# ----------------------------------------------
@application.route('/add', methods=['GET', 'POST'])
def add_leave():
    """
    This page allows employees to apply for leave.
    
    GET request: Shows the empty form
    POST request: Processes the submitted form
    """
    
    # If form is submitted (POST request)
    if request.method == 'POST':
        
        # Get data from the form
        employee_name = request.form.get('employee_name', '').strip()
        email = request.form.get('email', '').strip()
        leave_type = request.form.get('leave_type', '').strip()
        start_date = request.form.get('start_date', '')
        end_date = request.form.get('end_date', '')
        reason = request.form.get('reason', '').strip()

        # ----------------------------------------------
        # INPUT VALIDATION - Check if data is valid
        # This is important for security!
        # ----------------------------------------------
        errors = []
        
        # Check employee name (must be at least 2 characters)
        if not employee_name or len(employee_name) < 2:
            errors.append('Employee name must be at least 2 characters')
        
        # Check email (must contain @)
        if not email or '@' not in email:
            errors.append('Please enter a valid email')
        
        # Check leave type (must be selected)
        if not leave_type:
            errors.append('Please select leave type')
        
        # Check dates (must be provided)
        if not start_date or not end_date:
            errors.append('Please select dates')
        
        # Check reason (must be at least 10 characters)
        if not reason or len(reason) < 10:
            errors.append('Reason must be at least 10 characters')

        # If there are validation errors, show them and return to form
        if errors:
            for error in errors:
                flash(error, 'error')  # Show error message
            return render_template('add_leave.html')

        # ----------------------------------------------
        # SAVE TO DATABASE
        # ----------------------------------------------
        try:
            # Convert date strings to Python date objects
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            # Check if end date is after start date
            if end < start:
                flash('End date cannot be before start date', 'error')
                return render_template('add_leave.html')

            # Create new leave request object
            new_leave = LeaveRequest(
                employee_name=employee_name,
                email=email,
                leave_type=leave_type,
                start_date=start,
                end_date=end,
                reason=reason
                # status will be 'Pending' by default
            )
            
            # Add to database and save
            db.session.add(new_leave)
            db.session.commit()
            
            # Show success message and go to home page
            flash('Leave request submitted!', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            # If something goes wrong, show error
            flash('Error submitting request', 'error')

    # If GET request, just show the empty form
    return render_template('add_leave.html')


# ----------------------------------------------
# VIEW LEAVE - Shows details of one leave request
# URL: http://yourapp.com/view/1 (where 1 is the leave ID)
# ----------------------------------------------
@application.route('/view/<int:id>')
def view_leave(id):
    """
    Shows the full details of a single leave request.
    
    Parameters:
    - id: The unique ID of the leave request to view
    """
    # Find the leave request by ID (or show 404 error if not found)
    leave = LeaveRequest.query.get_or_404(id)
    
    # Show the view page with leave details
    return render_template('view_leave.html', leave=leave)


# ----------------------------------------------
# EDIT LEAVE - Form to update existing leave request
# URL: http://yourapp.com/edit/1 (where 1 is the leave ID)
# ----------------------------------------------
@application.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_leave(id):
    """
    Allows editing an existing leave request.
    Also used by manager to change status (Approve/Reject).
    
    Parameters:
    - id: The unique ID of the leave request to edit
    """
    # Find the leave request by ID
    leave = LeaveRequest.query.get_or_404(id)
    
    # If form is submitted (POST request)
    if request.method == 'POST':
        # Update the leave request with new data
        leave.employee_name = request.form.get('employee_name', '').strip()
        leave.email = request.form.get('email', '').strip()
        leave.leave_type = request.form.get('leave_type', '').strip()
        leave.start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
        leave.end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
        leave.reason = request.form.get('reason', '').strip()
        leave.status = request.form.get('status', 'Pending')  # Can change to Approved/Rejected
        
        # Save changes to database
        db.session.commit()
        
        # Show success message and go to home page
        flash('Leave updated!', 'success')
        return redirect(url_for('index'))
    
    # If GET request, show the edit form with existing data
    return render_template('edit_leave.html', leave=leave)


# ----------------------------------------------
# DELETE LEAVE - Removes a leave request
# URL: http://yourapp.com/delete/1 (where 1 is the leave ID)
# Note: Only accepts POST requests (for security)
# ----------------------------------------------
@application.route('/delete/<int:id>', methods=['POST'])
def delete_leave(id):
    """
    Deletes a leave request from the database.
    
    Parameters:
    - id: The unique ID of the leave request to delete
    """
    # Find the leave request by ID
    leave = LeaveRequest.query.get_or_404(id)
    
    # Delete from database
    db.session.delete(leave)
    db.session.commit()
    
    # Show success message and go to home page
    flash('Leave deleted!', 'success')
    return redirect(url_for('index'))


# ----------------------------------------------
# HEALTH CHECK - For monitoring the application
# URL: http://yourapp.com/health
# Used by AWS to check if app is running properly
# ----------------------------------------------
@application.route('/health')
def health():
    """
    Simple health check endpoint.
    Returns OK if the application is running.
    Used by AWS Elastic Beanstalk for monitoring.
    """
    return {'status': 'healthy', 'app': 'LeaveTrack-Pro'}, 200


# ==============================================
# RUN THE APPLICATION
# ==============================================

if __name__ == '__main__':
    """
    This runs the application when you execute:
    python application.py
    
    debug=True means:
    - Shows detailed errors
    - Auto-reloads when code changes
    - Only use debug=True during development!
    """
    application.run(debug=True)
