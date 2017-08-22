import requests
from django.conf import settings
from pubnub import pubnub
from pubnub.pnconfiguration import PNConfiguration

from experchat.patterns import Singleton


class ExperchatPublisher(metaclass=Singleton):
    """
    This class provides all publishing options by using pubnub SDK.
    """
    publisher = None
    user_publisher = None

    def __init__(self):
        pnconfig = PNConfiguration()
        pnconfig.subscribe_key = settings.PUBNUB_SUBSCRIBE_KEY
        pnconfig.publish_key = settings.PUBNUB_PUBLISH_KEY
        pnconfig.ssl = False

        self.publisher = pubnub.PubNub(pnconfig)

        pnconfig = PNConfiguration()
        pnconfig.subscribe_key = settings.PUBNUB_SUBSCRIBE_KEY_USER
        pnconfig.publish_key = settings.PUBNUB_PUBLISH_KEY_USER
        pnconfig.ssl = False

        self.user_publisher = pubnub.PubNub(pnconfig)

    def get_user_channel(self, user_id, user_type):
        """
        Provide pubnub channel for user.

        Args:
            user_id: ID of user.
            user_type: Type of user.

        Returns:
            Name of the channel.
        """
        if user_type is "expert":
            return "expert_ch_" + str(user_id)
        elif user_type is "user":
            return "user_ch_" + str(user_id)
        else:
            return "expert_ch_" + str(user_id) + "," + "user_ch_" + str(user_id)

    def get_device_channel(self, device_id):
        """
        Provide pubnub channel for device.

        Args:
            device_id: ID of device.

        Returns:
            Name of the channel.
        """
        return "device_ch_" + str(device_id)

    def __publish(self, user_type, channel, message):
        """
        Publish message on channel.

        Args:
            channel: Name of channel.
            message: Message to publish.

        Returns:
            None
        """
        if user_type is 'expert':
            self.publisher.publish().\
                channel(channel).\
                message(message).\
                should_store(True).\
                use_post(True).\
                sync()
        elif user_type is 'user':
            self.user_publisher.publish(). \
                channel(channel). \
                message(message). \
                should_store(True). \
                use_post(True). \
                sync()

    def publish_message_on_device(self, user_type, device_id, message):
        """
        Publish message on device.
        Args:
            user_type: Type of user.
            device_id: ID of device.
            message : message to publish.
        Returns:
            None
        """
        channel = self.get_device_channel(device_id)
        self.__publish(user_type=user_type, channel=channel, message=message)

    def publish_message_on_user_devices(self, user_id, user_type, message):
        """
        Publish message on a user devices.
        Args:
            user_id : ID of user to publish message on devices of.
            user_type: Type of user.
            message : Message to publish.
        """
        channel = self.get_user_channel(user_id, user_type)
        return self.__publish(user_type=user_type, channel=channel, message=message)

    def add_push_device(self, user_id, user_type, device_id,
                        device_token, device_type):
        """
        Add ios/android device to send push notifications.

        Args:
            user_id : ID of user to add device of.
            user_type : Type of user.
            device_id : ID of device.
            device_token : Token of device.
            device_type : Type of device (ios/android).
        Returns:
            Boolean value, whether device added or not.
        """
        device_channel = self.get_device_channel(device_id)
        user_channel = self.get_user_channel(user_id, user_type)
        channels = ",".join([user_channel, device_channel])

        device_type = 'apns' if device_type == 'ios' else 'gcm'

        if user_type is "user":
            subscribe_key = settings.PUBNUB_SUBSCRIBE_KEY_USER
        else:
            subscribe_key = settings.PUBNUB_SUBSCRIBE_KEY

        device_register_url = "{api_url}{subscribe_key}/devices/" \
                              "{device_token}?add={channels}&type={device_type}".format(
                                  api_url="http://pubsub.pubnub.com/v1/push/sub-key/",
                                  subscribe_key=subscribe_key,
                                  device_token=device_token,
                                  channels=channels,
                                  device_type=device_type,
                              )

        device_register_resp = requests.get(device_register_url)
        return True if device_register_resp.status_code == 200 else False

    def remove_push_device(self, user_id, user_type, device_id,
                           device_token, device_type):
        """
        Remove push device from push channel.

        Args:
            user_id : ID of user to add device of.
            user_type : Type of user.
            device_id : ID of device.
            device_token : Token of device.
            device_type : Type of device (ios/android).
        Returns:
            None
        """
        device_channel = self.get_device_channel(device_id)
        user_channel = self.get_user_channel(user_id, user_type)
        channels = ",".join([user_channel, device_channel])

        device_type = 'apns' if device_type == 'ios' else 'gcm'

        if user_type is "user":
            subscribe_key = settings.PUBNUB_SUBSCRIBE_KEY_USER
        else:
            subscribe_key = settings.PUBNUB_SUBSCRIBE_KEY

        device_remove_url = "{api_url}{subscribe_key}/devices/" \
                            "{device_token}?remove={channels}&type={device_type}".format(
                                api_url="http://pubsub.pubnub.com/v1/push/sub-key/",
                                subscribe_key=subscribe_key,
                                device_token=device_token,
                                channels=channels,
                                device_type=device_type,
                            )
        requests.get(device_remove_url)


def publish_data(session_info, alert):
    """
    Util function to format pushable data.
    """
    gcm_notification = {"body": alert, "push_type": "session"}
    gcm_notification.update(session_info)

    pubnub_publish_data = {
        "pn_apns": {
            "aps": {
                "alert": alert,
                "badge": 1,
                "sound": "default",
                "content-available": 1
            },
            "call": session_info,
            "push_type": "session",
        },
        "pn_gcm": {
            "data": gcm_notification,
        },
        "pn_ttl": settings.PUBNUB_PUSH_TIMEOUT,
        "pn_debug": settings.PUBNUB_DEBUG_MODE
    }

    return pubnub_publish_data


class DummyExperchatPublisher(ExperchatPublisher):
    """
    This class provides all publishing options by using pubnub SDK.
    """
    publisher = None
    user_publisher = None

    def __init__(self):
        return

    def publish_message_on_device(self, user_type, device_id, message):
        return

    def publish_message_on_user_devices(self, user_id, user_type, message):
        return

    def add_push_device(self, user_id, user_type, device_id,
                        device_token, device_type):
        return True

    def remove_push_device(self, user_id, user_type, device_id,
                           device_token, device_type):
        return


if settings.TEST_MODE:
    ExperchatPublisher = DummyExperchatPublisher
