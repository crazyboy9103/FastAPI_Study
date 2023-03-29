# FastAPI 실행 
```backend``` 폴더 내에 ```config.yaml``` 파일을 생성
```
{
    'connections': {
        # Dict format for connection
        'default': {
            'engine': 'tortoise.backends.asyncmy',
            'credentials': {
                'host': '호스트 주소',
                'port': '3306',
                'user': '호스트 계정',
                'password': '비밀번호',
                'database': 'DB명',
            }
        },
        # Using a DB_URL string
        'default': 'mysql://user:password@host:port/database' # credentials의 각 value와 동일하게 변경
    },
    'apps': {
        'models': {
            'models': ['models', 'aerich.models'],
            # If no default_connection specified, defaults to 'default'
            'default_connection': 'default',
        }
    }
}
```

## Poetry 가상환경 설정
> - [파이썬 설치](https://www.python.org/downloads/release/python-3112/) 
> - [Poetry 설치](https://python-poetry.org/docs/#installing-with-the-official-installer)
> - 설치후 PATH에 추가해야함
<br><br>

poetry 최신 버전 받아오기
```
poetry self update
``` 

특정 버전 1.2.0 으로 변경
```
poetry self update 1.2.0
```
  
아래 폴더 구조를 가지는 프로젝트를 만들고, ```pyproject.toml``` 이라는 의존성 파일을 생성
```    
poetry new poetry-demo => poetry-demo
                                ├── pyproject.toml # 의존성 파일
                                ├── README.md
                                ├── poetry_demo
                                │   └── __init__.py
                                └── tests
                                    └── __init__.py
```

이미 존재하는 프로젝트에 poetry를 시작
```
poetry init
```

런타임에서 새로운 의존성을 추가하고 ```pyproject.toml``` 업데이트  
```
poetry add PACKAGE
```

## Poetry 가상환경으로 실행
```pyproject.toml``` 에 적힌 라이브러리 모두 설치 및 ```poetry.lock``` 파일을 생성
> ```poetry.lock``` 파일을 VCS에 올려서 버전 관리
```
poetry install
```

Poetry의 가상환경 실행 - 터미널에서 바로 접근가능
```
poetry shell
```

서버 실행
```
uvicorn main:app --reload
```

## ```aerich```
> - 가상환경에서는 ```aerich```라는 패키지로 마이그래이션
> - ```database.py``` 파일에서 ```config.yaml``` 파일을 읽고 ```TORTOISE_ORM```이라는 변수에 저장하는데, ```aerich```에서 이 변수명으로 접근
>    - 이를 위해서 ```config.yaml```에 ```'aerich.models'```을 추가

인자로 주어진 값들을 ```pyproject.toml```에 저장하고 ```./migrations```에 마이그래이션용 폴더를 생성
```
aerich init -t database.TORTOISE_ORM --location ./migrations
``` 

모델에 대한 스키마를 작성, ```./migrations/models```에 migrate 경로를 생성
```
aerich init-db
```

모델을 업데이트하면 마이그래이션
> ```./migrations/models```에 ```1_202029051520102929_drop_column.json```이 생기는데, {버전번호}\_{시간}\_{name} 형태임
```
aerich migrate --name drop_column
```

   
최신 버전으로 업그레이드
```
aerich upgrade
```

특정 버전으로 다운그레이드
```
aerich downgrade -v {버전번호}
```

히스토리
```
aerich history
```

헤드 (마이그레이션 해야하는 버전)
```
aerich heads
```

모든 테이블 콘솔에 프린트
```
aerich --app models inspectdb
```

특정 테이블 모델로 만들기
> ```Pydantic```을 사용하기 때문에 ```./models``` 폴더 내 예제처럼 ```pydantic_model_creator``` 로 ```Pydantic``` 인스턴스를 추가해야함 
```
# 터미널에서 
aerich inspectdb -t {테이블명} > {원하는모델명}.py

# e.g. models.models.User: pydantic_model_creator 
from tortoise.contrib.pydantic import pydantic_model_creator
User_Pydantic = pydantic_model_creator(User, name="User", exclude_readonly=True)
```
