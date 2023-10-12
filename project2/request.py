import os

class Request:

    mime_types = {
        ".txt" : "text/plain",
        ".html" : "text/html",
        ".ico" : "image/x-icon"
    }

    def __init__(self, request_data):
        self.request_data = request_data.decode()
        self.http_method = None
        self.host = None
        self.directory = None
        self.file_name = None
        self.mime_type = None
        self.connection = None
        self.parse_request()

    def parse_request(self):
        # Locate the end of the header
        header_end_index = self.request_data.find("\r\n\r\n")

        # Slice the header out of the request string
        header = self.request_data[:header_end_index]

        # Split the string by CRLF (carriage return line feed)
        header = header.split("\r\n")

        # Save variables
        self.extract_header_info(header)

    def extract_file_info(self, request_line):
        # Split the request line on whitespace:
        # "GET /dir/dir2/foo.gif HTTP/1.1"
        request_line = request_line.split()

        # Separate the directory and file_name
        directory, file_name = os.path.split(request_line[1])

        # Separate the file name from file extension, only keep the file extension
        _, file_extension = os.path.splitext(file_name)

        # Store the necessary values as member variables
        self.directory = directory
        self.file_name = file_name
        self.mime_type = self.get_mime_type(file_extension)

    def extract_header_info(self, header):
        # Extract the file information from the header
        self.extract_file_info(header[0])

        # Store the other values as member variables
        self.host = header[1]
        self.connection = header[2]

    def get_mime_type(self, file_extension):
        return Request.mime_types[file_extension]

