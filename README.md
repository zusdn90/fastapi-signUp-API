### 프로젝트 개요
- 회원가입, 로그인, 회원 정보조회, 비밀번호 재설정 API

### 프로젝트 폴더 구조

``` 
├── backend              : FastAPI 프로젝트 root
│   └── app    
│   |    ├── api         : REST API 
│   |    ├── database    : db base class 정의
│   |    ├── middlewares : 미들웨어 정의 (JWT 적용)
│   |    ├── core        : config, event_handler,util 등등...
│   |    ├── models      : DB 모델
│   |    └── schemas     : pydantic 모델
|   ├── main.py          : FastAPI main모듈
│   └── migrations       : db migration 파일
│   └── tests            : test 코드
│   └── scripts          : shell 파일
```

### 개발 환경
- Python 3.8
- FastAPI
- SQLAlchemy (ORM)
- Postgresql 12
- docker-compose
- IDE: vscoode

### 로컬 서버 구동 / DB 테이블 생성 / 테스트 코드 실행
```
1. docker-compose build && docker-compose up
```
```
2. docker exec -it server /bin/bash
```
```
3. cd scripts ./migratinos.sh (DB migration)
   유저, 인증 테이블 생성
```
```
4. cd scripts ./test.sh (유닛 테스트 실행)
```

## swagger url: http://localhost:8000/docs

### API 사용 가이드
```
1. 최초 회원가입을 하기 전 전화번호 인증을 한다.
   전화번호 인증은 실제 SMS문자 서비스를 연동하지 않고 간략하게 전화번호를 body 파라미터로 요청하면 6자리의 숫자를 리턴한다.
   
   url: v1/register/auth - POST
```
```
2. 전화번호 인증이 완료되면 회원가입을 진행한다. 
   회원가입 시 인증받은 번호(auth_number)를 파라미터로 같이 보낸다. (인증된 유저인지 확인)
   
   url: v1/register - POST
```
```
3. 회원가입이 완료되면 로그인을 할 수 있다.
   로그인은 전화번호, 이메일 둘다 가능하고 API 요청 시 로그인 타입(login_type)을 지정해서 요청해야 한다.
   
   url: v1/users/login/{login_type} - POST
```
```
4. 로그인이 완료되면 토큰이 리턴되는데 해당 토큰으로 유저 인증 API를 호출해서 유저 ID값을 받아온다. (유저ID로 정보조회)

   url: v1/users/ - POST header: Authorization JWT xxxxxxxxxxxxxxxxx
   
   해당 API는 swagger에서 테스트가 불가합니다. 토큰값을 리퀘스트 헤더에 넣어줘야해서 Postman이나 Insomnia에서 테스트 할 수 있습니다.
```
```
5. 유저 ID값을 받아오면 유져 정보 조회 API를 요청해서 정보를 확인한다.

   url: v1/users/{id} - GET header: Authorization JWT xxxxxxxxxxxxxxxxx
   
   해당 API는 swagger에서 테스트가 불가합니다. 토큰값을 리퀘스트 헤더에 넣어줘야해서 Postman이나 Insomnia에서 테스트 할 수 있습니다.
```
```
6. 유저가 비밀번호를 재설정 하고 싶은 경우 전화번호 인증 후 재설정 가능하다.

   url: v1/register/reset/pasaword - POST
```
