from rest_framework.renderers import JSONRenderer


class EcJSONRenderer(JSONRenderer):
    """
    Override the response format before rendering.
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `data` into JSON, returning a bytestring.
        """
        if data is None:
            return bytes()

        if not any(key in data for key in ['results', 'errors', 'metadata']):
            data = {'results': data}

        return super(EcJSONRenderer, self).render(data, accepted_media_type, renderer_context)
