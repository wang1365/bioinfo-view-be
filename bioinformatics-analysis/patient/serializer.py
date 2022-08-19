import mimetypes
import io

from rest_framework import serializers

from patient.models import Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class FileSerializer(serializers.Serializer):
    file = serializers.FileField(use_url=False)

    def validate(self, attrs):
        if mimetypes.guess_type(getattr(attrs['file'], "name", ""))[0] != 'text/csv':
            raise serializers.ValidationError("The file you uploaded is not in csv format")

        c = attrs['file'].read()
        charset = attrs['file'].charset
        if not charset:
            charset = 'utf-8'
        try:
            f = io.StringIO(c.decode(charset))
        except Exception as err:
            raise serializers.ValidationError("parse file error. %s" % err)
        attrs['file'] = f
        return attrs