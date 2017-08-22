from celery import shared_task

from feeds.models import Content, ContentStats
from streamfeeds.utils import StreamHelper


@shared_task
def modify_tags_on_getstream(user_id, new_tag_ids, existing_tags_ids, content_id, super_admin=True):
    """
    Celery Task to add and remove feeds from getstream .
    Args:
        user_id : The id of user
        new_tag_ids: List of new tag ids
        existing_tags_ids: List of existing Tag ids
        content_id:The id of Content object
        super_admin (True): By default to True, because Superuser can only modify the tags
    Return: Boolean value True
    """
    streamhelper = StreamHelper()

    # Add feeds on Getstream
    tag_id_push_getstream = list(set(new_tag_ids) - set(existing_tags_ids))
    if tag_id_push_getstream:
        streamhelper.expert_publish_content(user_id, content_id, tag_ids=tag_id_push_getstream, super_admin=super_admin)

    # Remove Feeds from Getstream
    tag_ids_remove_getstream = list(set(existing_tags_ids) - set(new_tag_ids))
    for tag_id in tag_ids_remove_getstream:
        streamhelper.remove_content_tag_feeds(content_id, tag_id)


@shared_task
def delete_content_from_getstream(owner_id, content_id):
    """
    Celery Task to remove the content from getstream when deleting the content
    Args:
        owner_id (id): The id of owner
        content_id (id):The id of Content object
    Return:
        None
    """
    StreamHelper().remove_content_feeds(owner_id, content_id)


@shared_task
def like_or_unlike_content(content_id, user_activity):
    """
    Celery task to increase and decrease the count of like for a content.
    Args:
        content_id : Content object Id.
        user_activity : type of user activity(like or dislike)
    Return: None
    """
    content = Content.objects.get(id=content_id)
    try:
        stats = content.stats
    except Content.stats.RelatedObjectDoesNotExist:
        # When the comment will be liked for the first time
        stats = ContentStats.objects.create(content=content)
    if user_activity == 'like':
        stats.likes += 1
    if user_activity == 'dislike':
        stats.likes -= 1
    stats.save()
