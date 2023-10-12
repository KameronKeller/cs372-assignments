from request import Request

class Response:

    ERROR_404 = "404 Not Found"
    OK_200 = "200 OK"
    CONTENT_TYPE = "Content-Type: "
    CONTENT_LENGTH = "Content-Length: "
    CONNECTION = "Connection: close"
    ENCODING = "ISO-8859-1"

    def __init__(self, request, http_version="HTTP/1.1"):
        self.request = request
        self.http_version = http_version

    def build_response(self):
        # Request the file
        requested_file = self.get_requested_file(self.request.file_name)

        # If the file is a 404 message, prepare that
        if requested_file == Response.ERROR_404:
            response = "{} {}".format(self.http_version, requested_file)
        
        # Otherwise, build the response
        else:
            response = "{} {}\n{}{}\n{}{}\n{}\n\n{}".format(
                self.http_version,
                Response.OK_200,
                Response.CONTENT_TYPE,
                self.request.mime_type,
                Response.CONTENT_LENGTH,
                len(requested_file),
                Response.CONNECTION,
                requested_file
            )

        # Return the encoded response
        return response.encode(Response.ENCODING)

    def get_requested_file(self, filename):
        # Attempt to open the file, if it fails, return 404
        try:
            with open(filename) as file:
                data = file.read()
                return data
        except:
            return Response.ERROR_404