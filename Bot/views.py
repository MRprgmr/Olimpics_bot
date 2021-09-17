from Bot.models import Olympiad, User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer


class check_user(APIView):

    renderer_classes = [JSONRenderer]

    def get(self, request):
        PARAMS = dict(request.query_params)
        print(PARAMS)
        try:
            olympiad = Olympiad.objects.get(id=int(PARAMS['olympiad_id'][0]))
            olympiad: Olympiad
            user = User.objects.get(telegram_id=int(PARAMS['user_id'][0]))
            user: User
            if user in olympiad.registered_users.all():
                result = {
                    'status': 'accepted',
                    'telegram_id': PARAMS['user_id'][0],
                    'full_name': user.full_name,
                    'class_name': user.grade.name,
                    'phone_number': user.phone_number
                }
                return Response(result)
            else:
                return Response({
                    'status': 'not_found',
                })
        except Exception as er:
            return Response({
                    'status': 'not_found',
                })


class get_olympiads(APIView):
    
    renderer_classes = [JSONRenderer]

    def get(self, request):
        data = Olympiad.objects.filter(status=True)  
        olympiads = []
        for item in data:
            item: Olympiad
            olympiads.append({
                'id': item.id,
                'title': item.title
            })
        return Response(olympiads)