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
        'info': 'please select excel file to import.',
        'name': '',
        'size': 0,
        'handled_rows': 0
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
            from account.models import UserType
            from matching.models import QuestionType, QuestionGroup, QuestionSubGroup, Question, QuestionOfAnswerChoice

            tmp = xlrd.open_workbook(file_contents=f.read())
            sheet = tmp.sheet_by_index(0)
            del tmp, f
            num_rows = sheet.nrows

            user_type = UserType.objects.get(id=1)  # investee
            map_question_types = {
                'TX': {'obj': None, 'name': 'Text'},
                'MT': {'obj': None, 'name': 'Multiple Text'},
                'MC': {'obj': None, 'name': 'Multiple Choice'},
                'SC': {'obj': None, 'name': 'Single Choice'},
                'SN': {'obj': None, 'name': 'Single Number'},
                'MN': {'obj': None, 'name': 'Multiple Number'},
                'NR': {'obj': None, 'name': 'Number Range'},
                'YN': {'obj': None, 'name': 'Yes/No'},
                'BR': {'obj': None, 'name': 'Branch'},
                'DT': {'obj': None, 'name': 'Date'},
                'UV': {'obj': None, 'name': 'Upload Video'},
                'UW': {'obj': None, 'name': 'Upload WORD file'},
                'UE': {'obj': None, 'name': 'Upload Excel File'},
                'UP': {'obj': None, 'name': 'Upload PPT'},
                'UG': {'obj': None, 'name': 'Upload Graphic'},
                'UF': {'obj': None, 'name': 'Upload PDF'},
            }
            cur_question_group = None
            cur_question_sub_group = None
            cur_question_order_in_sub_group = 0

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
                data['handled_rows'] += 1

                # handle question type
                row[7] = row[7].strip(' ').upper()
                if row[7] in ['LB', 'LE']:
                    continue
                if 'TT' != row[7] and None is map_question_types[row[7]]['obj']:
                    tmp = QuestionType.objects.create(name=map_question_types[row[7]]['name'])
                    map_question_types[row[7]]['obj'] = tmp
                    del tmp

                row[8] = row[8].strip(' ')  # question title

                # handle question group and sub group
                if row[7] == 'TT':
                    row[1] = row[1].strip(' ').upper()  # question group
                    row[2] = row[2].strip(' ').upper()  # question sub group

                    # question group
                    if None is cur_question_group or row[1] != cur_question_group.name:
                        if None is cur_question_group:
                            tmp = 1
                        else:
                            tmp = 1 + cur_question_group.order
                        cur_question_group = QuestionGroup.objects.create(user_type=user_type,
                                                                          order=tmp,
                                                                          name=row[1],
                                                                          title=row[8])
                        del tmp
                        cur_question_sub_group = None

                    # question sub group
                    if row[2] != 'TITL' and (None is cur_question_sub_group or row[2] != cur_question_sub_group.name):
                        if None is cur_question_sub_group:
                            tmp = 1
                        else:
                            tmp = 1 + cur_question_sub_group.order
                        cur_question_sub_group = QuestionSubGroup.objects.create(question_group=cur_question_group,
                                                                                 order=tmp,
                                                                                 name=row[2],
                                                                                 title=row[8])
                        del tmp
                        cur_question_order_in_sub_group = 0

                    continue
                elif None is cur_question_sub_group or row[2] != cur_question_sub_group.name:  # question sub group
                    if None is cur_question_sub_group:
                        tmp = 1
                    else:
                        tmp = 1 + cur_question_sub_group.order
                    cur_question_sub_group = QuestionSubGroup.objects.create(question_group=cur_question_group,
                                                                             order=tmp,
                                                                             name=row[2],
                                                                             title=cur_question_group.title)
                    del tmp
                    cur_question_order_in_sub_group = 0

                # handle question
                cur_question_order_in_sub_group += 1
                question = Question.objects.create(question_group=cur_question_group,
                                                   question_sub_group=cur_question_sub_group,
                                                   question_type=map_question_types[row[7]]['obj'],
                                                   order=cur_question_order_in_sub_group,
                                                   title=row[8])

                # handle question of answer choice
                if row[7] in ['MC', 'SC']:
                    for j in range(12, 19):
                        row[j] = row[j].strip(' ')
                        if row[j]:
                            QuestionOfAnswerChoice.objects.create(question=question,
                                                                  order=j-11,
                                                                  title=row[j])

            data['info'] = 'importation completed.'

    return render_to_response('inv/import_excel.html', data)
