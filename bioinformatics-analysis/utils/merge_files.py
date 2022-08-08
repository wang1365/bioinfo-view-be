import zipfile
import os
from task.models import Task

def merge_files(origin_file_list: list, dest_dir, task_id):
    filename = os.path.join(dest_dir, "result.zip")
    f = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
    Task.objects.filter(id=task_id).update(progress=10, status=2)
    for item in origin_file_list:
        os.chdir(os.path.dirname(item))
        f.write(os.path.basename(item))
    f.close()
    Task.objects.filter(id=task_id).update(result_path=filename, progress=100, status=3)




