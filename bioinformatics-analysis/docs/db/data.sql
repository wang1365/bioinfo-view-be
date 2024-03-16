
INSERT INTO public.account (id, username, nickname, email, password, department, is_active, is_delete, disk_limit, used_disk, create_time, update_time, parent_id, task_count, task_limit)
VALUES (1, 'super', '超级管理员', 'super@super.com', '62c8ad0a15d9d1ca38d5dee762a16e01', null, true, false, null, 3894733, '2022-09-14 12:31:08.259631 +00:00', '2024-03-16 01:09:44.176449 +00:00', null, 487, null);
INSERT INTO public.account (id, username, nickname, email, password, department, is_active, is_delete, disk_limit, used_disk, create_time, update_time, parent_id, task_count, task_limit)
VALUES (2, 'admin', '管理员', 'admin@admin.com', '62c8ad0a15d9d1ca38d5dee762a16e01', null, true, false, 30000, 0, '2022-09-14 12:31:08.263026 +00:00', '2024-03-15 08:06:51.412373 +00:00', 1, 1, 1);


INSERT INTO public.role (id, code) VALUES (1, 'super');
INSERT INTO public.role (id, code) VALUES (2, 'admin');
INSERT INTO public.role (id, code) VALUES (3, 'normal');

INSERT INTO public.user2role (id, role_id, user_id) VALUES (1, 1, 1);
INSERT INTO public.user2role (id, role_id, user_id) VALUES (2, 2, 2);