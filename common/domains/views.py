from rest_framework import permissions, viewsets

from experchat.enumerations import TagTypes
from experchat.models.domains import Tag
from experchat.serializers import TagSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Allows readonly access to domain-tags.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = super(TagViewSet, self).get_queryset()

        try:
            parent_id = int(self.request.query_params.get('parent', ''))
        except ValueError:
            parent_id = None

        queryset = queryset.filter(
            domain=self.kwargs.get('domain_id'),
            parent=parent_id,
            tag_type__in=(TagTypes.PARENT.value, TagTypes.CHILD.value)
            )
        return queryset
