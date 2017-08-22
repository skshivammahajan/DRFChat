from django.conf import settings
from django.utils import timezone
from opentok import ArchiveModes, MediaModes, opentok


class ExperchatWebRTC:
    """Provide WebRTC services."""
    connection = None

    def __init__(self):
        """Initialize WebRTC connection."""
        self.connection = opentok.OpenTok(
            settings.TOKBOX_API_KEY,
            settings.TOKBOX_API_SECRET
        )

    def get_webrtc_session(self):
        """
        Generates webrtc session.

        args: NA
        return: webrtc session_id
        """
        session = self.connection.create_session(
            media_mode=MediaModes.routed,
            archive_mode=ArchiveModes.manual,
            location=settings.TOKBOX_LOCATION
        )

        return session.session_id

    def get_webrtc_session_token(self, session_id):
        """
        Generates webrtc session authentication token.

        args:
            session_id : WebRTC session id
        return:  webrtc session authentication token.
        """

        return self.connection.generate_token(
            session_id,
            expire_time=int(timezone.now().timestamp()) + settings.TOKBOX_TOKEN_EXPIRE_TIME
        )


class DummyExperchatWebRTC(ExperchatWebRTC):

    def __init__(self):
        return

    def get_webrtc_session(self):
        return "session_id"

    def get_webrtc_session_token(self, session_id):
        return "token"

if settings.TEST_MODE:
    ExperchatWebRTC = DummyExperchatWebRTC
