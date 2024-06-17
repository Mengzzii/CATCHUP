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

## 프로젝트 구조 및 소스 코드 설명
### 프로젝트 구조
```
├── **README.md**<br>
├── **backend**<br>
│      ├── src<br>
│      │     ├── config<br>
│      │     │     └── openai.config.py<br>
│      │     │<br>
│      │     ├── controller<br>
│      │     │        ├── auth_controllers.py<br>
│      │     │        ├── chat_controllers.py<br>
│      │     │        ├── concept_controller.py<br>
│      │     │        ├── langchain_controllers.py<br>
│      │     │        └── user_controllers.py<br>
│      │     │<br>
│      │     ├── db<br>
│      │     │    ├── chromadb_connection.py<br>
│      │     │    ├── connection.py<br>
│      │     │    └── vector_connection.py<br>
│      │     │<br>
│      │     └── models<br>
│      │           └── user.py<br>
│      │<br>        
│      ├── .gitignore<br>
│      ├── Pipfile<br>
│      ├── Pipfile.lock<br>
│      ├── requirements.txt<br>
│      └── main.py<br>
│<br>            
├── **frontend**<br>
│       ├── src<br>
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

### 소스 코드 설명
