# 用户

## 登录

```
curl --location --request POST 'http://127.0.0.1:8000/account/?action=login' \
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
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2MDI1NTcxNjEsInN1YiI6ImFjY2VzcyJ9.DaypwFZE8ME53ub-wfDXjMsEE109GL5oYzaQmuNhQ6o' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "jack",
    "desc": "xxx"
}
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
		"item_list": [{
			"id": 13,
			"name": "jack",
			"desc": "这是我的",
			"owner": "jack",
			"owner_id": "3",
			"members": [{
				"id": 3,
				"username": "jack",
				"email": "2514553187@qq.com"
			}],
			"create_time": "2020-10-13T15:49:15.812514"
		}, {
			"id": 12,
			"name": "jack",
			"desc": "这是我的",
			"owner": "jack",
			"owner_id": "3",
			"members": [{
				"id": 3,
				"username": "jack",
				"email": "2514553187@qq.com"
			}],
			"create_time": "2020-10-13T15:47:46.198580"
		}],
		"total_count": 5
	}
}
```





## 查看单个项目

```
curl --location --request GET 'http://127.0.0.1:8000/project/9' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE2MDI1NzY2MzEsInN1YiI6ImFjY2VzcyJ9.q8I5DR3YYYeU2YUIkB4P5sa-wVNEbiPtnLMxyvkIHqM' \
--header 'Content-Type: application/json'
```

```
{
	"id": 9,
	"name": "jack",
	"desc": "",
	"owner": "jack",
	"owner_id": "3",
	"members": [{
		"id": 1,
		"username": "wangxiaochuan01@163.com",
		"email": "wangxiaochuan01@163.com"
	}, {
		"id": 3,
		"username": "jack",
		"email": "2514553187@qq.com"
	}],
	"create_time": "2020-10-13T15:24:52.340492"
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
curl --location --request DELETE 'http://127.0.0.1:8000/project/2' \
--header 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2MDI0OTkyMDAsInN1YiI6ImFjY2VzcyJ9.HbXb7ZBsoDYQptH8h3rJaGbwCkuHTQDyub52_v7m5VM' \
--header 'Content-Type: application/json'
```

```
{"code": 0, "msg": "", "data": true}
```

```
{"code": 1, "msg": "非项目创建者不能删除项目", "data": false}
```



