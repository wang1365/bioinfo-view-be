import os
import json

from task.models import Task
from core import generate_df, extract_meta_data, extract_data
from constant import FILE_MAPPINGS


def get_meta_data(request, taskid, name):
    config = FILE_MAPPINGS[name]
    task = Task.models.get(id=taskid)
    filename = os.path.join(task.result_path, config['filepath'])
    columns = json.loads(request.body)
    df = generate_df(filename, sep=config['sep'], header=config['header'])
    return extract_meta_data(df, columns)


def get_raw_data(request, taskid, name):
    config = FILE_MAPPINGS[name]
    task = Task.models.get(id=taskid)
    filename = os.path.join(task.result_path, config['filepath'])
    query = json.loads(request.body)
    df = generate_df(filename, sep=config['sep'], header=config['header'])
    return extract_data(df, query)
