from rest_framework.views import APIView
from rest_framework import permissions, generics
from .serializers import MusicSerializer
from songs.models import BillBoard
from rest_framework.response import Response
from dateutil.parser import parse


class MusicListView(generics.ListCreateAPIView):
    queryset =BillBoard.objects.all()
    serializer_class = MusicSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MusicDateAPIView(APIView):
    def get(self, request):
        date =request.query_params.get('date')
        date = parse(date).date()
        print(date)
        qs = BillBoard.objects.filter(
                    date__lte=date).order_by('-date')[:100]
        if qs.exists():
            data = MusicSerializer(qs, many = True).data
            return Response(data)
        qs = BillBoard.objects.all()
        data = MusicSerializer(qs).data
        return Response(data)




class ArtistListAPIView(APIView):
      def get(self, request):
        singer =request.query_params.get('singer')
        qs =BillBoard.objects.filter(artist__contains=singer)
        if qs.exists():
            data = MusicSerializer(qs, many = True).data
            return Response(data)
        qs = BillBoard.objects.all()
        data = MusicSerializer(qs).data
        return Response(data)
