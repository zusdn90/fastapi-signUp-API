# fastapi-signUp-API
회원가입, 비밀번호 재설정 API

### 프로젝트 폴더 구조

``` 
├── backend              : FastAPI 프로젝트 root
│   └── app    
│   |    ├── api         : REST API 
│   |    ├── database    : db base class 정의
│   |    ├── middlewares : 미들웨어 정의
│   |    ├── core        : config, event_handler,util 등등...
│   |    ├── models      : DB 모델
│   |    └── schemas     : pydantic 모델
│   |    └── tests       : test 코드
|   ├── main.py          : FastAPI main모듈
│   └── migrations       : db migration 파일
│   └── scripts          : shell 파일
```

### 로컬 서버 구동 / DB 테이블 새성
```
1. docker-compose build && docker-compose up
```
```
2. cd backend/app/scripts ./migratinos.sh
```