# uhbyeon's log_

GitHub Pages용 한국어 정적 블로그입니다. 사용자가 제공한 Stitch 화면을 바탕으로 홈, 글 목록, 소개 터미널, 게시글과 커밋 목록형 추가 페이지를 구성했습니다. 모든 메뉴와 글에는 독립 HTML 주소가 있습니다.

데스크톱과 태블릿에서는 상단 헤더와 좌측 메뉴를, 768px 미만에서는 상단 헤더와 하단 탐색 메뉴를 사용합니다. 모바일 우측 상단 메뉴 버튼에서 논문·이슈·취약점 등 전체 메뉴를 열 수 있습니다.

## 미리보기

프로젝트 폴더에서 다음을 실행하고 `http://127.0.0.1:4173`을 엽니다.

```powershell
python -m http.server 4173 --bind 127.0.0.1
```

HTML 파일을 직접 열어도 페이지 간 이동이 가능합니다. 웹 폰트와 코드 복사 등 브라우저 기능 확인에는 HTTP 미리보기를 권장합니다.

## 메뉴와 페이지

| 메뉴 | 내용 | 파일 |
| --- | --- | --- |
| `~/workspace` | 홈 | `index.html` |
| `all_logs` | 모든 기록, 검색과 분류 필터 | `posts.html` |
| `papers_AI` | 인공지능 논문 | `papers-ai.html` |
| `papers_security` | 정보보안 논문 | `papers-security.html` |
| `issues` | 이슈 | `issues.html` |
| `vulnerabilities` | 취약점 | `vulnerabilities.html` |
| `dev_notes` | 개발 노트 | `development.html` |
| `about_me` | 터미널 형식의 소개 | `about.html` |

`timeline.html`은 용도가 정해지지 않은 커밋 목록형 추가 화면입니다. 사용자의 확인에 따라 목차·코드가 있는 Stitch 화면을 실제 게시글에 사용하고, 커밋 목록형은 이 파일로 별도 보관했습니다. 기본 탐색 메뉴에는 추가하지 않았습니다.

`posts/*.html`은 글별 본문이며 목차, 코드 복사, 이전·다음 글 링크를 포함합니다. 이전의 `projects.html`, `retrospectives.html` 경로는 기존 글의 목록으로 유지됩니다.

## 콘텐츠 수정과 재생성

- `content/site.json`: 블로그 이름, 작성자, 관심 분야, 메뉴 이름과 경로
- `content/posts.json`: 글 데이터. 현재 네 글은 미리보기용 예시이며 원본을 유지했습니다.
- `tools/build-site.py`: 공통 레이아웃과 15개 HTML 페이지 생성
- `styles.css`: 공통 색상, 웹 폰트, 반응형 배치
- `reference-views.css`: `all_logs`, `about_me`, 게시글의 원본별 글꼴·간격·헤더·카드 규격
- `script.js`: 검색·필터, 모바일 메뉴, 코드 복사와 소개 터미널

글의 `body`에는 `p`, `h3`, `pre` 블록을 사용합니다. 새 글의 `id`는 소문자 영문·숫자·하이픈으로 작성합니다. `section`을 `ai`, `security`, `issues`, `vulnerabilities`, `development` 중 하나로 지정하면 해당 메뉴에 표시됩니다. `section`이 없는 기존 개발 글은 `dev_notes`에 연결되며 다른 기존 글도 `all_logs`에서 볼 수 있습니다. 논문·이슈·취약점 글은 아직 없으므로 해당 페이지에는 빈 목록 안내가 표시됩니다.

```powershell
python tools/build-icons.py
python tools/build-site.py
python tools/export-terminal-concept.py
```

아이콘을 바꾸지 않을 때는 첫 명령을 생략해도 됩니다. HTML을 직접 수정하면 다음 재생성 때 덮어쓰므로 공통 구조는 생성 도구에서 수정합니다. 게시된 페이지를 보는 데 Python은 필요하지 않습니다.

소개 터미널의 빠른 명령은 원본의 `[help]`, `[posts]`, `[projects]`, `[skills]`, `[clear]`입니다. 이전 탐색 명령도 유지합니다. `clear`는 실행 결과를 비우며 기본 프로필을 지우지 않습니다. 실제 운영체제 명령은 실행하지 않습니다. 검색과 분류 필터는 함께 적용되며, `all_logs`의 필터는 현재 글에 있는 분류와 실제 개수로 생성됩니다.

`content/site.json`의 `tech_stack`과 `contacts`를 채우면 원본의 기술 스택·연락처 영역에 표시됩니다. 현재 값은 비어 있으며 참고 화면의 가상 경력·기술 버전·연락처·통계 수치는 복제하지 않았습니다.

## 브라우저 탭 아이콘

헤더의 터미널 심벌과 같은 형태로 `favicon.svg`, `favicon-32.png`, `favicon.ico`(16/32/48px), `apple-touch-icon.png`(180px)를 제공합니다. 모든 페이지의 제목은 `uhbyeon's log_ · 페이지 이름`이며, 아이콘 링크에는 캐시 갱신용 버전을 지정했습니다. GitHub 프로젝트 하위 경로에서도 동작하도록 모든 로컬 자산은 상대 경로로 연결했습니다.

## 디자인 원본과 이전 시안

사용자가 지정하고 최종 역할을 확인한 다섯 Stitch 링크는 `designs/stitch-references.json`에 기록했습니다. 각 시안의 다른 메뉴, 가상 경력·기술 수준·조회 수 등은 복제하지 않았습니다.

세부 화면에는 홈 전용 경로 줄·인용 푸터를 반복하지 않습니다. 목록의 추가 집계 줄과 `read log` 버튼, 소개 화면의 임의 주제 카드·설명문, 게시글의 `목록으로`·`예시 글` 표기는 제거했습니다. 제목·본문 크기, 복사 버튼 위치, 코드 줄 번호, 목차, 빠른 명령과 입력창은 해당 원본을 기준으로 맞춥니다. 공통 메뉴와 브랜드는 사용자가 지정한 구성을 유지합니다.

원본에서 확인한 대표 규격은 목록 제목 22/30px, 설명 13/21.125px, 게시글 제목 모바일 22/30px·데스크톱 28/36px, 본문 14/22.75px입니다. 색상은 원본의 강조색 `#5bf06c`, 테두리 `#3d4a3b`, 보조 글자색 `#bccbb6`을 사용합니다. 세부 화면의 줄바꿈도 원본처럼 `normal`로 적용합니다.

`designs/05-stitch-home.html`은 현재 홈을 HTML·CSS·JavaScript 한 파일로 묶은 미리보기입니다. 아이콘과 글 페이지 링크는 프로젝트 파일을 사용합니다. 이전 `designs/01-editorial.html`부터 `04-terminal-sidebar.html`까지와 Canva 링크는 당시 디자인 기록으로 보존했습니다. 현재 Stitch 반영 사항은 이전 Canva 디자인에 자동 동기화되지 않습니다.

## 게시와 업데이트

- 블로그: <https://byeonui-hyeok.github.io/>
- 저장소: <https://github.com/ByeonUi-Hyeok/ByeonUi-Hyeok.github.io>
- GitHub Pages 게시 소스: `main` 브랜치의 `/ (root)`

글을 수정한 뒤 `python tools/build-site.py`로 HTML을 재생성하고 변경 사항을 `main`에 커밋·푸시하면 GitHub Pages가 자동으로 다시 게시합니다. 아이콘을 수정했을 때만 먼저 `python tools/build-icons.py`를 실행합니다.

`output/`, `designs/`와 이전 시안 생성 도구는 로컬 디자인 기록이므로 `.gitignore`로 공개 저장소에서 제외합니다. 다른 컴퓨터에서 저장소를 복제했을 때는 블로그 생성에 `tools/build-site.py`와 `tools/build-icons.py`를 사용합니다.

댓글·로그인·관리자·서버 저장 기능은 포함하지 않습니다.
