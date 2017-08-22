from experchat.models.sessions import EcDevice


class Device(EcDevice):
    """
    Store user's devices to send push notifications to.
    """

    class Meta:
        proxy = True
