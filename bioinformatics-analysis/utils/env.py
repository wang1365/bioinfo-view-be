
import os

# 获取环境变量
bio_root = os.getenv("BIO_ROOT") or '/data/bioinfo'
image_dir = os.path.join(bio_root, "image_dir")
database_dir = os.getenv("DATABASE_ROOT") or '/data/bioinfo/database_dir'
task_result_dir = os.getenv("TASK_RESULT_DIR") or '/data/bioinfo/task'

