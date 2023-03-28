from tortoise import fields
from tortoise.models import Model

class LoginLog(Model):
    login_log_id = fields.IntField(pk=True, generated=True, unique=True, index=True, description="로그인 로그 고유번호")
    # user_id 대신 user라고 적어야 자동으로 DB 생성시 user + _id 로 생성됨 (user_id로 적으면 user_id + _id 로 생성..)
    user = fields.ForeignKeyField('models.AuthUser', related_name="login_logs", description="유저 고유번호") 
    created_at = fields.DatetimeField(auto_now=True, description="날짜")
    
    class Meta:
        table = "login_log"
        table_description = "로그인 로그" 

    class PydanticMeta:
        exclude_raw_fields : bool = False # _id 숨길지 여부
        pass

from tortoise.contrib.pydantic import pydantic_model_creator
LoginLog_Pydantic = pydantic_model_creator(LoginLog, name="LoginLog")