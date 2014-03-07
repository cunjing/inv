# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render_to_response('inv/index.html', {}, context_instance=RequestContext(request))


def site_help(request):
    return render_to_response('inv/index.html')


def contact(request):
    return render_to_response('inv/index.html')


def terms(request):
    return render_to_response('inv/index.html')


def privacy(request):
    return render_to_response('inv/index.html')


@csrf_exempt
def import_excel(request):
    data = {
        'info': '',
        'name': '',
        'size': 0,
    }

    if request.method == 'POST':
        f = request.FILES['file']
        data['name'] = f.name
        data['size'] = f.size / 1024
        if 'xls' not in f.name and 'xlsx' not in f.name:
            data['info'] = 'file type must be excel!'
        elif 0 == f.size:
            data['info'] = 'file content is empty!'
        else:
            import xlrd
            from matching.models import QuestionType, QuestionGroup, QuestionSubGroup, Question, QuestionOfAnswerChoice

            xls = xlrd.open_workbook(file_contents=f.read())
            sheet = xls.sheet_by_index(0)
            num_rows = sheet.nrows

            user_type = 1  # investee
            question_types = {}  # name: id
            cur_question_group = {'id': 0, 'name': '', 'order': 0}
            cur_question_sub_group = {'id': 0, 'name': '', 'order': 0}

            # index in row
            # ignore 0 Ques-User
            # 1 Ques-Group
            # 2 Ques-Sub-group
            # ignore 3 Ques-ID
            # ignore 4 Scr-Order
            # ignore 5 Sub-Scr-Order
            # special ignorance 6 Ques-Order
            # 7 Ques-Type
            # 8 Question-Title
            # ignore 9, 10 (col J, K)
            # ignore 11 No--of-Ans-Ch
            # 12 - 19 AC1 - AC8
            # ignore 20 No-of-Ans
            # ignore 21 - 25 Answer 1 - Answer 5
            for i in range(6, num_rows):
                row = sheet.row_values(i)

                # question type
                row[7] = row[7].strip(' ').upper()
                if row[7] not in question_types:
                    tmp = QuestionType(name=row[7])
                    tmp.save()
                    question_types[row[7]] = tmp.id
                    del tmp

                # question group
                row[1] = row[1].strip(' ').upper()
                if row[1] != cur_question_group['name']:
                    cur_question_group['name'] = row[1]
                    cur_question_group['order'] += 1
                    tmp = QuestionGroup(user_type=user_type,
                                        order=cur_question_group['order'],
                                        name=cur_question_group['name'])
                    tmp.save()
                    cur_question_group['id'] = tmp.id
                    del tmp

                # question sub group
                row[2] = row[2].strip(' ').upper()
                if row[2] != cur_question_sub_group['name']:
                    cur_question_sub_group['name'] = row[2]
                    cur_question_sub_group['order'] += 1
                    tmp = QuestionSubGroup(question_group=user_type,
                                           order=cur_question_sub_group['order'],
                                           name=cur_question_sub_group['name'])
                    tmp.save()
                    cur_question_sub_group['id'] = tmp.id
                    del tmp

                data['x'] = 'x'
                break

    return render_to_response('inv/import_excel.html', data)
