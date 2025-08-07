"""
Simple Flask app using modular structure.

This is the new minimal app.py that uses the modular structure.
For the original monolithic app, see app_original.py.
"""

from app import create_app

# Create the Flask application using the app factory
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
