#!/usr/bin/env python3

def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/html')]
    start_response(status, headers)
    
    html = """
    <!DOCTYPE html>
    <html>
    <head><title>Simple Test</title></head>
    <body>
        <h1>✅ Python is Working!</h1>
        <p>If you see this, Python and Passenger are working correctly.</p>
        <p>The issue is likely with Flask app imports or database connection.</p>
    </body>
    </html>
    """
    
    return [html.encode()]
