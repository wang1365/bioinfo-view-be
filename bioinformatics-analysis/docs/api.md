# 用户

## 登录

```
curl --location --request POST 'http://127.0.0.1:8080/account/?action=login' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'email=2514553187@qq.com' \
--data-urlencode 'password=123456' 
```

```
{"code": 0, "msg": "", "data": {"access_token":
"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE2MDIzMjA2ODEsInN1YiI6ImFjY2VzcyJ9.5SyLbNGrRgEqHq6EpBJ-mrHBZkekclEfCo5KnuUabJ0",
"token_type": "bearer"}}
```

```
{"code": 1, "msg": "邮箱未验证, 请前往邮箱验证", "data": ""}
```

 **备注: 登录和注册使用同一个url，同一个请求方法，用action区分**

## 注册

```
curl --location --request POST 'http://127.0.0.1:8000/account/?action=register' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'username=jack' \
--data-urlencode 'email=2514553187@qq.com' \
--data-urlencode 'password=123456' \
--data-urlencode 'password_again=123456'
```

```
{"code": 0, "msg": "", "data": "验证邮件已发送, 请前往邮箱认证"}
```

```
{"code": 1, "msg": "邮箱已存在", "data": ""}
```

## 查看当前登录用户

```
curl --location --request GET 'http://127.0.0.1:8000/account/' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE2MDIzMjA1MjgsInN1YiI6ImFjY2VzcyJ9.ndWPp-OEwdsM0cYnK6z2pk0KyHbqMhyiUj3LVN8ejjY' 
```

```
{"code": 0, "msg": "", "data": {"id": 4, "username": "jack", "email": "2514553187@qq.com", "role_list": ["normal"]}}
```

## 修改用户信息

```
curl --location --request PATCH 'http://127.0.0.1:8000/account/' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0LCJleHAiOjE2MDIzMjQ2MjgsInN1YiI6ImFjY2VzcyJ9.foL8qjAt5phlAg8yl9XzAxh6lUzQtkO2JaqpjuH_hzc' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'username=jack0' \
--data-urlencode 'password=123456' \
--data-urlencode 'password_again=123456'
```

```
{"code": 0, "msg": "", "data": "更新成功"}
```

 **备注: 修改使用patch, 部分更新**

## 管理员批量删除用户

```
curl --location --request DELETE 'http://127.0.0.1:8000/account/manager' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJleHAiOjE2MDI0ODk0NjksInN1YiI6ImFjY2VzcyJ9.jpAFbRIXSQaREoeGdJP9SJHRL10WczyfC7XP0cn4xtE' \
--header 'Content-Type: application/json' \
--data-raw '{"ids": [9, 11]}'
```

```
{"code": 0, "msg": "", "data": 2}
```

```
{"code": 1, "msg": "", "msg": "非管理员用户不能删除用户"}
```



## 管理员查询用户列表

```
curl --location --request GET 'http://127.0.0.1:8000/account/manager?page=1&size=5' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJleHAiOjE2MDI0ODk0NjksInN1YiI6ImFjY2VzcyJ9.jpAFbRIXSQaREoeGdJP9SJHRL10WczyfC7XP0cn4xtE' \
--header 'Content-Type: application/json'
```



```
{
    "code": 0,
    "msg": "",
    "data": {
        "item_list": [
            {
                "id": 1,
                "username": "阿拉斯加牛^_^",
                "email": "wangxiaochuan01@163.com",
                "is_active": true,
                "role": [
                    "admin"
                ]
            },
            {
                "id": 3,
                "username": "jack",
                "email": "2514553187@qq.com",
                "is_active": true,
                "role": [
                    "admin"
                ]
            },
            {
                "id": 4,
                "username": "汤姆克鲁斯",
                "email": "0@qq.com",
                "is_active": false,
                "role": [
                    "normal"
                ]
            },
            {
                "id": 5,
                "username": "勒布朗詹姆斯",
                "email": "1@qq.com",
                "is_active": true,
                "role": []
            },
            {
                "id": 6,
                "username": "爱因斯坦",
                "email": "2@qq.com",
                "is_active": true,
                "role": []
            }
        ],
        "total_count": 12
    }
}
```

```
{"code": 1, "msg": "", "msg": "非管理员用户不能查看用户列表"}
```

## 管理员修改用户角色和禁用用户

```
curl --location --request PATCH 'http://127.0.0.1:8000/account/manager?page=1&size=15' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE2MDI2NDM1ODcsInN1YiI6ImFjY2VzcyJ9.P_ZiZSUa0vFzHvJeYED8qfe95CkNQF0cGxGhCNv9Y7k' \
--header 'Content-Type: application/json' \
--data-raw '{"userid": 3, "role": ["admin"]}'
```

```
{"code": 0, "msg": "", "data": true}
```

```
{"code": 1, "msg": "非管理员用户不能修改用户角色", "data": ""}
```





# 角色

## 查看系统已有角色

```
curl --location --request GET 'http://127.0.0.1:8000/role' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE2MDI1ODM1MjEsInN1YiI6ImFjY2VzcyJ9.qlMPPx_QrR1Uj0Ay0U9YaSJKl5JzmD1hZTtgI4aOWoQ' \
--header 'Content-Type: application/json'
```

```
{
    "code": 0,
    "msg": "",
    "data": [
        {
            "id": 1,
            "code": "admin",
            "permission2action": []
        },
        {
            "id": 2,
            "code": "normal",
            "permission2action": []
        }
    ]
}
```





# 项目

## 创建项目

```
curl --location --request POST 'http://127.0.0.1:8000/project' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE2MDgzNjI2NTksInN1YiI6ImFjY2VzcyJ9.a0OP7TvKJoyYwras5MIOWtI93FcnmfhEX9n_T1nuH80' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "jack",
    "desc": "xxx"
}'
```

```
curl --location --request POST 'http://127.0.0.1:8000/project' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2MDI1NTcxNjEsInN1YiI6ImFjY2VzcyJ9.DaypwFZE8ME53ub-wfDXjMsEE109GL5oYzaQmuNhQ6o' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "jack",
    "desc": "xxx",
    "samples": [1,2]
}
```

```
curl --location --request POST 'http://127.0.0.1:8000/project' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2MDI1NTcxNjEsInN1YiI6ImFjY2VzcyJ9.DaypwFZE8ME53ub-wfDXjMsEE109GL5oYzaQmuNhQ6o' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "jack",
    "desc": "xxx",
    "samples": [1,2],
    "members": [1,2]
}
```

```
{
    "code": 0,
    "msg": "",
    "data": {
        "id": 13,
        "name": "jack",
        "desc": "这是我的",
        "owner": "jack",
        "owner_id": "3",
        "members": [
            {
                "id": 3,
                "username": "jack",
                "email": "2514553187@qq.com"
            }
        ],
        "create_time": "2020-10-13T15:49:15.812514"
    }
}
```





## 查询用户参与的所有项目(带查询参数)

```
curl --location --request GET 'http://127.0.0.1:8000/project?name=ack&page=1&size=2' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE2MDI1NzY2MzEsInN1YiI6ImFjY2VzcyJ9.q8I5DR3YYYeU2YUIkB4P5sa-wVNEbiPtnLMxyvkIHqM' \
--header 'Content-Type: application/json'
```

```
{
    "code": 0,
    "msg": "",
    "data": {
        "item_list": [
            {
                "id": 1,
                "name": "jack",
                "desc": "这是我的",
                "owner": "阿拉斯加牛^_^",
                "samples": [],
                "owner_id": "1",
                "members": [
                    {
                        "id": 1,
                        "username": "阿拉斯加牛^_^",
                        "email": "wangxiaochuan01@163.com",
                        "create_time": "2020-10-19 15:02:07"
                    },
                    {
                        "id": 3,
                        "username": "jack",
                        "email": "2514553187@qq.com",
                        "create_time": "2020-10-19 15:02:07"
                    }
                ],
                "task_count": 5,
                "create_time": "2020-10-19T14:58:38.465182"
            }
        ],
        "total_count": 1
    }
}
```





## 查看单个项目

```
curl --location --request GET 'http://127.0.0.1:8000/project/6' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2MDc0ODc3MjMsInN1YiI6ImFjY2VzcyJ9.iItenAVT0PmUYM30B_CDlooUa-unE3kc_P-wqgc1TlA' \
--header 'Content-Type: application/json'
```

```
{
	"code": 0,
	"msg": "",
	"data": {
		"id": 2,
		"name": "王晓川的项目1",
		"desc": "test",
		"owner": "阿拉斯加牛^_^",
		"samples": [],
		"owner_id": "1",
		"members": [{
			"id": 1,
			"username": "阿拉斯加牛^_^",
			"email": "wangxiaochuan01@163.com",
			"create_time": "2020-10-26 22:31:24"
		}, {
			"id": 3,
			"username": "jack",
			"email": "2514553187@qq.com",
			"create_time": "2020-10-26 22:31:24"
		}, {
			"id": 4,
			"username": "汤姆克鲁斯",
			"email": "0@qq.com",
			"create_time": "2020-10-26 22:31:24"
		}, {
			"id": 5,
			"username": "勒布朗詹姆斯",
			"email": "1@qq.com",
			"create_time": "2020-10-26 22:31:24"
		}],
		"create_time": "2020-10-26T22:31:24.507331",
		"total_task_count": 0,
		"pending_task_count": 0,
		"running_task_count": 0,
		"finished_task_count": 0,
		"failured_task_count": 0,
		"canceled_task_count": 0
	}
}
```





## 修改项目

```
curl --location --request PUT 'http://127.0.0.1:8000/project/1' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2MDI1NTcxNjEsInN1YiI6ImFjY2VzcyJ9.DaypwFZE8ME53ub-wfDXjMsEE109GL5oYzaQmuNhQ6o' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "jack3",
    "samples": [],
    "members": [1,2]
}'
```

```
{"code": 0, "msg": "", "data": true}
```

```
{"code": 1, "msg": "非项目创建者不能修改项目", "data": false}
```



## 删除项目

```
curl --location --request DELETE 'http://127.0.0.1:8000/project/6' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE2MDgwMTYyMzAsInN1YiI6ImFjY2VzcyJ9.Pa2iVecIencT3XpgripoCRu9etnfu565tTXtYBgARaQ' \
--header 'Content-Type: application/json'
```

```
{"code": 0, "msg": "", "data": true}
```

```
{"code": 1, "msg": "非项目创建者不能删除项目", "data": false}
```



# 任务

任务状态status枚举值: PENDING、RUNNING、FINISHED、FAILURED、CANCELED



## 创建任务

priority：1 普通优先级，2 紧急优先级

创建任务先校验是否有同样的任务

```
curl --location --request POST 'http://127.0.0.1:8000/task?check_duplicate=true' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE2MDgwMTYyMzAsInN1YiI6ImFjY2VzcyJ9.Pa2iVecIencT3XpgripoCRu9etnfu565tTXtYBgARaQ' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "first",
    "samples": [5],
    "project_id": 1,
    "flow_id": 1,
    "parameter":[{"key": "name", "value": "jack2"}, {"key": "age", "value": 23}],
    "memory": 1024
}'
```

```
{"code": 1, "msg": "jack已在项目名为jack创建了任务名称为first的同样的分析任务", "data": ""}
```

```
{"code": 0, "msg": "", "data": ""}
```

校验不通过提示信息让用户选择是否继续，继续就调用如下接口，不传query参数check_duplicate



```
curl --location --request POST 'http://127.0.0.1:8000/task' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE2MDgwMTYyMzAsInN1YiI6ImFjY2VzcyJ9.Pa2iVecIencT3XpgripoCRu9etnfu565tTXtYBgARaQ' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "first",
    "samples": [5],
    "project_id": 1,
    "flow_id": 1,
    "parameter":[{"key": "name", "value": "jack"}, {"key": "age", "value": 23}],
    "memory": 1024,   
    "keep_bam": true,
    "priority": 1
}'
```

```
{
    "code": 0,
    "msg": "",
    "data": {
        "id": 15,
        "status": "PENDING",
        "project": {
            "id": 1,
            "name": "jack",
            "desc": "这是我的",
            "owner": "阿拉斯加牛^_^",
            "samples": [],
            "owner_id": "1",
            "members": [
                {
                    "id": 1,
                    "username": "阿拉斯加牛^_^",
                    "email": "wangxiaochuan01@163.com",
                    "create_time": "2020-10-19 15:02:07"
                },
                {
                    "id": 3,
                    "username": "jack",
                    "email": "2514553187@qq.com",
                    "create_time": "2020-10-19 15:02:07"
                }
            ],
            "create_time": "2020-10-19T14:58:38.465182"
        },
        "creator": {
            "id": 3,
            "username": "jack",
            "email": "2514553187@qq.com",
            "is_active": true
        },
        "name": "first",
        "progress": 0,
        "result_path": null,
        "keep_bam": false,
        "env": {
            "name": "jack",
            "age": 23,
            "sample_name_list": "测试样本",
            "sample_path_list": "1"
        },
        "memory": 1024,
        "samples": [
            1
        ],
        "parameter": [
            {
                "key": "name",
                "value": "jack"
            },
            {
                "key": "age",
                "value": 23
            }
        ],
        "create_time": "2020-10-28T15:54:45.690259",
        "update_time": "2020-10-28T15:54:45.690268",
        "flow": 1,
        "priority": 1
    }
}
```



## 删除任务

```
curl --location --request DELETE 'http://127.0.0.1:8000/task/10' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE2MDU4NTM4MTAsInN1YiI6ImFjY2VzcyJ9.U2-ndoXSyzjWLmG9tQO6zssjIiUzyJ9rnXHOnPFzK40' \
--header 'Content-Type: application/json'
```

```
{"code": 0, "msg": "", "data": true}
```

```
{"code": 1, "msg": "只有管理员和任务创建者可以删除任务", "data": false}
```



## 查看任务详情

```
curl --location --request GET 'http://127.0.0.1:8000/task/11' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE2MDU4NTM4MTAsInN1YiI6ImFjY2VzcyJ9.U2-ndoXSyzjWLmG9tQO6zssjIiUzyJ9rnXHOnPFzK40' \
--header 'Content-Type: application/json'
```

```
{
    "code": 0,
    "msg": "",
    "data": {
        "id": 11,
        "status": "RUNNING",
        "project": {
            "id": 1,
            "name": "jack",
            "desc": "这是我的",
            "owner": "阿拉斯加牛^_^",
            "samples": [],
            "owner_id": "1",
            "members": [
                {
                    "id": 1,
                    "username": "阿拉斯加牛^_^",
                    "email": "wangxiaochuan01@163.com",
                    "create_time": "2020-10-19 15:02:07"
                },
                {
                    "id": 3,
                    "username": "jack",
                    "email": "2514553187@qq.com",
                    "create_time": "2020-10-19 15:02:07"
                }
            ],
            "create_time": "2020-10-19T14:58:38.465182"
        },
        "creator": {
            "id": 3,
            "username": "jack",
            "email": "2514553187@qq.com",
            "is_active": true
        },
        "name": "first",
        "progress": 0,
        "result_path": null,
        "keep_bam": false,
        "env": {
            "age": "23",
            "name": "jack"
        },
        "memory": 1024,
        "samples": [
            1
        ],
        "parameter": [
            {
                "key": "name",
                "value": "jack"
            },
            {
                "key": "age",
                "value": 23
            }
        ],
        "create_time": "2020-10-27T14:40:43.860942",
        "update_time": "2020-10-27T14:40:43.860949",
        "flow": 1
    }
}
```



## 查看任务列表

管理员可以查看所有任务, 普通用户只能看到自己创建的任务。任务列表入口可以是项目(传项目id)，否则就展示所有关联项目的任务。

```
curl --location --request GET 'http://127.0.0.1:8000/task?page=1&size=2&status=PENDING' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE2MDgwMTYyMzAsInN1YiI6ImFjY2VzcyJ9.Pa2iVecIencT3XpgripoCRu9etnfu565tTXtYBgARaQ' \
--header 'Content-Type: application/json'
```

```
{
	"code": 0,
	"msg": "",
	"data": {
		"item_list": [{
			"id": 97,
			"status": "PENDING",
			"project": {
				"id": 8,
				"name": "xx1",
				"desc": "xxx",
				"code": null,
				"owner": "jack",
				"samples": [],
				"owner_id": "3",
				"members": [{
					"id": 3,
					"username": "jack",
					"email": "2514553187@qq.com",
					"department": "1",
					"create_time": "2020-11-20 15:15:49"
				}],
				"task_count": 1,
				"create_time": "2020-11-20T15:15:48.963695"
			},
			"creator": {
				"id": 1,
				"username": "阿拉斯加牛^_^",
				"email": "admin@nanodigmbio.com",
				"is_active": true,
				"department": "1"
			},
			"name": "ceshi",
			"progress": 0,
			"pid": null,
			"is_merge": false,
			"result_path": null,
			"result_dir": null,
			"keep_bam": false,
			"has_cleaned": false,
			"is_qc": false,
			"env": {},
			"priority": 1,
			"memory": 1024,
			"samples": ["5"],
			"parameter": null,
			"create_time": "2020-12-07T18:00:52.501312",
			"update_time": "2020-12-07T18:00:52.506095",
			"flow": {
				"id": 6,
				"name": "ff123",
				"code": "1",
				"desp": "",
				"owner_id": 1,
				"create_time": "2020-10-27T23:13:42.612630",
				"update_time": "2020-11-23T09:50:01.602095",
				"location": "fffffff",
				"alignment_tool": "sfdsafd",
				"parameter_schema": "[]",
				"sample_type": "multiple",
				"flow_type": "normal",
				"flow_category": "",
				"allow_nonstandard_samples": false,
				"details": "",
				"members": []
			}
		}, {
			"id": 96,
			"status": "PENDING",
			"project": {
				"id": 16,
				"name": "这是qc",
				"desc": "xxx",
				"code": "qc",
				"owner": "jack",
				"samples": [6, 5],
				"owner_id": "3",
				"members": [{
					"id": 3,
					"username": "jack",
					"email": "2514553187@qq.com",
					"department": "1",
					"create_time": "2020-11-24 15:26:38"
				}],
				"task_count": 13,
				"create_time": "2020-11-24T15:26:38.731430"
			},
			"creator": {
				"id": 1,
				"username": "阿拉斯加牛^_^",
				"email": "admin@nanodigmbio.com",
				"is_active": true,
				"department": "1"
			},
			"name": "undefined",
			"progress": 100,
			"pid": null,
			"is_merge": true,
			"result_path": "/tmp/QL-191130-1-P65.txt",
			"result_dir": null,
			"keep_bam": false,
			"has_cleaned": false,
			"is_qc": false,
			"env": {
				"OUT_DIR": "/tmp/nano/web/阿拉斯加牛^_^/qc/20201201/ff123/96",
				"IS_MERGE": "1",
				"TASK_URL": "http://192.168.10.63:8000/task/96",
				"MERGE_SAMPLE_FILES": "/tmp/nano/result/other/jack/qc/ff123/20201130/89/QL-191130-1-P65/QL-191130-1-P65.txt,/tmp/nano/result/other/jack/qc/ff123/20201130/89/QL-191130-2-P66/QL-191130-2-P66.txt"
			},
			"priority": 1,
			"memory": 1024,
			"samples": ["6"],
			"parameter": [],
			"create_time": "2020-12-01T16:52:41.768822",
			"update_time": "2020-12-01T16:59:06.435762",
			"flow": {
				"id": 6,
				"name": "ff123",
				"code": "1",
				"desp": "",
				"owner_id": 1,
				"create_time": "2020-10-27T23:13:42.612630",
				"update_time": "2020-11-23T09:50:01.602095",
				"location": "fffffff",
				"alignment_tool": "sfdsafd",
				"parameter_schema": "[]",
				"sample_type": "multiple",
				"flow_type": "normal",
				"flow_category": "",
				"allow_nonstandard_samples": false,
				"details": "",
				"members": []
			}
		}],
		"total_count": 3
	}
}
```

```
curl --location --request GET 'http://127.0.0.1:8000/task?page=1&size=1&project_id=1' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE2MDU4NTM4MTAsInN1YiI6ImFjY2VzcyJ9.U2-ndoXSyzjWLmG9tQO6zssjIiUzyJ9rnXHOnPFzK40' \
--header 'Content-Type: application/json'
```



## 更新任务

```
curl --location --request PUT 'http://127.0.0.1:8000/task/11' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE2MDgwMTYyMzAsInN1YiI6ImFjY2VzcyJ9.Pa2iVecIencT3XpgripoCRu9etnfu565tTXtYBgARaQ' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "second",
    "priority": 2
}'
```

```
{
	"code": 0,
	"msg": "",
	"data": {
		"id": 11,
		"status": "RUNNING",
		"project": {
			"id": 1,
			"name": "jack",
			"desc": "这是我的",
			"owner": "阿拉斯加牛^_^",
			"samples": [],
			"owner_id": "1",
			"members": [{
				"id": 1,
				"username": "阿拉斯加牛^_^",
				"email": "wangxiaochuan01@163.com",
				"create_time": "2020-10-19 15:02:07"
			}, {
				"id": 3,
				"username": "jack",
				"email": "2514553187@qq.com",
				"create_time": "2020-10-19 15:02:07"
			}],
			"create_time": "2020-10-19T14:58:38.465182"
		},
		"creator": {
			"id": 3,
			"username": "jack",
			"email": "2514553187@qq.com",
			"is_active": true
		},
		"name": "second",
		"progress": 0,
		"result_path": "/Users/guwanhua/Downloads/zookeeper_test.zip",
		"result_dir": null,
		"keep_bam": false,
		"has_cleaned": false,
		"env": {
			"age": "23",
			"name": "jack"
		},
		"memory": 1024,
		"samples": [1],
		"parameter": [{
			"key": "name",
			"value": "jack"
		}, {
			"key": "age",
			"value": 23
		}],
		"create_time": "2020-10-27T14:40:43.860942",
		"update_time": "2020-10-27T14:40:43.860949",
		"flow": 1
	}
}
```

取消排队中的任务：

```
curl --location --request PUT 'http://127.0.0.1:8000/task/11?action=cancel' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE2MDgwMTYyMzAsInN1YiI6ImFjY2VzcyJ9.Pa2iVecIencT3XpgripoCRu9etnfu565tTXtYBgARaQ' \
--header 'Content-Type: application/json'
```

重启失败的任务:

```
curl --location --request PUT 'http://127.0.0.1:8000/task/11?action=restart' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE2MDgwMTYyMzAsInN1YiI6ImFjY2VzcyJ9.Pa2iVecIencT3XpgripoCRu9etnfu565tTXtYBgARaQ' \
--header 'Content-Type: application/json'
```



## 下载结果文件

```
curl --location --request GET 'http://127.0.0.1:8000/task/download/82' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE2MDU4NTM4MTAsInN1YiI6ImFjY2VzcyJ9.U2-ndoXSyzjWLmG9tQO6zssjIiUzyJ9rnXHOnPFzK40' \
--header 'Content-Type: application/json'
```

## 创建QC任务

```
curl --location --request POST 'http://127.0.0.1:8000/task/run_qc' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE2MDU4NTM4MTAsInN1YiI6ImFjY2VzcyJ9.U2-ndoXSyzjWLmG9tQO6zssjIiUzyJ9rnXHOnPFzK40' \
--header 'Content-Type: application/json' \
--data-raw '{
    "sample_id": 5
}'
```



# 系统配置

## 查看内置配置

**两个配置参数，最大运行任务数max_task(value > 1的整数)，内存使用率memory_rate(0-1.0)**

```
curl --location --request GET 'http://127.0.0.1:8000/config' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2MDgxMDU0MDMsInN1YiI6ImFjY2VzcyJ9.lffnFLgXbDrIL0RICyDcnUf3hpj8wxUNtNoowJoh5XU'
```

```
{
    "code": 0,
    "msg": "",
    "data": {
        "count": 2,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 2,
                "name": "max_task",
                "value": 10.0,
            },
            {
                "id": 1,
                "name": "memory_rate",
                "value": 0.7,
            }
        ]
    }
}
```

## 修改内置配置

```
curl --location --request PUT 'http://127.0.0.1:8000/config/1' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2MDgxMDU0MDMsInN1YiI6ImFjY2VzcyJ9.lffnFLgXbDrIL0RICyDcnUf3hpj8wxUNtNoowJoh5XU' \
--header 'Content-Type: application/json' \
--data-raw '{"value": 0.9}'
```

```
{"code": 0, "msg": "success", "data": {"id": 1, "name": "memory_rate", "value": 0.9}}
```



