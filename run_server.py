from app import app

if __name__ == '__main__':
    print("Starting PM Tool server...")
    print("Open your browser and go to: http://localhost:5000")
    print("Login credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\nPress Ctrl+C to stop the server")
    app.run(debug=True, host='0.0.0.0', port=5000)