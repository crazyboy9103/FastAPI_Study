# FastAPI 실행 

## 
* ```config.yaml``` 파일을 생성
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
                'models': ['models.models'],
                # If no default_connection specified, defaults to 'default'
                'default_connection': 'default',
            }
        }
    }
    ```

## 
* anaconda 설치 후, ```environment.yaml``` 파일 맨 마지막 줄을 본인의 경로로 변경 
    ```
    prefix: 설치된 경로\envs\fastapi 
    ```
* ```conda env create -f environment.yaml``` : 콘다 가상환경 설치 
* ```conda activate fastapi``` : 콘다 가상환경 실행
* ```uvicorn main:app --reload``` : 서버 실행