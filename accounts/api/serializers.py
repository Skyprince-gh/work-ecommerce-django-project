from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate


User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone', 'password')
        extra_kwargs = {'password':{'write_only': True}, }

        def create(self, validated_data):
            user = User.objects.create(**validated_data)
            return user



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone', 'name', 'registered_on')



class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(
        style= { 'input_type': 'password' },
        trim_whitespace = False
    )

    def validate(self, data):
        print(data)
        phone = data.get('phone')
        password = data.get('password')

        if phone and password:
            if User.objects.filter(phone = phone).exists():
                print(phone, password)
                user = authenticate(request = self.context.get('request'), phone = phone, password = password)
                print(user)

            else:
                msg = {
                    'status': False,
                    'detail': 'Phone number not found'
                }
                raise serializers.ValidationError(msg)
            if not user:
                msg: {
                    'status': False,
                    'detail': "Phone and Password mismatch"
                }
                raise serializers.ValidationError(msg, code = 'authorization')
        else:
            msg: {
                'status': False,
                'detail': "phone and password not found in request"
            }
            raise serializers.ValidationError(msg, code = 'authorization')
        data['user'] = user
        return data