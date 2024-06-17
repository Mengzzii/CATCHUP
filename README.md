## 컴퓨터공학과 학생에게 선수 학습 사항 자료를 제공해 주는 LLM 챗봇 웹서비스
<img src=https://github.com/Mengzzii/CATCHUP/assets/151775207/670f56a1-066c-4d40-b9ad-a71dd5573427 width=500 height=120/>

<br><br>
## 팀원 소개
|유영민|강민아|임은지|
|:---:|:---:|:---:|
|<img src=https://github.com/Mengzzii/CATCHUP/assets/151775207/13a3823a-f116-4928-9532-e242993cfbc5 width=300 height=300/>|<img src=https://github.com/Mengzzii/CATCHUP/assets/151775207/9f13db75-7d6e-46ea-b9bd-33074a17c295 width=300 height=300/>|<img src=https://github.com/Mengzzii/CATCHUP/assets/151775207/da8bf217-beec-4435-964a-aa8ceaf45d65 width=300 height=300/>|
|팀장, 백엔드, 서버|팀원, 백엔드, 프론트엔드|팀원, 백엔드, RAG|
|@|@|@|

<br><br>
## 개발 환경
- Frontend: React, HTML, CSS, JAVASCRIPT
- Backend: FastAPI
- Database: MongoDB, ChromaDB
- 버전 및 이슈 관리: Github
- 협업 툴: Discord, Notion, Slack
- 서비스 배포 환경: AWS EC2, DOCKER
- 디자인: Figma
<br><br>

## 프로젝트 개요
***CATCHUP*** 프로젝트는 컴퓨터공학과 학생들이 방학 동안 선수학습 사항을 충족하여 학기 중 전공과목을 성공적으로 이수하도록 돕는 것을 목표로 합니다. 최소한의 공부 범위를 선별해 주고, 개념별 학습자료를 제공하며, 질문을 받아주는 LLM 챗봇 웹서비스를 기획하게 되었습니다.
<br><br>

## 프로젝트 구조 및 소스 코드
### 프로젝트 구조
```
├── **README.md**
├── **backend**
│      ├── src
│      │     ├── config
│      │     │     └── openai.config.py
│      │     │<br>
│      │     ├── controller<br>
│      │     │        ├── auth_controllers.py
│      │     │        ├── chat_controllers.py
│      │     │        ├── concept_controller.py
│      │     │        ├── langchain_controllers.py
│      │     │        └── user_controllers.py
│      │     │
│      │     ├── db
│      │     │    ├── chromadb_connection.py
│      │     │    ├── connection.py
│      │     │    └── vector_connection.py
│      │     │
│      │     └── models
│      │           └── user.py
│      │       
│      ├── .gitignore
│      ├── Pipfile
│      ├── Pipfile.lock
│      ├── requirements.txt
│      └── main.py
│           
├── **frontend**
│       ├── src
│       │        ├── Icons
│       │        │      ├── Editicon.jsx
│       │        │      ├── Loading.jsx
│       │        │      ├── Pencilcon.jsx
│       │        │      .
│       │        │      .
│       │        │      .
│       │        │      └── UserIcon.jsx
│       │        ├── components
│       │        │        ├── BuChatItem.jsx
│       │        │        ├── BuConceptItem.jsx
│       │        │        ├── ChatItem.jsx
│       │        │        ├── ConceptItem.jsx
│       │        │        ├── Form.jsx
│       │        │        ├── HomeLogo2.jsx
│       │        │        ├── Logo.jsx
│       │        │        ├── Main1_left.jsx
│       │        │        ├── Main1_r_login.jsx
│       │        │        ├── Main1_r_signup.jsx
│       │        │        ├── Main1_right.jsx
│       │        │        ├── Main2_class.jsx
│       │        │        ├── Main2_new.jsx
│       │        │        ├── Main2_top.jsx
│       │        │        ├── NormalButton.jsx
│       │        │        ├── StartBasic.jsx
│       │        │        ├── StartStudy.jsx
│       │        │        └── SubmitButton.jsx
│       │        │
│       │        ├── css
│       │        │    ├── Chat.module.css
│       │        │    ├── ChatExtra.module.css
│       │        │    ├── Form.module.css
│       │        │    ├── Loading.module.css
│       │        │    ├── Login.module.css
│       │        │    ├── Logo.module.css
│       │        │    ├── Main1.module.css
│       │        │    ├── Main2.module.css
│       │        │    ├── NormalButton.module.css
│       │        │    ├── SignUp.module.css
│       │        │    └── SubmitButton.module.css
│       │        │
│       │        ├── hooks
│       │        │     └── useChekcLogin.jsx
│       │        │
│       │        ├── pages
│       │        │      ├── Classroomchat.jsx
│       │        │      ├── Login.jsx
│       │        │      ├── Main1.jsx
│       │        │      ├── Main2.jsx
│       │        │      ├── Newclassroomchat.jsx
│       │        │      ├── Signup.jsx
│       │        │      ├── buClassroomchat.jsx
│       │        │      └── buNewclassroomchat.jsx
│       │        │
│       │        ├── App.jsx
│       │        └── main.jsx
│       │
│       ├── .eslintrc.cjs
│       ├──.gitignore
│       ├── favicon.ico
│       ├── homeLogo.png
│       ├── package-lock.json
│       ├── package.json
│       ├── vite.config.js
│       └── index.html
│
├── Pipfile
└── Pipfile.lock
```

### 소스 코드 한 눈에 보기
#### [Backend]
1. controller: 각종 백엔드 함수와 관련된 소스 코드
	- auth_controllers.py: 사용자 인증 처리와 관련 코드
	- chat_controller.py: 과목과 개념별 채팅 기록 관리 및 개념 리스트 제공 관련 코드
	- concept_controller.py: 학습 자료 제공 및 사용자 질문에 대한 답변 관련 코드
	- langchain_controllers.py: Langchain 및 OpenAI API를 활용한 개념 리스트 반환, 학습 자료 생성, Q&A 응답 처리 관련 코드
	- user_controllers.py: 사용자 관리 관련 코드 (사용자 인증, 회원가입, 로그인, 강의실 생성 및 수정, 강의실 목록 조회, 강의실 삭제, 개념 챗방 삭제)

2. db: 데이터베이스 연결 및 데이터베이스와 관련된 소스 코드
	- chromadb_connection.py: 벡터 데이터 베이스 임베딩 및 문서 검색 관련 코드
	- connection.py: mongodb 연결 코드
	- vector_connection.py: chromadb 및 OpenAI 연결 코드

3. models: 데이터베이스에서 사용될 데이터 구조와 관련된 소스 코드
   	- user.py: FastAPI를 사용해 데이터 모델을 정의

4. main.py: FastAPI를 사용해 구축된 API 서버의 엔드 포인트들을 정의
<br><br>
#### [Frontend]
1. Icons: 프론트에서 사용된 아이콘들 관련 코드

2. components: 페이지에서 사용될 각 컴포넌트 관련 코드

3. css: 컴포넌트의 css를 선언한 코드

4. hooks: React에서 사용자가 로그인 되어있는지 확인하는 코드 

5. pages: 컴포넌트들을 활용해 필요한 화면들을 생성한 코드

6. App.jsx: React의 라우팅을 관리하는 코드

7. Main.jsx: React를 초기화하고 랜더링하는 코드

8. index.html: React를 위해해 기본적인 구조를 정의하는 코드

