## CPT-BOT PROJECT ( 4/8 ~ 4/26 )
#### GPT-3.5-Turbo를 이용한 Python 교육 챗봇 제작
---
![image](https://github.com/glassesholder/chunjae_edu_chatbot_project/assets/150658909/dcfc0e4c-9102-4b39-8f37-f0e1b420980c)

---

Hello everyone!😀

We worked on a project to develop a coding-learning AI CHATBOT for Python beginners who are going through middle school education curriculum.

We are affiliated with chunjae-edutech bigdata team 6, consisting of team leader `LEE SHIN YOUNG` and team members `KIM MIN SUN`, `LEE HYO JUN`, and `HWANG WON JIN`.

We sincerely appreciate you taking the time to read the introduction of our CHATBOT.

As it is designed for Korean students, we kindly ask for your understanding that the following instructions will be provided in Korean.

Thank you and have a nice day!💕

---
### ✅ 요약 보고서
>
대형 언어 모델(LLM)인 GPT-3.5-turbo에 학생의 학습에 도움이 된다고 판단한 파이썬 관련 질의 응답 데이터셋을 학습시켰다. 그에 따라 파이썬 질문에 대해서 점진적인 질의 응답이 가능하도록 하는 코딩 튜터링 서비스 챗봇(이하 CPT봇)이 구현되기를 기대했다.

2015 개정 교육과정 정보과 성취 기준과 2022 개정 교육과정 정보과 편성 시수에 따르면 프로그래밍의 이해를 위한 교육비중이 늘어난 것을 확인할 수 있다. CPT봇은 학습자의 학습 만족도를 올리고 사고력 증진을 이루는 데 큰 기여를 할 수 있을 것으로 생각된다.

fine-tuning 을 위한 데이터 수집을 위해서는 중등 정보교과서 및 파이썬 기본서를 참고했다. 컴퓨팅 사고력 향상이라는 챗봇 개발 목표에 맞게 문답을 3번으로 나누어 첫 두번의 문답은 질문에서 요구하는 알고리즘 및 순서개념을 안내, 마지막 문답은 정답 Python code를 제공하는 형식으로 짜여진 데이터를 수집했다. 이렇게 수집된 데이터를 학습시키고 시스템 프롬프트를 작성하여 CPT봇을 개발했다. 

UI는 파이썬 웹 프레임 워크 streamlit을 이용하여 구성했다. 소개/회원가입/로그인/이용가이드/CPT봇 페이지로 구분하여 사용자의 사용에 어려움이 없도록 했다. 사용자는 CPT봇을 자유롭게 사용할 수 있으며, 기업은 DB에 쌓이는 사용자 정보, 사용자의 질의응답 내용 및 피드백을 바탕으로 더 나은 성능을 보이는 CPT봇을 지속적으로 업데이트 할 수 있다.

---
### ✅ GUIDE FOR DEVELOPER

🖐안녕하세요🖐
다음 서비스들을 설치해주세요.
>
1. VSCODE
2. PYTHON (3.10.0 으로 설치 부탁드립니다.)
환경변수에 추가하여 VSCODE에서 TERMINAL에서 사용할 수 있도록 해주세요.
4. GIT
5. POSTGRESQL (다른 DB로 대체 가능합니다. )
6. DBEAVER (다른 DBMS로 대체 가능합니다.)

폴더 내 .env 파일을 생성한 뒤 아래 내용을 적어주세요. <br>
OPEN_API_KEY="본인의 api key" <br>
POSTGRES_DB="db 이름 넣어주세요" <br>
POSTGRES_USER="postgres" <br>
POSTGRES_PASSWORD="본인이 설정한 pwd 넣어주세요" <br>
POSTGRES_HOST="localhost"

다음 단계를 거쳐주세요.


1. VSCODE를 열어서 터미널을 열어주세요.

2. ```$ git clone --single-branch --branch main https://github.com/glassesholder/chunjae_edu_chatbot_project.git```
를 터미널에 입력해서 내려받아 주세요.

3. (생략가능) 가상환경 설치
```$ python venv -m venv cpt```
로 가상환경을 설치해서 활성화 후 사용해주세요.

4. requirements.txt에 담겨있는 라이브러리를 설치해주세요.
```$ pip install -r requirements.txt```

5. vscode는 잠시 두고, pgadmin4에 들어가서 자신의 db를 만들어주세요.(해당 과정은 자신의 여건에 맞게 AWS 또는 NCP에서 진행해도 문제가 되지 않습니다.)

6. dbeaver에 들어가서 자신이 만들어놓은 db를 연결해주세요. 이제 쌓이는 데이터를 확인할 준비가 되었습니다.

7. 다시 vscode terminal로 돌아와서 db에 테이블을 만들기 위한 코드를 실행해주세요.
```$ python create_table.py```

8. 끝으로 터미널에서 챗봇 실행을 위한 cptbot_start.py 파일을 실행해주세요.
```$ streamlit run cptbot_start.py```

다음과 같은 과정을 거쳐서 챗봇 페이지 실행 및 쌓이는 데이터를 확인할 수 있습니다.😉

---
### ✅ RESULT

>
프로젝트의 목적에 맞게 1차적으로 힌트(알고리즘)를 제공하고, 이후 사용자가 힌트(알고리즘)를 요청하면 2차적으로 자세한 힌트(알고리즘)를 제공합니다. 마지막으로 사용자가 정답 코드를 요청하면 질문에 알맞는 python 코드를 제공하여 단계적으로 사용자의 학습을 유도하는 모습을 확인할 수 있습니다.

1. 소개 / 회원가입 / 로그인 화면

![image](https://github.com/glassesholder/chunjae_edu_chatbot_project/assets/150658909/aacb10db-7b5a-4c0f-947f-12f44dd53fc3)

2. 질의/응답 화면(1)

![image](https://github.com/glassesholder/chunjae_edu_chatbot_project/assets/150658909/45c146c8-bbc9-49b1-95f3-d77fbe3b3058)

3. 질의/응답 화면(2)

![image](https://github.com/glassesholder/chunjae_edu_chatbot_project/assets/150658909/7dc5229f-82a5-4e45-9c55-87c16a0e8ba7)

---
### ✅ GUIDE FOR BUSINESS MAN

완성된 CPT모델은 실제 비즈니스에서 다음과 같은 역할을 할 것이라고 기대합니다.

1. B2G : 교육부에서 주관하는 AIDT 내 서비스로 제공할 수 있습니다.

2. B2C : 학습자의 학습 만족도를 높여주는 챗봇은 에듀테크 분야에서 긍정적인 기업이미지를 창출할 수 있습니다.

3. B2B : 데이터베이스에 저장된 학습데이터를 타기업과 거래하거나 챗봇 서비스 자체를 거래할 수 있습니다.

4. 내부 효과 : 데이터베이스에서 자주 묻는 질문을 추출하여 프로그래밍 참고서에 반영할 수 있습니다.

---
### ✅ 마무리

CPT봇의 한계점에 기반한 우리 팀의 추가 개발 방향은 다음과 같습니다.

1. CPT는 기준에 부합하는 40개의 데이터세트를 학습시켰습니다😂 답변의 정확도를 고려하였을 때 적은 수로 판단되기 때문에 이후 추가 데이터셋을 확보하여 모델을 학습시키고자 합니다.

2. 기기(노트북,휴대폰,태블릿,모니터 등) 특성에 맞게 코드를 수정하여 디자인을 수정 보완하고자 합니다.
  
4. CPT봇 사용에 있어서 세션이 종료되면 다시 로그인을 해야 하는 불편함이 있습니다. 사용자의 편의를 고려하여 쿠키를 이용한 아이디와 비밀번호 기억을 통해 자동 로그인이 되도록 구현하고자 합니다.

5. CPT봇 내 “자주 묻는 질문” 항목을 생성하고 개인별 오답노트를 제작하는 등 사용자 개인별 맞춤 서비스를 제공하고자 합니다.

---

#### 우리 팀의 프로젝트에 관심을 가져주셔서 진심으로 감사합니다🎶
