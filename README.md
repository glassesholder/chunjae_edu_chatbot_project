## CPT-BOT PROJECT
#### ChatGPT를 이용한 Python 교육 챗봇 제작

---

Hello everyone!😀

We worked on a project to develop a coding-learning AI CHATBOT for Python beginners who are going through middle school education curriculum.

We are affiliated with chunjae-edutech bigdata team 6, consisting of team leader `LEE SHIN YOUNG` and team members `KIM MIN SUN`, `LEE HYO JUN`, and `HWANG WON JIN`.

We sincerely appreciate you taking the time to read the introduction of our CHATBOT.

As it is designed for Korean students, we kindly ask for your understanding that the following instructions will be provided in Korean.

Thank you and have a nice day!💕

---
### ✅ 요약

대형 언어 모델(LLM)인 GPT3.5-turbo에 학생의 학습에 도움이 된다고 판단한 파이썬 관련 질의 응답 데이터셋을 학습시켰다. 그에 따라 파이썬 질문에 대해서 점진적인 질의 응답이 가능하도록 하는 코딩 튜터링 서비스 챗봇(이하 CPT봇)이 구현되기를 기대했다.

2015 개정 교육과정 정보과 성취 기준과 2022 개정 교육과정 정보과 편성 시수에 따르면 프로그래밍의 이해를 위한 교육비중이 늘어난 것을 확인할 수 있다. CPT봇은 학습자의 학습 만족도를 올리고 사고력 증진을 이루는 데 큰 기여를 할 수 있을 것으로 생각된다.

fine-tuning 을 위한 데이터 수집을 위해서는 중등 정보교과서 및 파이썬 기본서를 참고했다. 컴퓨팅 사고력 향상이라는 챗봇 개발 목표에 맞게 문답을 3번으로 나누어 첫 두번의 문답은 질문에서 요구하는 알고리즘 및 순서개념을 안내, 마지막 문답은 정답 Python code를 제공하는 형식으로 짜여진 데이터를 수집했다. 이렇게 수집된 데이터를 학습시키고 시스템 프롬프트를 작성하여 CPT봇을 개발했다. UI는 파이썬 웹 프레임 워크 streamlit을 이용하여 구성했다. 소개/회원가입/로그인/이용가이드/CPT봇 페이지로 구분하여 사용자의 사용에 어려움이 없도록 했다. 사용자는 CPT봇을 자유롭게 사용할 수 있으며, 기업은 DB에 쌓이는 사용자 정보, 사용자의 질의응답 내용 및 피드백을 바탕으로 더 나은 성능을 보이는 CPT봇을 지속적으로 업데이트 할 수 있다.
