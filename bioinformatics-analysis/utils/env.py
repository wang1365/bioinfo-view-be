import os

# 获取环境变量
bio_root = os.getenv("BIO_ROOT") or '/data/bioinfo'
image_dir = os.path.join(bio_root, "image_dir")
data_dir = os.getenv("DATA_DIR") or '/data/bioinfo/data_dir'
database_dir = os.getenv("DATABASE_DIR") or '/data/bioinfo/database_dir'
sample_dir = os.getenv("SAMPLE_DIR") or '/data/bioinfo/sample_dir'
task_result_dir = os.getenv("TASK_RESULT_DIR") or '/data/bioinfo/task'

all = {
    "BIO_ROOT": bio_root,
    "IMAGE_DIR": image_dir,
    "DATA_DIR": data_dir,
    "DATABASE_DIR": database_dir,
    "SAMPLE_DIR": sample_dir,
    "TASK_RESULT_DIR": task_result_dir,
}
