import json
from flask import Response


class JsonResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, (list, dict)):
            response = Response(json.dumps(response), mimetype='application/json')
        return super(Response, cls).force_type(response, environ)
