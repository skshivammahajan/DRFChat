from django.utils.translation import ugettext as _

from config.messages import errors, success


def get_message(title):
    message = dict()
    if title.startswith("ERROR_"):
        code_dict = getattr(errors, title)
    elif title.startswith("OK_"):
        code_dict = getattr(success, title)
    else:
        raise NotImplementedError

    message.update(code=code_dict['code'], message=_(code_dict['message']))

    if title.startswith("OK_"):
        return {"metadata": message}

    return message
