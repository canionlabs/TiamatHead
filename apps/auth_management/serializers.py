from django.contrib.auth.models import User, Group

from rest_framework import serializers

from apps.auth_management.models import Organization


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', "first_name", "last_name")


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name",)


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    users = serializers.HyperlinkedRelatedField(
        many=True, view_name='auth_management:detail-users', read_only=True
    )
    organization_id = serializers.UUIDField()

    class Meta:
        model = Organization
        fields = ('organization_id', 'name', 'users')

    def get_organization_id(self, obj):
        return obj.id


class OrganizationUserSerializer(serializers.Serializer):
    users = serializers.ListField()

    @staticmethod
    def check_users(users):
        user_map = {}
        for username in users:
            user_query = User.objects.filter(username=username)
            if not user_query.exists():
                return serializers.ValidationError(
                    f"{username} is not a valid username."
                )
            user_map[username] = user_query.first()
        return user_map

    def validate_users(self, value):
        return self.check_users(value)

    def check_organization(self):
        org_params = self.context.get('view').kwargs
        organization = Organization.objects.filter(**org_params)
        if organization.exists():
            return organization
        return serializers.ValidationError(
            f"{org_params.pk} is not a valid organization."
        )

    def get_organization(self):
        return self.check_organization()[0]

    def validate(self, attrs):
        self.check_organization()
        return attrs

    def create(self, validated_data):
        user_dict = validated_data.pop('users')
        organization = self.get_organization()
        for user in user_dict.values():
            organization.users.add(user)
        serializer_filler = {'users': user_dict.keys()}
        return serializer_filler
