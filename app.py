"""
Simple Flask app using modular structure.

This is the new minimal app.py that uses the modular structure.
For the original monolithic app, see app_original.py.
"""

from app import create_app
from flask import Flask, render_template

app = create_app()

# Quick test route from PR merge
@app.route('/mobile-demo')
def mobile_demo():
    return render_template('mobile-demo.html')

if __name__ == '__main__':
    app.run(debug=True)
