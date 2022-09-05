# 用户

## 月注册用户统计

```buildoutcfg
curl --location --request GET 'http://127.0.0.1:9001/account/summary' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE2NjMwNjQxOTcsInN1YiI6ImFjY2VzcyJ9.F_GfkaaIEk-QZhyf9UjEH2sruKCzdWCSlSGLXHBE6qs' \
--header 'Content-Type: application/json'
```

```buildoutcfg
{"code": 0, "msg": "", "data": [{"month": "2022-08-01 00:00:00", "count": 1}]}
```

## 登录

```
curl --location --request POST 'http://127.0.0.1:8080/account/login' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'username=admin@admin.com' \
--data-urlencode 'password=1234qwer'
```

```
{"code": 0, "msg": "", "data": {"access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE2NjI1OTk3MjMsInN1YiI6ImFjY2VzcyJ9.XazpV3L98Ep6DBwntXXVRSIo-RsnxRXCtJnE7I-mRaE", "token_type": "bearer"}}
```

```
{"code": 401, "msg": "用户名或密码错误", "data": ""}
```


## 管理员创建普通账号

```
curl --location --request POST 'http://127.0.0.1:8080/account/create_user' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE2NjI1OTk3MjMsInN1YiI6ImFjY2VzcyJ9.XazpV3L98Ep6DBwntXXVRSIo-RsnxRXCtJnE7I-mRaE' \
--data-urlencode 'username=jack' \
--data-urlencode 'password=123456' \
--data-urlencode 'password_again=123456'
```

```
{"code": 0, "msg": "", "data": {"id": 8, "username": "jack", "email": "", "is_active": false, "department": null}}
```

```
{"code": 1, "msg": "用户名已存在", "data": ""}
```

## 查看当前登录用户

```
curl --location --request GET 'http://127.0.0.1:8080/account/me' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE2NjI1OTk3MjMsInN1YiI6ImFjY2VzcyJ9.XazpV3L98Ep6DBwntXXVRSIo-RsnxRXCtJnE7I-mRaE' 
```

```
{"code": 0, "msg": "", "data": {"id": 8, "username": "jack", "email": "", "is_active": true, "department": null, "role_list": ["normal"]}}```
```

## 管理员重置用户密码

```
curl --location --request PUT 'http://127.0.0.1:8080/account/4/reset_password' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE2NjI1OTk3MjMsInN1YiI6ImFjY2VzcyJ9.XazpV3L98Ep6DBwntXXVRSIo-RsnxRXCtJnE7I-mRaE' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'password=12345678'
```

```
{"code": 0, "msg": "", "data": "重置密码成功"}```
```

## 修改用户信息

```
curl --location --request PATCH 'http://127.0.0.1:8080/account/5' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE2NjI1OTk3MjMsInN1YiI6ImFjY2VzcyJ9.XazpV3L98Ep6DBwntXXVRSIo-RsnxRXCtJnE7I-mRaE' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'username=jack0' \
--data-urlencode 'password=123456' \
--data-urlencode 'password_again=123456'
```

```
{"code": 0, "msg": "", "data": "更新成功"}
```

## 管理员批量删除用户

```
curl --location --request DELETE 'http://127.0.0.1:8080/account/delete_user' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE2NjI1OTk3MjMsInN1YiI6ImFjY2VzcyJ9.XazpV3L98Ep6DBwntXXVRSIo-RsnxRXCtJnE7I-mRaE' \
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
curl --location --request GET 'http://127.0.0.1:9001/account/?page=1&size=5' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE2NjI1OTk3MjMsInN1YiI6ImFjY2VzcyJ9.XazpV3L98Ep6DBwntXXVRSIo-RsnxRXCtJnE7I-mRaE' \
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
                ],
                "used_disk": ""
            },
            {
                "id": 3,
                "username": "jack",
                "email": "2514553187@qq.com",
                "is_active": true,
                "role": [
                    "admin"
                ],
                "used_disk": "8M"
            },
            {
                "id": 4,
                "username": "汤姆克鲁斯",
                "email": "0@qq.com",
                "is_active": false,
                "role": [
                    "normal"
                ],
                "used_disk": "8G"
            },
            {
                "id": 5,
                "username": "勒布朗詹姆斯",
                "email": "1@qq.com",
                "is_active": true,
                "role": [],
                "used_disk": "8G"
            },
            {
                "id": 6,
                "username": "爱因斯坦",
                "email": "2@qq.com",
                "is_active": true,
                "role": [],
                "used_disk": "8G"
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
curl --location --request POST 'http://127.0.0.1:8080/account/manager' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE2NjI1OTk3MjMsInN1YiI6ImFjY2VzcyJ9.XazpV3L98Ep6DBwntXXVRSIo-RsnxRXCtJnE7I-mRaE' \
--header 'Content-Type: application/json' \
--data-raw '{"userid": 5, "is_active": false}'
```

```
{"code": 0, "msg": "", "data": true}
```

# 系统样式图标设置

## 查看系统设置的title和image
```
curl --location --request GET 'http://127.0.0.1:8080/site_config' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE2NjI1OTk3MjMsInN1YiI6ImFjY2VzcyJ9.XazpV3L98Ep6DBwntXXVRSIo-RsnxRXCtJnE7I-mRaE' \
--header 'Content-Type: application/json'
```

```buildoutcfg
[{"id":1,"title":"test","image":"data:image/jpeg;base64,/9sss","create_time":"2022-08-14T14:57:47.552747","update_time":"2022-08-14T14:57:47.553068"}]
```

## 创建
```
curl --location --request POST 'http://127.0.0.1:8080/site_config' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE2NjI1OTk3MjMsInN1YiI6ImFjY2VzcyJ9.XazpV3L98Ep6DBwntXXVRSIo-RsnxRXCtJnE7I-mRaE' \
--header 'Content-Type: application/json' \
--data-raw '{"title": "test", "image": "data:image/jpeg;base64,/9sss"}'
```

```
{"id":1,"title":"test","image":"data:image/jpeg;base64,/9sss","create_time":"2022-08-14T14:57:47.552747","update_time":"2022-08-14T14:57:47.553068"}
```

## 修改

```
curl --location --request PUT 'http://127.0.0.1:8080/site_config/1' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE2NjI1OTk3MjMsInN1YiI6ImFjY2VzcyJ9.XazpV3L98Ep6DBwntXXVRSIo-RsnxRXCtJnE7I-mRaE' \
--header 'Content-Type: application/json' \
--data-raw '{"title": "test", "image": "data:image/jpeg;base64,/9sss"}'
```

```
{"id":1,"title":"test","image":"data:image/jpeg;base64,/9sss","create_time":"2022-08-14T14:57:47.552747","update_time":"2022-08-14T14:57:47.553068"}
```

# 角色

## 查看系统已有角色

```
curl --location --request GET 'http://127.0.0.1:8080/role' \
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
curl --location --request POST 'http://127.0.0.1:8080/project' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE2NjM5MzUwNzksInN1YiI6ImFjY2VzcyJ9.v2cLd31Tnd20t1ILTsFtCv0z3-xuVUbFX8_KxoHBCTY' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "jack",
    "desc": "xxx"
}'
```

```buildoutcfg
curl --location --request POST 'http://127.0.0.1:8080/project' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE2NjM5MzUwNzksInN1YiI6ImFjY2VzcyJ9.v2cLd31Tnd20t1ILTsFtCv0z3-xuVUbFX8_KxoHBCTY' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "jack1",
    "desc": "xxx",
    "parent": 1
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
curl --location --request GET 'http://127.0.0.1:8080/project?parent_id=1&page=1&size=2' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE2NjM5MzUwNzksInN1YiI6ImFjY2VzcyJ9.v2cLd31Tnd20t1ILTsFtCv0z3-xuVUbFX8_KxoHBCTY' \
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

# 患者管理

## 创建患者

```buildoutcfg
curl --location --request POST 'http://127.0.0.1:8080/patient/patients' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE2NjMwNjQxOTcsInN1YiI6ImFjY2VzcyJ9.F_GfkaaIEk-QZhyf9UjEH2sruKCzdWCSlSGLXHBE6qs' \
--header 'Content-Type: application/json' \
--data-raw '{
    "age": 23,
    "birthday": "2022-08-05",
    "name": "张三",
    "id_card": "3402111999111106501",
    "medical_doctor": "李四",
    "gender": "male",
    "location": "location",
    "identifier": "7983f7a0-d824-49da-807c-217a6d1d1473",
    "inspection_agency": "xxx",
    "tumor_stage": "tumor_stage",
    "diagnosis": "diagnosis",
    "disease": "disease",
    "family_history": "family_history",
    "medication_history": "medication_history",
    "treatment_history": "treatment_history",
    "prognosis_time": "2022-08-05 12:00:00",
    "recurrence_time": "2022-08-05 12:00:00",
    "survival_time": "2022-08-05 12:00:00"
}'
```

```buildoutcfg
{
    "id": 1,
    "age": 23,
    "birthday": "2022-08-05",
    "name": "张三",
    "id_card": "3402111999111106501",
    "medical_doctor": "李四",
    "gender": "male",
    "location": "location",
    "identifier": "7983f7a0-d824-49da-807c-217a6d1d1473",
    "inspection_agency": "xxx",
    "tumor_stage": "tumor_stage",
    "diagnosis": "diagnosis",
    "disease": "disease",
    "family_history": "family_history",
    "medication_history": "medication_history",
    "treatment_history": "treatment_history",
    "prognosis_time": "2022-08-05T12:00:00",
    "recurrence_time": "2022-08-05T12:00:00",
    "survival_time": "2022-08-05T12:00:00",
    "create_time": "2022-08-19T21:33:57.895420",
    "update_time": "2022-08-19T21:33:57.895842",
    "creator": 2
}
```

## 查询患者

```buildoutcfg
curl --location --request GET 'http://127.0.0.1:8080/patient/patients' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE2NjMwNjQxOTcsInN1YiI6ImFjY2VzcyJ9.F_GfkaaIEk-QZhyf9UjEH2sruKCzdWCSlSGLXHBE6qs' \
--header 'Content-Type: application/json'
```

```buildoutcfg
{"code": 0, "msg": "", "data": {"count": 1, "next": null, "previous": null, "results": [{"id": 1, "age": 23, "birthday":
"2022-08-05", "name": "张三", "id_card": "3402111999111106501", "medical_doctor": "李四", "gender": "male", "location":
"location", "identifier": "7983f7a0-d824-49da-807c-217a6d1d1473", "inspection_agency": "xxx", "tumor_stage":
"tumor_stage", "diagnosis": "diagnosis", "disease": "disease", "family_history": "family_history", "medication_history":
"medication_history", "treatment_history": "treatment_history", "prognosis_time": "2022-08-05T12:00:00",
"recurrence_time": "2022-08-05T12:00:00", "survival_time": "2022-08-05T12:00:00", "create_time":
"2022-08-19T21:33:57.895420", "update_time": "2022-08-19T21:33:57.895842", "creator": 2}]}}
```

## 删除患者

```buildoutcfg
curl --location --request DELETE 'http://127.0.0.1:8080/patient/patients/1' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE2NjMwNjQxOTcsInN1YiI6ImFjY2VzcyJ9.F_GfkaaIEk-QZhyf9UjEH2sruKCzdWCSlSGLXHBE6qs' \
--header 'Content-Type: application/json' 
```

## 修改患者

```buildoutcfg
curl --location --request PATCH 'http://127.0.0.1:8080/patient/patients/2' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE2NjMwNjQxOTcsInN1YiI6ImFjY2VzcyJ9.F_GfkaaIEk-QZhyf9UjEH2sruKCzdWCSlSGLXHBE6qs' \
--header 'Content-Type: application/json' \
--data-raw '{
    "age": 23,
    "birthday": "2022-08-05",
    "name": "张三",
    "id_card": "3402111999111106501",
    "medical_doctor": "李四",
    "gender": "male",
    "location": "location",
    "identifier": "7983f7a0-d824-49da-807c-217a6d1d1473",
    "inspection_agency": "xxx",
    "tumor_stage": "tumor_stage",
    "diagnosis": "diagnosis",
    "disease": "disease",
    "family_history": "family_history",
    "medication_history": "medication_history",
    "treatment_history": "treatment_history",
    "prognosis_time": "2022-08-05 12:00:00",
    "recurrence_time": "2022-08-05 12:00:00",
    "survival_time": "2022-08-05 12:00:00"
}'
```

```buildoutcfg
{
    "id": 2,
    "age": 23,
    "birthday": "2022-08-05",
    "name": "张三",
    "id_card": "3402111999111106501",
    "medical_doctor": "李四",
    "gender": "male",
    "location": "location",
    "identifier": "7983f7a0-d824-49da-807c-217a6d1d1473",
    "inspection_agency": "xxx",
    "tumor_stage": "tumor_stage",
    "diagnosis": "diagnosis",
    "disease": "disease",
    "family_history": "family_history",
    "medication_history": "medication_history",
    "treatment_history": "treatment_history",
    "prognosis_time": "2022-08-05T12:00:00",
    "recurrence_time": "2022-08-05T12:00:00",
    "survival_time": "2022-08-05T12:00:00",
    "create_time": "2022-08-19T21:48:38.945847",
    "update_time": "2022-08-19T21:49:01.864583",
    "creator": 2
}
```

## 下载模板

```buildoutcfg
curl --location --request GET 'http://127.0.0.1:8080/patient/patients/dl_patient_template' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE2NjMwNjQxOTcsInN1YiI6ImFjY2VzcyJ9.F_GfkaaIEk-QZhyf9UjEH2sruKCzdWCSlSGLXHBE6qs' \
--header 'Content-Type: application/json' 
```

## 上传csv文件

```buildoutcfg
curl --location --request POST 'http://127.0.0.1:8080/patient/patients/import_patients' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE2NjMwNjQxOTcsInN1YiI6ImFjY2VzcyJ9.F_GfkaaIEk-QZhyf9UjEH2sruKCzdWCSlSGLXHBE6qs' \
--form 'file=@"/Users/guwanhua/Documents/patient_template.csv"'
```

# 资源

## 管理员设置用户可以使用的磁盘大小, 单位MB

```buildoutcfg
curl --location --request POST 'http://127.0.0.1:9001/resource_limit/resource_limits' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE2NjMwNjQxOTcsInN1YiI6ImFjY2VzcyJ9.F_GfkaaIEk-QZhyf9UjEH2sruKCzdWCSlSGLXHBE6qs' \
--header 'Content-Type: application/json' \
--data-raw '{
    "user": 1,
    "limit_type": "disk",
    "limit": 34
}'
```

## 查询设置情况

```buildoutcfg
curl --location --request GET 'http://127.0.0.1:9001/resource_limit/resource_limits' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE2NjMwNjQxOTcsInN1YiI6ImFjY2VzcyJ9.F_GfkaaIEk-QZhyf9UjEH2sruKCzdWCSlSGLXHBE6qs' \
--header 'Content-Type: application/json'
```

```buildoutcfg
{"code": 0, "msg": "", "data": {"count": 1, "next": null, "previous": null, "results": [{"id": 1, "limit": 34, "limit_type": "disk", "desc": "", "create_time": "2022-09-02T17:48:36.289476", "update_time": "2022-09-02T17:48:36.289876", "user": 1, "creator": 2}]}}
```

## 查询系统内存和磁盘使用情况 单位MB

```buildoutcfg
curl --location --request GET 'http://127.0.0.1:9001/resource_limit/resource_limits/resource' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE2NjMwNjQxOTcsInN1YiI6ImFjY2VzcyJ9.F_GfkaaIEk-QZhyf9UjEH2sruKCzdWCSlSGLXHBE6qs' \
--header 'Content-Type: application/json'
```

```buildoutcfg
{"code": 0, "msg": "", "data": {"memory": {"all": 16384, "used": 8417}, "disk": {"all": 476802, "used": 399280}}}
```