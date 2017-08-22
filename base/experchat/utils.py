import datetime
import io
from copy import deepcopy
from operator import itemgetter

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils import timezone
from PIL import Image
from rest_framework.views import exception_handler

from experchat.data_uri import DataURI
from experchat.enumerations import CallStatus
from experchat.messages import get_message
from experchat.models.appointments import Calendar
from experchat.models.session_pricing import SessionPricing
from experchat.models.sessions import EcSession


def custom_send_mail(subject_template_name, email_template_name,
                     context, to_email, html_email_template_name=None):
    subject = loader.render_to_string(subject_template_name, context)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(email_template_name, context)

    email_message = EmailMultiAlternatives(subject, body, settings.DEFAULT_FROM_EMAIL, [to_email])
    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, 'text/html')

    email_message.send()


def custom_exception_handler(exc, context):
    """
    Update response for 400 exceptions to include code of validation error along with error message.
    """

    # Format standard serializer validation errors to custom format.
    if hasattr(exc, 'detail'):
        if isinstance(exc.detail, dict):
            new_detail = dict()
            for key, value in exc.detail.items():
                if isinstance(value, list):
                    error = value[0]
                    if error.startswith("ERROR_"):
                        new_detail.update({key: [get_message(error)]})
                    else:
                        new_detail.update({key: [{"code": 1000, "message": error}]})
                else:
                    try:
                        new_detail.update({key: [{"code": 1000, "message": str(value)}]})
                    except Exception:
                        new_detail.update({key: value})
            exc.detail = new_detail

    # Call REST framework's default exception handler,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Modify response data to have key errors
    if response:
        response.data = {"errors": response.data}

    return response


def validate_data_uri(data_uri_str):
    """
    Validate input data uri.

    Args:
        data_uri_str: Data URI. (https://en.wikipedia.org/wiki/Data_URI_scheme)
    Returns:
        DataURI object.
    Raises:
        ValueError: Invalid Data URI.
    """

    try:
        data_uri = DataURI(data_uri_str)
    except ValueError:
        raise ValueError("Invalid Data URI.")

    if not data_uri.is_base64 or not data_uri.data:
        raise ValueError("Invalid Data URI.")

    return data_uri


def create_image_thumbnail(image, width, height, filename):
    """
    Generate thumbnail (jpeg) of image and save in default storage.

    Args:
        image: Image object (PIL).
        width: Width of thumbnail.
        height: Height of thumbnail.
        filename: Name of the thumbnail file.
    """
    image.thumbnail((width, height), Image.ANTIALIAS)

    # Save thumbnail in a buffer, to use django's default_storage
    f = io.BytesIO()
    image.save(f, 'jpeg')

    default_storage.save(
        '{filename}_{width}x{height}.jpg'.format(
            filename=filename,
            width=width,
            height=height,
        ),
        f
    )


#  util method to get the datetime
def get_slot_datetime(date, time, time_zone):
    # This method will get the slot datetime after converting saved date time to UTC
    if type(time_zone) == str:
        time_zone = timezone.pytz.timezone(time_zone)

    date_time = timezone.datetime.combine(date, time)
    return timezone.make_aware(date_time, time_zone).astimezone(timezone.pytz.UTC)


def process_and_merge_slots(slots, today=None):
    """
    Process the craeted slots and merge them into one slots if overlapping
    Args:
        slots (query string): Django query dict
        today (obj): default to None, this is require for test case and from which date slots will be calculated
    Return:
        merge slots which were created by expert
    """
    if not slots:
        return []

    if today is None:
        today = timezone.now().date()

    def get_next_date(day, cur_week):
        daydiff = day - today.weekday() - 1

        if daydiff < 0:
            daydiff += 7

        date = today + timezone.timedelta(days=(daydiff + cur_week * 7))
        return date

    def merge_final_slots(combined_slots):
        counter = 0
        merged_slots = []

        if not combined_slots:
            return merged_slots

        while counter < len(combined_slots) - 1:
            is_mergable = (
                combined_slots[counter]['start_time'] <= combined_slots[counter + 1]['start_time'] <=
                combined_slots[counter]['end_time'] and combined_slots[counter]['day'] ==
                combined_slots[counter + 1]['day']
            )
            if not is_mergable:
                merged_slots.append(combined_slots[counter])
                counter += 1
                continue

            if is_mergable and combined_slots[counter + 1]['end_time'] > combined_slots[counter]['end_time']:
                combined_slots[counter + 1]['start_time'] = combined_slots[counter]['start_time']

            else:
                combined_slots[counter + 1] = combined_slots[counter]

            counter += 1

        merged_slots.append(combined_slots[-1])
        return merged_slots

    # this needs to be make configurable update the key
    final_slots = []
    count = 0
    num_weeks = getattr(settings, 'NEXT_SLOTS_LIMIT_WEEKS', 2)
    while len(slots) > count:
        slots_days = [day.day for day in slots[count].week_days.all()]
        slot = slots[count]
        # making timezone aware for start_time and end_time
        for day in slots_days:
            cur_week = 0
            while cur_week < num_weeks:
                date = get_next_date(day, cur_week)
                startDateTime = get_slot_datetime(date, slot.start_time, slot.timezone)
                endDateTime = get_slot_datetime(date, slot.end_time, slot.timezone)
                final_slots.append({
                    'start_time': startDateTime,
                    'end_time': endDateTime,
                    'day': day,
                    'date_string': startDateTime.date()
                })
                cur_week += 1

        count += 1

    final_sorted_slots = sorted(final_slots, key=itemgetter('start_time', 'day'))
    final_merge_slots = merge_final_slots(final_sorted_slots)
    return final_merge_slots


def filter_slots(available_slots, booked_slots):
    """
    Util method to filter the slots if anyslots is coming in between
    Args:
        available_slots (list): list of dict of slots on which filtering will happen
        booked_or_cancelled_slots (list): list of dict of booked or cancelled slots
    return:
        filtered_slots (list): list of dict after filtration
    Example:
        available_slots =  [
            {'start_time': datetime.time(10, 20), 'day': 3, 'end_time': datetime.time(11, 30),
            'date_string': datetime.date(2017, 4, 05)}
        ]
        booked_slots = [
            {'start_time': datetime.time(10, 30), 'day': 3, 'end_time': datetime.time(11, 00),
            'date_string': datetime.date(2017, 4, 05)}
        ]

        expected_result = [
            {'end_time': datetime.time(11, 30), 'start_time': datetime.time(11, 0), 'day': 3,
            'date_string': datetime.date(2017, 4, 05)}
        ]
    """
    merged_slots = process_and_merge_slots(available_slots)
    if not booked_slots:
        return merged_slots
    filtered_slots = []
    for booked_slot in booked_slots:
        count = 0
        if len(merged_slots) == 0:
            return filtered_slots

        # since both slots are sorted with start time, then if the current booked slots start_time is greater then
        # merged slot end_time then that slot is available, so for that append that slot in the filtred slot and
        # remove the slot from the list

        if booked_slot['start_time'] > merged_slots[count]['end_time']:
            while merged_slots and booked_slot['start_time'] > merged_slots[count]['end_time']:
                filtered_slots.append(merged_slots[count])
                merged_slots.pop(count)

        # if in any case current booked_slot start time is less than merged slot start_time
        # then in that case we will not do any thing just go for next booked slot
        if not merged_slots or booked_slot['start_time'] < merged_slots[count]['start_time']:
            continue
        # equal condition or in middle
        if (merged_slots[count]['start_time'] <= booked_slot['start_time'] <= merged_slots[count]['end_time']
            and merged_slots[count]['start_time'] <= booked_slot['end_time'] <= merged_slots[count]['end_time']
        ):
            start_time_diff = booked_slot['start_time'] - merged_slots[count]['start_time']
            end_time_diff = merged_slots[count]['end_time'] - booked_slot['end_time']
            # if booked slots in middle and available slots are splitted into two slots
            # then first update the existing slot with the left splitted slot and then for right
            # make the deepcopy and update for the next and insert to next index
            if start_time_diff.seconds >= (60 * 20) and end_time_diff.seconds >= (60 * 20):
                slot_copy = deepcopy(merged_slots[count])
                merged_slots[count]['end_time'] = booked_slot['start_time']
                filtered_slots.append(merged_slots[count])
                merged_slots.pop(count)
                slot_copy['start_time'] = booked_slot['end_time']
                merged_slots.insert(count, slot_copy)

            # if can be splitted from left then update the slot and pop that slot
            elif start_time_diff.seconds >= (60 * 20):
                merged_slots[count]['end_time'] = booked_slot['start_time']
                filtered_slots.append(merged_slots[count])
                merged_slots.pop(count)
            # if can be splitted from right then update the slot only
            elif end_time_diff.seconds >= (60 * 20):
                merged_slots[count]['start_time'] = booked_slot['end_time']
            # if there is exact map then remove that slot
            elif end_time_diff.seconds == 0:
                merged_slots.pop(count)

        else:
            # we need to pop here because slots are in sorted order and if that is not matching with first occurence
            # then that needs to be removed becasue you can not book invalid slots
            filtered_slots.append(merged_slots[count])
            merged_slots.pop(count)

    # if we have consume all booked slots and therer are already remaining slots in available slots then add allthose
    # into the filtered slots
    if merged_slots:
        filtered_slots.extend(merged_slots)
    return filtered_slots


def split_in_duration(filterd_slots, duration, time_zone=None, price=None, current_time=None):
    """
    This util method is used to split the slots in passed duration
    Args:
        filterd_slots (list): List of filtered slots
        duration (Int): this is the length of the session
        time_zone (str): user requeted timezone
        price (int): price associated with the duration
        current_time (obj): current datetime
    Return:
        splited slots in the duration

    Example:
        {
            "30": {
                "2017-04-07": [
                    {
                        "day": 5,
                        "end_time": "2017-04-07T11:30:00Z",
                        "start_time": "2017-04-07T11:00:00Z",
                        "price": 50,
                        "date_string": "2017-04-07"
                    },
                    {
                        "day": 5,
                        "end_time": "2017-04-07T12:00:00Z",
                        "start_time": "2017-04-07T11:30:00Z",
                        "price": 50,
                        "date_string": "2017-04-07"
                    }
                ],
                "2017-04-05": [
                    {
                        "day": 3,
                        "end_time": "2017-04-05T11:30:00Z",
                        "start_time": "2017-04-05T11:00:00Z",
                        "price": 50,
                        "date_string": "2017-04-05"
                    }
                ],
                "2017-04-13": [
                    {
                        "day": 4,
                        "end_time": "2017-04-13T11:30:00Z",
                        "start_time": "2017-04-13T11:00:00Z",
                        "price": 50,
                        "date_string": "2017-04-13"
                    }
                 ]
            }
        }
    """
    def _get_next_starting_time(time, duration):
        # this method will give the starting point from where filterig will start
        # here increasing by 5 minutes to get the exact first start time
        if time.minute % duration == 0:
            return time

        min_diff = duration - (time.minute % duration)
        return time + timezone.timedelta(minutes=min_diff)

    if not filterd_slots:
        return []

    if current_time is None:
        current_time = timezone.now()

    # convert the current_time into same format as the Calendar format
    current_time = timezone.datetime.strptime(current_time.strftime('%Y-%m-%d %H:%M'), '%Y-%m-%d %H:%M')
    current_time = get_slot_datetime(current_time.date(), current_time.time(), timezone.pytz.UTC)

    # Convert the filtered slots with the time_zone if timezone is otherthan UTC
    if time_zone is None:
        time_zone = 'UTC'

    if time_zone != 'UTC':
        for slots in filterd_slots:
            slots['start_time'] = slots['start_time'].astimezone(timezone.pytz.timezone(time_zone))
            slots['end_time'] = slots['end_time'].astimezone(timezone.pytz.timezone(time_zone))

        current_time = current_time.astimezone(timezone.pytz.timezone(time_zone))

    splited_slots_in_duration = []

    slot_dict = {duration: {}}
    # this needs to done because in the workflow we are updating the slots
    filterd_slots_new = deepcopy(filterd_slots)

    for slot in filterd_slots_new:
        local_slots = []

        time_diff = slot['end_time'] - slot['start_time']
        # if the time diff is less than the allocatable then don't return that slot
        # Or if the slot is a past session slot and start_time and end time is less than current time then don't return
        # otherwise make the slot start_time to current_time if start_time is less than the current_time
        if time_diff.seconds < 60 * duration or (slot['start_time'] < current_time and slot['end_time'] <= current_time):
            continue
        elif slot['start_time'] < current_time:
            slot['start_time'] = current_time

        slot['start_time'] = _get_next_starting_time(slot['start_time'], duration)
        end_time = slot['start_time'] + timezone.timedelta(minutes=duration)
        while end_time <= slot['end_time']:
            slot_date = slot['start_time'].date().strftime("%Y-%m-%d")
            if slot_dict[duration].get(slot_date) is None:
                slot_dict[duration].update({slot_date: []})

            slot_dict[duration][slot_date].append({'start_time': slot['start_time'].strftime("%H:%M")})
            slot['start_time'] = end_time
            end_time = end_time + timezone.timedelta(minutes=duration)

        # TODO MAKE the slots configurable to return max 10 result for Now for the given duration
        splited_slots_in_duration.extend(local_slots)

    return slot_dict


def split_and_update_price(final_slots, time_zone=None, current_time=None):
    """
    This util method is used to split the slots based on the session length
    Args:
        final_slots (list): list of slots data
        time_zone (str): requested timezone by user
        current_time (obj): datetime obj is used for unit testing and remove the past slots
    Return:
        slots_based_on_length (list): list of slots based on the session length
    """
    if not final_slots:
        return []

    if current_time is None:
        current_time = timezone.now()

    slots_based_on_length = []
    is_valid_timezone = time_zone in timezone.pytz.all_timezones
    if not is_valid_timezone:
        time_zone = 'UTC'

    ec_pricing_obj = SessionPricing.objects.all()
    for session_p_data in ec_pricing_obj:
        splited_slots = split_in_duration(final_slots, session_p_data.session_length, time_zone, session_p_data.price,
                                          current_time=current_time)
        slots_based_on_length.append(splited_slots)

    return slots_based_on_length


def get_booked_and_available_slots(expert_id):
    """
    Get the booked and available slots for the given expert_id
    Args:
        expert_id (int): Expert id
    return:
        new_slots (list): Filter slots excluding cancelled slots
    """
    # TODO get the list of booked slots for next 2 week from Today
    ec_session = EcSession.objects.filter(
        expert=expert_id,
        is_deleted=False
    ).order_by('scheduled_datetime')

    booked_slots = []
    for session in ec_session:
        start_datetime = session.scheduled_datetime
        end_time = start_datetime + timezone.timedelta(minutes=session.scheduled_duration)
        booked_slots.append({
            'start_time': get_slot_datetime(start_datetime.date(), start_datetime.time(), start_datetime.tzinfo),
            'end_time': get_slot_datetime(end_time.date(), end_time.time(), end_time.tzinfo),
            'date_string': session.scheduled_datetime.date()
        })

    available_slots = Calendar.objects.filter(expert__userbase=expert_id).order_by('start_time')
    return available_slots, booked_slots


def combine_slots(slots_in_duration, only_till_next_day=False, today=None):
    """
    This util method will convert duration slots into the date time object and return one list
    Args:
        slots_in_duration (list): slots which were splited in durations
        only_till_next_day (boolean): True or False
        today (object): current datetime
    Raturns:
        combined_slots (list): slots with combined date and time
    """
    if not slots_in_duration:
        return []
    combined_slots = []

    if today is None:
        today = timezone.now()

    for slot in slots_in_duration.values():
        for key, val in slot.items():
            combined_slots.extend(map(lambda x: timezone.datetime.strptime(key + 'T' + x['start_time'], '%Y-%m-%dT%H:%M'), val))

    if only_till_next_day:
        next_day = today + timezone.timedelta(days=1)
        combined_slots = [slot for slot in combined_slots if slot.date() in [today.date(), next_day.date()]]

    return sorted(combined_slots)
