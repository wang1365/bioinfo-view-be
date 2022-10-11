"""前端直接传递 Q 表达式, 进行单表的完全查询"""

from django.db.models import Q
# 
# q = {
#     '_connector':
#     'OR',
#     '_negated':
#     False,
#     'args': [{
#         '_connector':
#         'AND',
#         '_negated':
#         False,
#         'args': [['email', 'admin'], {
#             '_connector': 'AND',
#             '_negated': False,
#             'args': [
#                 ['email', 'admin'],
#             ],
#             'kwargs': {
#                 'password__startswith': 'test',
#                 'email': 'testemail'
#             }
#         }],
#         'kwargs': {
#             'password__startswith': 'test',
#             'email': 'testemail'
#         }
#     }, ['username__in', ['admasdfasdfin', 'xadminxxx']]],
#     'kwargs': {
#         'username__in': ['adasdfasdfasdfmin', 'xadminxxx'],
#         'password': 'test',
#         'create_time__gte': '2022-11-01'
#     }
# }


def build_q(q):
    q_args = q.pop('args', [])
    q_kwargs = q.pop('kwargs', {})
    if not q_args:
        return Q(**q, **q_kwargs)

    args = []

    for item in q_args:
        if isinstance(item, list):
            args.append(Q(**{item[0]: item[1]}))
        elif isinstance(item, dict):
            args.append(build_q(item))
    return Q(*args, **q, **q_kwargs)
