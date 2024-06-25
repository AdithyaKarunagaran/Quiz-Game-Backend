import json
from datetime import datetime, timedelta

from django.http import JsonResponse
from django.utils.timezone import now, make_aware
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from quiz_game.models import JSQuestion, User_Register, admin_model


@csrf_exempt
@api_view(['POST', 'GET'])
def create_question(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if 'id' not in data or data['id'] is None or data['id'] == "":
            JSQuestion.objects.create(
                question=data["question"],
                choices=data["choices"],
                answer=data["answer"],
                created_by=data["created_by"],
                created_date=now()
            )
            response_data = [{"Message": "New Question Created"}]
        else:
            JSQuestion.objects.filter(id=data["id"]).update(
                question=data["question"],
                choices=data["choices"],
                answer=data["answer"],
                update_by=data["updated_by"],
                update_date=now()
            )
            response_data = [{"Message": "Question updated"}, {'in-id': data['id']}]
        return JsonResponse(response_data, safe=False)


@csrf_exempt
@api_view(['POST'])
def delete_question(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        question_id = data.get('id')
        JSQuestion.objects.filter(id=question_id).delete()
        return JsonResponse({"Message": "Question deleted"}, safe=False)


@api_view(['GET'])
def get_questions(request):
    if request.method == 'GET':
        questions = JSQuestion.objects.all().values()
        return JsonResponse(list(questions), safe=False)


@csrf_exempt
@api_view(["GET"])
def get_question(request):
    if request.method == 'GET':
        obj = JSQuestion.objects.all()
        data = []
        for i in obj:
            questions = {
                "question": i.question,
                "choices": i.choices,
                "answer": i.answer
            }
            data.append(questions)
        return JsonResponse(data, safe=False)


@csrf_exempt
@api_view(["POST"])
def user_register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user, created = User_Register.objects.get_or_create(
            e_mail=data["e_mail"],
            defaults={'name': data["name"], 'ph_no': data["ph_no"]}
        )
        if created:
            return JsonResponse({'Message': "New User Created"})
        else:
            return JsonResponse({'Message': "User already exists"})


@csrf_exempt
@require_http_methods(["POST"])
def submit_quiz(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = User_Register.objects.get(e_mail=data["e_mail"])
            score = data.get("score", 0)
            user.append_score(score)
            return JsonResponse({
                'Message': "Quiz Data Updated",

                'Total Attempts': user.quiz_attempts,
                'Scores': user.quiz_marks
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@api_view(['POST'])
def get_results(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        start_time = datetime.fromisoformat(data['start_time'])
        start_time = make_aware(start_time, pytz.timezone('Asia/Kolkata'))
        end_time = start_time + timedelta(hours=1)

        results = User_Register.objects.filter(updated_date__range=(start_time, end_time)).values(
            'name', 'quiz_attempts', 'quiz_marks', 'e_mail', 'ph_no'
        )

        processed_results = []
        for result in results:
            if result['quiz_marks']:
                latest_score = result['quiz_marks'][-1]
                result['latest_score'] = latest_score
            else:
                result['latest_score'] = None
            processed_results.append(result)

        return JsonResponse(processed_results, safe=False)


@csrf_exempt
@api_view(['POST'])
def admin_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        admin_id = data.get("id")
        name = data.get("name")
        password = data.get("password")

        try:
            admin = admin_model.objects.get(id=admin_id)

            if admin.name == name and admin.password == password:
                response_data = {"Message": "Admin authenticated"}
                return JsonResponse(response_data)
            else:
                response_data = {"Message": "Incorrect details"}
                return JsonResponse(response_data, status=400)

        except admin_model.DoesNotExist:
            response_data = {"Message": "Admin with provided ID not found"}
            return JsonResponse(response_data, status=400)
