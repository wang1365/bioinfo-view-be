from django.db import models

from account.models import Account

# Create your models here.


class Role(models.Model):
    """
    角色表
    """
    code = models.CharField(max_length=32, verbose_name="角色名")
    permission2action = models.ManyToManyField(
        to='Permission2Action')

    def __str__(self):
        return self.code

    class Meta:
        db_table = "role"
        verbose_name_plural = "角色表"


class User2Role(models.Model):
    """
    用户角色表
    """
    user = models.ForeignKey(to=Account,
                             on_delete=models.CASCADE, related_name="user2role")
    role = models.ForeignKey(to="Role",
                             on_delete=models.CASCADE)

    def __str__(self):
        return f"user_id: {self.user.id}, role_id: {self.role.id}"

    class Meta:
        db_table = "user2role"
        verbose_name_plural = "用户角色表"


class Action(models.Model):
    """
    http 操作表
    """
    code = models.CharField(max_length=32)
    caption = models.CharField(max_length=32)

    def __str__(self):
        return self.code

    class Meta:
        db_table = "action"
        verbose_name_plural = "http动作表"


class Permission(models.Model):
    """
    url表
    """
    title = models.CharField(max_length=32, verbose_name="url标题")
    url = models.CharField(max_length=32, verbose_name="含正则的url")
    alias = models.CharField(max_length=32, verbose_name="url别名", null=True)

    def __str__(self):
        return self.url

    class Meta:
        db_table = "permission"
        verbose_name_plural = "url表"


class Permission2Action(models.Model):
    """
    真实的权限表
    """
    permission = models.ForeignKey(to=Permission,
                                   on_delete=models.CASCADE)
    parent = models.ForeignKey(to="self",
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)
    action = models.ForeignKey(to=Action,
                               on_delete=models.CASCADE)
    args = models.TextField(null=True, blank=True)
    kwargs = models.TextField(null=True, blank=True)
    customer_func = models.CharField(max_length=32,
                                     blank=True,
                                     null=True)

    def __str__(self):
        return f"{self.action.caption}: {self.permission.url}"

    class Meta:
        db_table = "permission2action"
        verbose_name_plural = "权限表"
