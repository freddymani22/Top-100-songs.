from rest_framework import serializers
from songs.models import BillBoard


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillBoard
        fields = [
            'date',
        "rank",
        "song",
        "artist",
        "last_week",
        "peak_rank",
        "weeks_on_board"
        ]