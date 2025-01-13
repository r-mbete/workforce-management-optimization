from app import create_app  # Import the factory function

# Create the app instance
app = create_app()

# Ensure that the database tables are created (only if needed)
with app.app_context():
    from app.db import db  # Import db here
    db.create_all()  # Create all tables if they don't exist

if __name__ == '__main__':
    # Start the app
    app.run(debug=True)


