from tortoise import fields
from tortoise.models import Model
class User(Model):
    user_id = fields.IntField(pk=True, generated=True, unique=True, index=True, description="유저 아이디")
    name = fields.CharField(max_length=255, null=True, description="이름")
    email = fields.CharField(max_length=255, null=True, description="이메일")
    password = fields.CharField(max_length=255, null=True, description="비밀번호")
    def __str__(self):
        return self.name
    class Meta:
        table = "users"
        table_description = "유저 테이블"
        
# class tortoise.fields.base.Field(
#   source_field=None, # DB상 필드와 Model상 필드가 다를 경우 DB상 field명
#   generated=False, # DB가 관리하는 자동 생성된 필드일 경우 True
#   pk=False, # PK 
#   null=False, # Nullable
#   default=None, # default 값
#   unique=False, # unique 여부
#   index=False, # index 해놓을지 여부
#   description=None, # 코멘트
#   model=None, # fields.ForeignKeyField('models.User', related_name='blogs') 와 같은 외래키의 경우 model에 해당 model의 경로,
#               # user = await User.get(id=1)
#               # blogs = await user.blogs.all() # related_name으로 가져올 수 있음
#   validators=None, # func = lambda val: True|False 여러개를 list에 묶어서 넣으면 됨 
# **kwargs) 
# 
# CharField (
#   max_length,
#   **kwargs
# )
#
# Hardly used enums 
# CharEnumField (
#   enum_type: Enum class, 
#   max_length=0,
#   **kwargs
# )  
# IntEnumField (
#   enum_type: Enum class, 
#   **kwargs
# )  
#
# TextField (
#   pk=False, 
#   unique=False, 
#   index=False,
#   **kwargs
# )
# DateField (
# )
# DatetimeField (
#   다음 두 필드는 둘 중 하나만 입력하던지 아예 입력하지 말아야함  
#   auto_now=False, # always set to datetime.utcnow() on save
#   auto_now_add=False, # set to datetime.utcnow() on first save only 
# )
# 정확한 소수를 표현하는 필드 : .을 기준으로 왼쪽 숫자들의 개수 max_digits와 오른쪽 숫자들의 개수 decimal_places
# DecimalField (
#   max_digits, # 정수값의 최대 자리수
#   decimal_places, # 소수값의 최대 자리수 
# )
# decimal 라이브러리를 사용해서 빠르고 정확한 계산을 할 수 있음

# FloatField ( 
#   pk = False
# )

# SmallIntField ( 
#   pk = False
# )

from tortoise.contrib.pydantic import pydantic_model_creator
User_Pydantic = pydantic_model_creator(User, name="User", exclude_readonly=True)