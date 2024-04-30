from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from pytube import YouTube
from pytube.exceptions import RegexMatchError, VideoUnavailable

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open("home.html", "rb") as file:
                self.wfile.write(file.read())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 - Not Found')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        post_params = parse_qs(post_data)

        if self.path == "/submitform":
            link = post_params['url'][0]
            try:
                video = YouTube(link, allow_oauth_cache=True)
                video_stream = video.streams.get_highest_resolution()
                video_path = f"videos.mp4"
                video_stream.download(output_path="static", filename=video_path)
                print("YouTube video downloaded successfully")
                self.send_response(200)
                self.send_header('Content-type', 'application/octet-stream')
                self.send_header('Content-Disposition', f'attachment; filename="{video_path}"')
                self.end_headers()
                with open(f"static/{video_path}", "rb") as file:
                    self.wfile.write(file.read())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=MyHandler, port=5001):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
