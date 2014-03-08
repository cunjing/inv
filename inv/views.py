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

            tmp = xlrd.open_workbook(file_contents=f.read())
            sheet = tmp.sheet_by_index(0)
            del tmp
            num_rows = sheet.nrows

            user_type = 1  # investee
            map_question_types = {
                'TX': {'id': 0, 'name': 'Text'},
                'MT': {'id': 0, 'name': 'Multiple Text'},
                'MC': {'id': 0, 'name': 'Multiple Choice'},
                'SC': {'id': 0, 'name': 'Single Choice'},
                'SN': {'id': 0, 'name': 'Single Number'},
                'MN': {'id': 0, 'name': 'Multiple Number'},
                'NR': {'id': 0, 'name': 'Number Range'},
                'YN': {'id': 0, 'name': 'Yes/No'},
                'BR': {'id': 0, 'name': 'Branch'},
                'DT': {'id': 0, 'name': 'Date'},
                'UV': {'id': 0, 'name': 'Upload Video'},
                'UW': {'id': 0, 'name': 'Upload WORD file'},
                'UE': {'id': 0, 'name': 'Upload Excel File'},
                'UP': {'id': 0, 'name': 'Upload PPT'},
                'UG': {'id': 0, 'name': 'Upload Graphic'},
                'UF': {'id': 0, 'name': 'Upload PDF'},
            }
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
            # 7 Ques-Type (ignore TT, LB, LE)
            # 8 Question-Title
            # ignore 9, 10 (col J, K)
            # ignore 11 No--of-Ans-Ch
            # 12 - 19 AC1 - AC8
            # ignore 20 No-of-Ans
            # ignore 21 - 25 Answer 1 - Answer 5
            for i in range(6, num_rows):
                row = sheet.row_values(i)

                # handle question type
                row[7] = row[7].strip(' ').upper()
                if row[7] in ['LB', 'LE']:
                    continue
                if row[7] != 'TT' and 0 == map_question_types[row[7]]['id']:
                    tmp = QuestionType.objects.create(name=map_question_types[row[7]]['name'])
                    map_question_types[row[7]]['id'] = tmp.id
                    del tmp

                # handle question group and sub group
                if row[7] == 'TT':
                    row[1] = row[1].strip(' ').upper()  # question group
                    row[2] = row[2].strip(' ').upper()  # question sub group
                    row[8] = row[8].strip(' ')  # question title

                    # question group
                    if row[1] != cur_question_group['name']:
                        cur_question_group['name'] = row[1]
                        cur_question_group['order'] += 1
                        tmp = QuestionGroup.objects.create(user_type=user_type,
                                                           order=cur_question_group['order'],
                                                           name=cur_question_group['name'],
                                                           title=row[8])
                        cur_question_group['id'] = tmp.id
                        del tmp

                    # question sub group
                    if row[2] != cur_question_sub_group['name']:
                        cur_question_sub_group['name'] = row[2]
                        cur_question_sub_group['order'] += 1
                        tmp = QuestionSubGroup.objects.create(question_group=user_type,
                                                              order=cur_question_sub_group['order'],
                                                              name=cur_question_sub_group['name'],
                                                              titile=row[8])
                        cur_question_sub_group['id'] = tmp.id
                        del tmp

                data['x'] = 'x'
                break

    return render_to_response('inv/import_excel.html', data)
