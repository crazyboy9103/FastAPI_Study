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

<!-- ## ---
* anaconda 설치 후, ```environment.yaml``` 파일 맨 마지막 줄을 본인의 경로로 변경 
    ```
    prefix: 설치된 경로\envs\fastapi 
    ```
* ```conda env create -f environment.yaml``` : 콘다 가상환경 설치 
* ```conda activate fastapi``` : 콘다 가상환경 실행
* ```uvicorn main:app --reload``` : 서버 실행 -->

## Poetry 가상환경
* https://www.python.org/downloads/release/python-3112/ 에서 파이썬 설치
* https://python-poetry.org/docs/#installing-with-the-official-installer 에서 poetry 설치
  * 시스템 환경 변수 PATH에 추가해야함
    * Mac: ~/Library/Application Support/pypoetry/venv/bin/poetry
    * Linux/Unix: ~/.local/share/pypoetry/venv/bin/poetry
    * Windows: %APPDATA%\pypoetry\venv\Scripts\poetry
    * 만약 $POETRY_HOME이 존재하면 $POETRY_HOME/venv/bin/poetry

<br>

* ```poetry self update```: poetry 최신 버전 받아오기
* ```poetry self update 1.2.0```: 특정 버전 1.2.0 을 가져오기
* ```poetry new poetry-demo```: 다음과 같은 폴더 구조를 만들고, ```pyproject.toml``` 이라는 의존성 리스트를 작성해줌 
    ```
    poetry-demo
    ├── pyproject.toml
    ├── README.md
    ├── poetry_demo
    │   └── __init__.py
    └── tests
        └── __init__.py
    ```
* ```poetry init```: 이미 존재하는 프로젝트에 poetry를 시작
* ```poetry add PACKAGE```: 런타임에서 새로운 의존성을 추가하고 ```pyproject.toml``` 업데이트  

## Poetry 가상환경으로 실행
1. ```poetry install```: ```pyproject.toml``` 에 적힌 라이브러리 모두 설치하고 ```poetry.lock``` 파일을 생성하는데, 이를 VCS에 올려서 버전 관리를 해야함
2. ```poetry shell```: Poetry가 activate돼있는 shell을 invoke
3. ```uvicorn main:app --reload```: 서버 실행