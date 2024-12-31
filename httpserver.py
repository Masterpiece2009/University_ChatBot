from http.server import BaseHTTPRequestHandler, HTTPServer #to handle http requests individual and httpserver to create and run http server
from urllib.parse import parse_qs

# Custom HTTP request handler class
class MyHandler(BaseHTTPRequestHandler):
    # Handle GET request
    def do_GET(self):
        if self.command == "GET":
            # Parse the query string
            query_string = self.path.split('?')[-1]
            params = parse_qs(query_string)

            # Access specific parameters
            name = params.get('name', [''])[0]  # Get 'name' parameter or default to empty string

            # Respond with content based on the parameter
            self.send_response(200)
            self.send_header("Content-type", "plainText")#inform client that response is html
            self.end_headers()
            self.wfile.write(f"Hello, {name}!To register for courses, log in to the student portal IBN EL-HAITHAM, navigate to Course Registration, and select your desired courses based on eligibility and program requirements. Confirm your selections, submit the form, and pay any required fees to finalize. For assistance, contact your academic advisor.".encode())

    # Handle POST request
    def do_POST(self):
        if self.command == "POST":
            # Get content length from headers
            content_len = int(self.headers.get('Content-Length', 0))

            # Read form data from request body
            post_data = self.rfile.read(content_len).decode()#read raw data from client ,then convert to string

            # Parse the form data (assuming a single field named 'message')
            message = post_data.split('=')[-1]  # Split to extract the value after '='

            # Respond with content based on the form data
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f"You sent: {message}".encode())

# Define port number
PORT = 54512

# Create and start the HTTP server
if __name__ == "__main__":
    server = HTTPServer(("", PORT), MyHandler)
    print(f"Server running at port {PORT}")
    server.serve_forever()

    #http://localhost:54512/