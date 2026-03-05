# sugang_py

Playwright 기반 **수강신청 자동화 스크립트**입니다.  
로그인 → 신청 페이지 준비 → **목표 시간까지 정밀 대기** → 과목(코드) 자동 신청을 수행합니다.

> ⚠️ **주의 / 면책**  
> 이 프로젝트는 학습·연구 목적의 예시입니다. 실제 사용 시 해당 사이트의 **이용약관/규정**을 준수해야 하며, 자동화 사용으로 발생하는 모든 책임은 사용자에게 있습니다.

---

## 1. 요구 사항

- Python **3.10+**
- Playwright (Python) + Chromium

운영체제: Windows / macOS / Linux 모두 가능

---

## 2. 설치 방법

### 2.1 저장소 준비

```bash
git clone https://github.com/achiyang/sugang_py
cd sugang_py
```

### 2.2 패키지 설치 (권장)

`src/` 레이아웃 프로젝트이므로 **editable install(-e)** 로 설치하는 것을 권장합니다.

```bash
pip install -e .
```

### 2.3 Playwright 브라우저 설치

Playwright는 라이브러리 설치와 별개로 **브라우저 설치**가 필요합니다.

```bash
playwright install
```

(선택) Chromium만 설치할 수도 있습니다.

```bash
playwright install chromium
```

---

## 3. 실행 방법

### 3.1 모듈 실행

직접 모듈로 실행하고 싶다면:

```bash
python -m sugang_py.main
```

---

## 4. 환경 변수(.env) 설정

이 프로젝트는 `.env` 파일(또는 환경 변수)을 통해 설정을 주입합니다.  
루트 디렉토리에 `.env` 파일을 만들고 `.env.example`를 참고하여 값을 채우세요.

### 4.1 `.env` 템플릿

```dotenv
# ===== 계정 정보 =====
SUGANG_USER_ID=your_id
SUGANG_USER_PW=your_password

# ===== 신청할 과목 코드 (쉼표로 구분) =====
SUBJECT_CODES=ABC123,DEF456,GHI789

# ===== 목표 시작 시각 =====
# ISO 8601 형식 권장: YYYY-MM-DDTHH:MM:SS
SUGANG_TARGET_AT=2026-03-03T10:00:00

# ===== 타이밍/반복 튜닝 =====
# 목표 시간보다 미리 클릭/요청을 시작할 시간(ms)
SUGANG_ADVANCE_MS=250

# 과목 목록을 몇 번 반복 시도할지
SUGANG_REPEAT=50

# 각 시도 사이의 대기 간격(ms)
SUGANG_INTERVAL_MS=10

# ===== 실행 옵션 =====
# true/false 형태 사용 권장
SUGANG_HEADLESS=false
```

---

## 5. 환경 변수 상세 설명

### 5.1 계정

| 변수 | 필수 | 설명 | 예시 |
|---|---:|---|---|
| `SUGANG_USER_ID` | ✅ | 로그인 아이디 | `20201234` |
| `SUGANG_USER_PW` | ✅ | 로그인 비밀번호 | `p@ssw0rd` |

> ✅ 보안 팁  
> - `.env` 파일을 **git에 커밋하지 마세요**. (`.gitignore`에 추가 권장)  
> - 공용 PC/공유 폴더에 `.env`를 남기지 마세요.

---

### 5.2 신청 과목

| 변수 | 필수 | 설명 | 예시 |
|---|---:|---|---|
| `SUGANG_SUBJECT_CODES` | ✅ | 신청할 과목 코드 목록(쉼표 구분) | `ABC123,DEF456` |

- 공백이 섞이면 파싱이 꼬일 수 있으니 **쉼표만** 사용을 권장합니다.
- 예: `ABC123, DEF456`(공백 포함) 대신 `ABC123,DEF456` 권장

---

### 5.3 목표 시각 (정밀 대기)

| 변수 | 필수 | 설명 | 예시 |
|---|---:|---|---|
| `SUGANG_TARGET_AT` | ✅ | 목표 시작 시각. 해당 시각에 맞춰 신청 루프 시작 | `2026-03-03T10:00:00` |

권장 형식: **ISO 8601**  
- `YYYY-MM-DDTHH:MM:SS` 예) `2026-03-03T10:00:00`

> ⏰ 타임존(중요)  
> - 기본적으로 **로컬 시간(PC 시간)** 기준입니다.  
> - PC 시간이 실제 시간과 다르면 성능이 크게 떨어집니다.  
> - 수강신청은 1초 단위보다 더 민감할 수 있으니 **PC 시간을 정확히 맞추세요**.
> - ntp.kriss.re.kr 서버와 시간 동기화 추천

---

### 5.4 타이밍 튜닝 파라미터

| 변수 | 기본 성격 | 설명 | 추천 시작값 |
|---|---|---|---:|
| `SUGANG_ADVANCE_MS` | 공격성↑ | 목표 시각보다 **몇 ms 먼저** 클릭/요청을 시작할지 | `250` |
| `SUGANG_REPEAT` | 시도량↑ | 총 신청을 시도하는 횟수 | `50` |
| `SUGANG_INTERVAL_MS` | 부하↓ | 각 시도 사이 쉬는 간격(ms) | `10` |

#### 5.4.1 `SUGANG_ADVANCE_MS` (중요)

- 너무 작으면: 목표 시각에 늦어질 수 있음
- 너무 크면: 서버에서 "너무 이른 요청"으로 실패하거나 의미 없는 트래픽만 발생

권장:
- **100~300ms** 범위에서 환경에 맞게 조정

#### 5.4.2 `SUGANG_REPEAT`

- 누적 신청횟수 50회 마다 captcha 인증 발생

권장:
- ~50 범위에서 테스트

#### 5.4.3 `SUGANG_INTERVAL_MS`

- 너무 낮으면(0~5ms): 사이트 측 제한/차단 위험, 로컬 CPU도 상승
- 너무 높으면(50ms+): 경쟁 상황에서 손해

권장:
- 10 ± 5ms

---

### 5.5 실행 옵션

| 변수 | 설명 | 예시 |
|---|---|---|
| `SUGANG_HEADLESS` | 브라우저 UI 표시 여부 | `false`(표시), `true`(숨김) |

권장:
- 처음 설정/디버깅은 `SUGANG_HEADLESS=false`
- 실제 실행은 `SUGANG_HEADLESS=true`가 더 가볍습니다.

---