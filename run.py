from app import create_app

app = create_app('prod') # Use prod config by default for production readiness

if __name__ == '__main__':
    # Use waitress for production serving on Windows
    from waitress import serve
    print("Starting production server on http://0.0.0.0:5000")
    serve(app, host='0.0.0.0', port=5000)
