---
title: "This MCP makes Hermes Agent 10x more powerful - YouTube | LilysAI(릴리스AI) - 유튜브·PDF·웹 무료 요약 & 채팅"
source: "https://lilys.ai/digest/10119546/11775771"
author:
published:
created: 2026-06-16
description: "이 영상은 Hermes Agent 와 Apify 를 활용하여 웹 스크래핑 및 데이터 분석을 자동화하는 방법을 소개합니다. Hermes Agent 는 강력한 AI 에이전트로, Apify의 방대한 도구와 연동하여 웹사이트 접근 제한 문제를 해결하고 원하는 데이터를 수집할 수 있습니다. 특히, Apify의 MCB 커넥터 를 통해 수집된 데이터를 Superbase 와 같은 데이터베이스에 저장하고, Hermes Agent가 이를 분석하여 리드 자격 평가, 채용 후보자 분석 등 다양한 비즈니스 목표 달성에 활용하는 방법을 구체적으로 보여줍니다. 이 과정을 통해 채용 프로세스 자동화, 잠재 고객 발굴, 시장 조사 등 비즈니스 경쟁력을 강화할 수 있으며, 모든 과정을 자동화하여 시간과 비용을 절감하는 방법을 제시합니다. 이 영상은 AI 에이전트와 웹 스크래핑 기술을 결합하여 실질적인 비즈니스 가치를 창출하는 방법을 배우고 싶은 분들에게 유용합니다."
tags:
  - "clippings"
---
[1\. Hermes Agent와 Apify 연동을 통한 비즈니스 자동화](#54f7c80d-69ca-4bfe-99fd-800f80abd5c1)

[1.1. Hermes Agent 설치 및 기본 설정](#cceb711c-dceb-4a40-bab1-0002b28d59e7)

[1.2. Apify를 활용한 데이터 스크래핑 및 Superbase 연동](#aaee8446-8455-453c-a705-7590d2f09bf0)

[2\. Superbase 연동 및 Hermes Agent를 통한 리드 분석 자동화](#91b40891-5cdc-4c88-b5e3-5b07829680d5)

[2.1. Superbase 데이터베이스 설정 및 Apify 연동](#0fae6363-cb7d-4ec9-9c2e-321913d5fb85)

[2.2. Hermes Agent를 통한 리드 분석 및 자동화](#8e65939c-0a55-4612-afaa-4a4f2328c2e5)

Hermes Agent를 활용하여 비즈니스 프로세스를 자동화하는 방법은? Apify의 웹 스크래핑 기능과 Superbase 데이터베이스를 연동하여 **잠재 고객 발굴부터 채용 후보자 분석까지 모든 과정을** **자동화** 할 수 있습니다.

목차

[1\. Hermes Agent와 Apify 연동을 통한 비즈니스 자동화](#54f7c80d-69ca-4bfe-99fd-800f80abd5c1)

[1.1. Hermes Agent 설치 및 기본 설정](#cceb711c-dceb-4a40-bab1-0002b28d59e7)

[1.2. Apify를 활용한 데이터 스크래핑 및 Superbase 연동](#aaee8446-8455-453c-a705-7590d2f09bf0)

[2\. Superbase 연동 및 Hermes Agent를 통한 리드 분석 자동화](#91b40891-5cdc-4c88-b5e3-5b07829680d5)

[2.1. Superbase 데이터베이스 설정 및 Apify 연동](#0fae6363-cb7d-4ec9-9c2e-321913d5fb85)

[2.2. Hermes Agent를 통한 리드 분석 및 자동화](#8e65939c-0a55-4612-afaa-4a4f2328c2e5)

## 1\. Hermes Agent와 Apify 연동을 통한 비즈니스 자동화 \[1\]

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 800" style="width: 100%; height: auto;"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#d8d6d0"></polygon></marker></defs><rect x="0" y="0" width="1400" height="800" fill="#f4f3ef"></rect><text x="700" y="110" fill="currentColor">Hermes Agent &amp; Apify 비즈니스 자동화</text> <rect x="80" y="220" width="280" height="460" rx="12" fill="none" stroke="currentColor"></rect><text x="220" y="260" fill="currentColor">웹 데이터 소스</text> <g filter="url(#shadow)"><rect x="110" y="290" width="220" height="80" rx="12" fill="none" stroke="currentColor"></rect><text x="220" y="340" fill="currentColor">링크드인</text> <rect x="110" y="410" width="220" height="80" rx="12" fill="none" stroke="currentColor"></rect><text x="220" y="460" fill="currentColor">구글 맵스</text> <rect x="110" y="530" width="220" height="80" rx="12" fill="none" stroke="currentColor"></rect><text x="220" y="580" fill="currentColor">이커머스</text> </g><path d="M360 450 L420 450" fill="none" stroke="currentColor"></path><g filter="url(#shadow)"><rect x="430" y="370" width="240" height="160" rx="12" fill="none" stroke="currentColor"></rect><path d="M550 410 L570 430 L550 450 L530 430 Z" fill="#b5532a" opacity="0.2"></path><text x="550" y="465" fill="currentColor">Apify 엔진</text> <text x="550" y="500" fill="currentColor">데이터 추출</text> </g><path d="M670 450 L730 450" fill="none" stroke="currentColor"></path><g filter="url(#shadow)"><path d="M740 400 Q740 380 840 380 Q940 380 940 400 L940 500 Q940 520 840 520 Q740 520 740 500 Z" fill="none"></path><ellipse cx="840" cy="400" rx="100" ry="20" fill="none" stroke="currentColor"></ellipse><text x="840" y="465" fill="currentColor">Supabase</text> <text x="840" y="500" fill="currentColor">구조화된 저장소</text> </g><path d="M940 450 L1000 450" fill="none" stroke="currentColor"></path><g filter="url(#shadow)"><circle cx="1120" cy="450" r="100" fill="none" stroke="currentColor"></circle><text x="1120" y="445" fill="currentColor">Hermes AI</text> <text x="1120" y="480" style="fill: #e0e0e0;">지능형 분석</text> </g><path d="M1220 420 L1280 340" fill="none" stroke="currentColor"></path><path d="M1220 450 L1280 450" fill="none" stroke="currentColor"></path><path d="M1220 480 L1280 560" fill="none" stroke="currentColor"></path><text x="1250" y="300" style="text-anchor: start;" fill="currentColor">리드 발굴</text> <text x="1250" y="458" style="text-anchor: start;" fill="currentColor">채용 자동화</text> <text x="1250" y="610" style="text-anchor: start;" fill="currentColor">자동 아웃리치</text></svg>

Hermes Agent와 Apify를 연동하여 웹 데이터를 수집하고 분석함으로써 비즈니스 프로세스를 자동화할 수 있다.

### 1.1. Hermes Agent 설치 및 기본 설정 \[1\]

![imageDeleteButton](data:image/svg+xml,%3csvg%20xmlns='http://www.w3.org/2000/svg'%20width='14'%20height='14'%20viewBox='0%200%2014%2014'%20fill='none'%3e%3cpath%20d='M11.6673%206.33301V12.5997C11.6673%2012.8206%2011.4883%2012.9997%2011.2673%2012.9997H2.73398C2.51307%2012.9997%202.33398%2012.8206%202.33398%2012.5997V6.33301'%20stroke='%239FA28E'%20stroke-linecap='round'%20stroke-linejoin='round'/%3e%3cpath%20d='M5.66602%2010.333V6.33301'%20stroke='%239FA28E'%20stroke-linecap='round'%20stroke-linejoin='round'/%3e%3cpath%20d='M8.33398%2010.333V6.33301'%20stroke='%239FA28E'%20stroke-linecap='round'%20stroke-linejoin='round'/%3e%3cpath%20d='M13%203.66667H9.66667M9.66667%203.66667V1.4C9.66667%201.17909%209.4876%201%209.26667%201H4.73333C4.51242%201%204.33333%201.17909%204.33333%201.4V3.66667M9.66667%203.66667H4.33333M1%203.66667H4.33333'%20stroke='%239FA28E'%20stroke-linecap='round'%20stroke-linejoin='round'/%3e%3c/svg%3e) ![captureSource](https://resource-release.s3.ap-northeast-2.amazonaws.com/thumbnails/V80QfRa7t_c/0.jpg)
1. **Hermes Agent의 특징 및 활용성** \[1\]
	1. Hermes Agent는 GitHub에서 약 20만 개의 스타를 받은 세계에서 가장 인기 있는 AI 에이전트이다. \[1\]
	2. 이 에이전트는 거의 모든 작업을 수행할 수 있다. \[2\]
2. **Hermes Agent의 한계와 Apify의 필요성** \[3\]
	1. Hermes Agent는 인터넷의 중요한 사이트에 접근하려 할 때 종종 차단된다. \[3\]
	2. Apify를 활용하면 이러한 문제를 해결하고 다음과 같은 이점을 얻을 수 있다. \[4\]
		1. 비즈니스를 위한 **적격 리드** 를 발굴한다. \[4\]
		2. 회사에 **최고의 인재** 를 찾는다. \[4\]
		3. 경쟁사, 가격, 시장 변화를 **추적** 한다. \[4\]
		4. 더 나은 직업 및 경력 기회를 **찾는다**. \[4\]
		5. 에이전트가 일반적으로 차단되는 웹사이트에 **접근** 한다. \[4\]
3. **Hermes Agent 설치 방법** \[7\]
	1. Hermes Agent GitHub 저장소에 접속하여 'Quick Install' 섹션으로 이동한다. \[7\]
	2. 단일 명령어를 복사하여 터미널에 붙여넣고 실행하면 Hermes Agent가 컴퓨터에 설치된다. \[10\]
4. **Apify를 통한 Hermes Agent 기능 강화** \[15\]
	1. Apify는 40,000개 이상의 다양한 웹 스크래핑 도구를 제공한다. \[15\]
	2. Apify를 AI 에이전트에 연결하면 에이전트의 기능을 10배 이상 강력하게 만들 수 있다. \[17\]
5. **Hermes Agent 설정 완료 및** **모델** **선택** \[20\]
	1. 설치가 완료되면 다양한 제공업체 중에서 AI 모델을 선택할 수 있다. \[20\]
	2. API 키를 입력하고 모델을 선택한 후, Hermes Agent와 로컬에서 채팅할 수 있다. \[27\]
	3. Apify를 연결하여 웹의 모든 데이터에 접근하고 어떤 웹사이트든 스크래핑할 수 있도록 함으로써 Hermes Agent를 10배 더 강력하게 만들 수 있다. \[41\]

### 1.2. Apify를 활용한 데이터 스크래핑 및 Superbase 연동 \[42\]

![imageDeleteButton](data:image/svg+xml,%3csvg%20xmlns='http://www.w3.org/2000/svg'%20width='14'%20height='14'%20viewBox='0%200%2014%2014'%20fill='none'%3e%3cpath%20d='M11.6673%206.33301V12.5997C11.6673%2012.8206%2011.4883%2012.9997%2011.2673%2012.9997H2.73398C2.51307%2012.9997%202.33398%2012.8206%202.33398%2012.5997V6.33301'%20stroke='%239FA28E'%20stroke-linecap='round'%20stroke-linejoin='round'/%3e%3cpath%20d='M5.66602%2010.333V6.33301'%20stroke='%239FA28E'%20stroke-linecap='round'%20stroke-linejoin='round'/%3e%3cpath%20d='M8.33398%2010.333V6.33301'%20stroke='%239FA28E'%20stroke-linecap='round'%20stroke-linejoin='round'/%3e%3cpath%20d='M13%203.66667H9.66667M9.66667%203.66667V1.4C9.66667%201.17909%209.4876%201%209.26667%201H4.73333C4.51242%201%204.33333%201.17909%204.33333%201.4V3.66667M9.66667%203.66667H4.33333M1%203.66667H4.33333'%20stroke='%239FA28E'%20stroke-linecap='round'%20stroke-linejoin='round'/%3e%3c/svg%3e) ![captureSource](https://resource-release.s3.ap-northeast-2.amazonaws.com/thumbnails/V80QfRa7t_c/180.jpg)
1. **Apify** **MCP 커넥터** **소개** \[42\]
	1. Apify MCP 커넥터는 40,000개 이상의 액터를 Superbase, GitHub, Notion 등 데이터가 저장된 곳과 연결하여 데이터를 즉시 스크래핑하고 데이터베이스에 저장할 수 있게 한다. \[42\]
	2. 이렇게 저장된 데이터는 Hermes Agent를 통해 원하는 대로 활용할 수 있다. \[43\]
2. **Apify 계정 생성 및 콘솔 접속** \[44\]
	1. Apify는 무료로 시작할 수 있으며, 계정을 생성한 후 콘솔에 접속하여 액터 관리, 실행 기록 확인, 자동화 및 스케줄 설정 등을 할 수 있다. \[44\]
3. **LinkedIn 프로필 스크래핑 액터 설정** \[49\]
	1. 채용 후보자를 찾기 위해 LinkedIn 액터를 사용한다. \[49\]
	2. 이 액터는 LinkedIn 로그인이나 계정 쿠키가 필요 없으며, 낮은 계정 차단 위험으로 직무, 위치, 산업별 검색을 통해 풍부한 프로필 데이터를 반환한다. \[52\]
4. **Apify 액터 검색 및 활용** \[60\]
	1. Apify 콘솔에서 'Actors'를 클릭하고 'Go to Store'로 이동하면 40,000개 이상의 다양한 액터를 검색할 수 있다. \[60\]
	2. 리드 생성, 인기 액터 등 다양한 카테고리로 분류되어 있어 YouTube, Reddit, LinkedIn, Twitter 등 어떤 플랫폼이든 원하는 액터를 찾을 수 있다. \[61\]
5. **Apify 액터 테스트 실행 및 데이터 확인** \[63\]
	1. 프로필 스크래퍼 모드에서 'full'을 선택하고, 검색 쿼리(예: AI 개발자, 소프트웨어 엔지니어)와 최대 프로필 수(예: 20개), 위치 필터(예: Katowice)를 설정한다. \[63\]
	2. 설정을 '새 작업으로 저장'하고 '저장 및 시작'을 클릭하여 액터를 실행한다. \[73\]
	3. 실행이 완료되면 '저장소'에서 데이터를 확인하고 JSON 형식으로 내보낼 수 있다. \[81\]
6. **Superbase** **데이터베이스** **설정 및 연동** \[96\]
	1. Apify 액터 실행 시 생성된 데이터셋을 Superbase 데이터베이스에 저장하여 Hermes Agent가 리드를 분석하고 연락하는 등의 작업을 수행할 수 있도록 한다. \[96\]

## 2\. Superbase 연동 및 Hermes Agent를 통한 리드 분석 자동화 \[98\]

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 800" style="width: 100%; height: auto;"><defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7"></polygon></marker></defs><rect x="0" y="0" width="1400" height="800" fill="#f4f3ef"></rect><text x="700" y="110" fill="currentColor">리드 생성 및 분석 자동화 워크플로우</text> <g transform="translate(100, 320)" filter="url(#shadow)"><rect width="280" height="240" fill="none" stroke="currentColor"></rect><circle cx="140" cy="80" r="40" fill="none" stroke="currentColor"></circle><path d="M125 70h30M125 80h30M125 90h20" stroke="#1a1a1a" stroke-width="3" stroke-linecap="round"></path><rect x="120" y="65" width="40" height="35" rx="4" fill="none" stroke="#1a1a1a" stroke-width="3"></rect><text x="140" y="165" fill="currentColor">Apify 수집</text> <text x="140" y="200" fill="currentColor">LinkedIn 프로필</text> </g><g transform="translate(560, 480)" filter="url(#shadow)"><rect width="280" height="200" fill="none" stroke="currentColor"></rect><circle cx="140" cy="70" r="40" fill="none" stroke="currentColor"></circle><path d="M120 60c0-8 40-8 40 0s-40 8-40 0z M120 60v20c0 8 40 8 40 0v-20 M120 70v20c0 8 40 8 40 0v-20" fill="none" stroke="#1a1a1a" stroke-width="3" stroke-linejoin="round"></path><text x="140" y="145" fill="currentColor">Supabase 저장소</text> <text x="140" y="180" fill="currentColor">데이터 적재</text> </g><g transform="translate(560, 200)" filter="url(#shadow)"><rect width="280" height="200" fill="none" stroke="currentColor"></rect><circle cx="140" cy="70" r="40" fill="#ffffff" opacity="0.2"></circle><path d="M130 60a15 15 0 1 1 20 0c5 10-5 25-10 25s-15-15-10-25z" fill="#ffffff"></path><circle cx="135" cy="65" r="2" fill="#5a7a5a"></circle><circle cx="145" cy="65" r="2" fill="#5a7a5a"></circle><text x="140" y="145" fill="currentColor">Hermes Agent</text> <text x="140" y="180" style="font-weight: 400; font-size: 22px;" fill="currentColor">적합도 평가</text> </g><g transform="translate(1020, 320)" filter="url(#shadow)"><rect width="280" height="240" fill="none" stroke="currentColor"></rect><circle cx="140" cy="80" r="40" fill="none" stroke="currentColor"></circle><path d="M140 60l15 30h-30z M130 90v10 M150 90v10" fill="none" stroke="#1a1a1a" stroke-width="3"></path><text x="140" y="165" fill="currentColor">자동화 액션</text> <text x="140" y="200" fill="currentColor">요약 및 아웃리치</text> </g><path d="M380 440 Q 470 440 470 580 L 550 580" marker-end="url(#arrowhead)" fill="none" stroke="currentColor"></path><path d="M680 470 L 680 410" marker-end="url(#arrowhead)" fill="none" stroke="currentColor"></path><path d="M720 410 L 720 470" marker-end="url(#arrowhead)" fill="none" stroke="currentColor"></path><text x="800" y="445" style="text-anchor: start;" fill="currentColor">분석 결과 갱신</text> <path d="M840 300 Q 1160 300 1160 310" marker-end="url(#arrowhead)" fill="none" stroke="currentColor"></path><path d="M700 700 C 400 700 100 650 100 450" fill="none" stroke="currentColor"></path><circle cx="700" cy="710" r="60" fill="#ebe9e3" stroke="#d8d6d0" stroke-width="2"></circle><path d="M690 700 L 700 710 L 715 710" fill="none" stroke="#1a1a1a" stroke-width="3" stroke-linecap="round"></path><text x="700" y="755" fill="currentColor">스케줄링 시스템</text></svg>

Superbase에 저장된 스크래핑 데이터를 Hermes Agent가 분석하고, 이 과정을 자동화하여 비즈니스 효율성을 극대화할 수 있다.

### 2.1. Superbase 데이터베이스 설정 및 Apify 연동 \[98\]

![imageDeleteButton](data:image/svg+xml,%3csvg%20xmlns='http://www.w3.org/2000/svg'%20width='14'%20height='14'%20viewBox='0%200%2014%2014'%20fill='none'%3e%3cpath%20d='M11.6673%206.33301V12.5997C11.6673%2012.8206%2011.4883%2012.9997%2011.2673%2012.9997H2.73398C2.51307%2012.9997%202.33398%2012.8206%202.33398%2012.5997V6.33301'%20stroke='%239FA28E'%20stroke-linecap='round'%20stroke-linejoin='round'/%3e%3cpath%20d='M5.66602%2010.333V6.33301'%20stroke='%239FA28E'%20stroke-linecap='round'%20stroke-linejoin='round'/%3e%3cpath%20d='M8.33398%2010.333V6.33301'%20stroke='%239FA28E'%20stroke-linecap='round'%20stroke-linejoin='round'/%3e%3cpath%20d='M13%203.66667H9.66667M9.66667%203.66667V1.4C9.66667%201.17909%209.4876%201%209.26667%201H4.73333C4.51242%201%204.33333%201.17909%204.33333%201.4V3.66667M9.66667%203.66667H4.33333M1%203.66667H4.33333'%20stroke='%239FA28E'%20stroke-linecap='round'%20stroke-linejoin='round'/%3e%3c/svg%3e) ![captureSource](https://resource-release.s3.ap-northeast-2.amazonaws.com/thumbnails/V80QfRa7t_c/467.jpg)
1. **Superbase 계정 생성 및 테이블 생성** \[98\]
	1. Superbase 무료 계정을 생성하고, SQL 편집기에서 리드(leads) 테이블을 생성한다. \[98\]
	2. 생성된 테이블은 '테이블 편집기'에서 확인할 수 있다. \[116\]
2. **Apify** **MCP 커넥터** **설정** \[119\]
	1. Apify 콘솔의 '설정'에서 'API 및 통합'으로 이동하여 'MCP 커넥터' 섹션을 찾는다. \[119\]
	2. '커넥터 추가'를 클릭하고, Superbase 프로젝트 URL과 개인 액세스 토큰을 입력하여 커넥터를 설정한다. \[125\]
	3. 설정된 MCP 커넥터는 목록에 나타난다. \[146\]
3. **Apify Universal MCP Connector를 통한 데이터 전송** \[148\]
	1. Apify Universal MCP Connector 액터를 사용하여 스크래핑된 데이터셋 ID를 입력한다. \[148\]
	2. 사용자 쿼리, 언어 모델, 최대 에이전트 단계 등을 설정하고, 이전에 생성한 Superbase MCP 커넥터를 선택한다. \[161\]
	3. '저장 및 시작'을 클릭하여 액터를 실행하면, 스크래핑된 데이터가 Superbase 테이블로 전송된다. \[169\]
	4. API 키 만료 등의 오류를 해결하면, 스크래핑된 리드가 Superbase에 성공적으로 저장된 것을 확인할 수 있다. \[175\]
4. **Superbase 데이터 저장의 중요성** \[207\]
	1. 스크래핑된 데이터가 Superbase에 저장되면 Hermes Agent가 리드를 분석하고, 자격을 부여하며, 후속 워크플로우를 설정하는 등 다양한 가능성이 열린다. \[207\]

### 2.2. Hermes Agent를 통한 리드 분석 및 자동화 \[212\]

![imageDeleteButton](data:image/svg+xml,%3csvg%20xmlns='http://www.w3.org/2000/svg'%20width='14'%20height='14'%20viewBox='0%200%2014%2014'%20fill='none'%3e%3cpath%20d='M11.6673%206.33301V12.5997C11.6673%2012.8206%2011.4883%2012.9997%2011.2673%2012.9997H2.73398C2.51307%2012.9997%202.33398%2012.8206%202.33398%2012.5997V6.33301'%20stroke='%239FA28E'%20stroke-linecap='round'%20stroke-linejoin='round'/%3e%3cpath%20d='M5.66602%2010.333V6.33301'%20stroke='%239FA28E'%20stroke-linecap='round'%20stroke-linejoin='round'/%3e%3cpath%20d='M8.33398%2010.333V6.33301'%20stroke='%239FA28E'%20stroke-linecap='round'%20stroke-linejoin='round'/%3e%3cpath%20d='M13%203.66667H9.66667M9.66667%203.66667V1.4C9.66667%201.17909%209.4876%201%209.26667%201H4.73333C4.51242%201%204.33333%201.17909%204.33333%201.4V3.66667M9.66667%203.66667H4.33333M1%203.66667H4.33333'%20stroke='%239FA28E'%20stroke-linecap='round'%20stroke-linejoin='round'/%3e%3c/svg%3e) ![captureSource](https://resource-release.s3.ap-northeast-2.amazonaws.com/thumbnails/V80QfRa7t_c/803.jpg)
1. **Hermes Agent에 Superbase 접근 권한 부여** \[212\]
	1. Hermes Agent에 Superbase 프로젝트 URL과 서비스 역할 키를 제공하여 Superbase 데이터베이스에 접근할 수 있도록 설정한다. \[212\]
	2. Hermes Agent는 이 정보를 환경 변수에 저장하여 데이터베이스에 접근한다. \[245\]
2. **Hermes Agent를 통한 리드 분석** \[247\]
	1. Hermes Agent에게 Superbase의 'leads' 테이블 내용을 확인하고 사람들을 볼 수 있는지 묻는다. \[247\]
	2. Hermes Agent는 Superbase에 접근하여 리드 데이터를 확인할 수 있다. \[253\]
	3. Hermes Agent에 Superbase 프로젝트에 연결하여 'public leads' 테이블을 읽고, 각 후보자의 적합도를 0에서 100점까지 평가하도록 지시한다. \[263\]
	4. Hermes Agent는 모든 리드를 평가하고 'lead score', 'rating', 'reasoning', 'fit tags' 등의 정보를 Superbase 테이블에 다시 기록한다. \[266\]
	5. Superbase에서 리드 점수가 기록된 것을 확인하여, Hermes Agent가 잠재력 있는 후보자를 식별하는 데 도움을 줄 수 있음을 알 수 있다. \[269\]
3. **Apify와 Hermes Agent의 결합 활용 사례** \[274\]
	1. Apify와 Hermes Agent의 조합은 채용뿐만 아니라 B2B 리드 발굴, 고객 확보, 새로운 도시에서 친구 찾기, 좋은 레스토랑이나 체육관 찾기 등 다양한 분야에서 활용될 수 있다. \[274\]
	2. 웹 스크래핑을 통해 얻은 데이터를 Hermes Agent가 분석하고, 자격을 부여하며, 연락하는 등의 작업을 자동화하여 비즈니스 성장과 삶의 질 향상에 기여할 수 있다. \[283\]
4. **전체 프로세스 자동화** \[285\]
	1. **Hermes Agent 자동화**: Hermes Agent에게 매일 Superbase의 'public leads' 테이블을 읽고, 'lead score'가 null인 모든 리드를 찾아 적합도를 평가하도록 지시한다. \[286\]
		1. 평가 기준은 소프트웨어 엔지니어링 능력, AI 자동화 경험, 경력, 지역 관련성, 실제 프로젝트 수행 증거 등을 우선시한다. \[288\]
		2. 평가 후 'lead score', 'rating', 'reasoning', 'fit tags'를 각 새 행에 기록하고, 상위 5명의 후보자를 요약하여 보고하도록 설정한다. \[289\]
		3. Hermes Agent는 이를 위해 **크론 작업** **(cron job)** 을 생성하여 매일 오전 8시에 자동으로 실행되도록 설정한다. \[294\]
	2. **Apify 스크래핑 자동화**: Apify 콘솔의 '스케줄'에서 새 스케줄을 생성하고, 이전에 저장한 LinkedIn 스크래핑 작업을 선택한다. \[307\]
		1. 스케줄을 6시간마다 실행되도록 설정하여 소프트웨어 엔지니어를 지속적으로 스크래핑하도록 한다. \[313\]
		2. '저장 및 활성화'를 클릭하면 스크래핑 작업이 자동으로 실행된다. \[320\]
	3. **자동화의 이점**: 이러한 자동화는 채용 프로세스, 인재 관리, HR의 상당 부분을 자동화하여 주당 수십 시간의 인력 비용을 절감하고, 기업을 경쟁 우위에 서게 한다. \[338\]
5. **결론 및 추가 자료** \[345\]
	1. Apify와 Hermes Agent의 결합은 웹 스크래핑을 통해 상상할 수 있는 거의 모든 웹사이트에서 데이터를 수집하고 분석하는 강력한 기능을 제공한다. \[345\]
	2. Apify 무료 계정 생성 및 영상에서 사용된 모든 리소스(프롬프트, 설정, SQL 등)는 제공된 링크를 통해 얻을 수 있다. \[352\]

확장

한눈에 이해되는 애니메이션 제작

바로 적용할 수 있는 액션 아이템도출

한눈에 이해되는 인포그래픽 제작

고급

Gemini 최신 모델을 활용해 자료를 근거로 답변해요