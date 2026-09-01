# Todo REST API

FastAPI로 만든 간단한 Todo REST API입니다. 데이터는 메모리에 저장되므로
서버를 재시작하면 초기화됩니다.

## 요구 사항

- Python 3.10+

## 설치

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 실행

```bash
uvicorn app.main:app --reload
```

- API 문서(Swagger UI): http://127.0.0.1:8000/docs
- OpenAPI 스키마: http://127.0.0.1:8000/openapi.json

## 엔드포인트

### GET /todos

전체 Todo 목록을 반환합니다.

```bash
curl http://127.0.0.1:8000/todos
```

```json
[
  { "id": 1, "title": "Buy milk", "completed": false }
]
```

### POST /todos

새 Todo를 생성합니다.

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `title` | string | ✅ | 1~200자 |
| `completed` | boolean | ❌ | 기본값 `false` |

```bash
curl -X POST http://127.0.0.1:8000/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy milk"}'
```

응답 (`201 Created`):

```json
{ "id": 1, "title": "Buy milk", "completed": false }
```

### GET /todos/{id}

단건 조회. 없으면 `404`.

```bash
curl http://127.0.0.1:8000/todos/1
```

### PUT /todos/{id}

전체 교체. 본문은 `POST /todos`와 동일한 스키마이며 모든 필드를 보내야 합니다. 없으면 `404`.

```bash
curl -X PUT http://127.0.0.1:8000/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy oat milk", "completed": true}'
```

### PATCH /todos/{id}

부분 수정. 보낸 필드만 갱신합니다. 없으면 `404`.

```bash
curl -X PATCH http://127.0.0.1:8000/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

### DELETE /todos/{id}

삭제. 성공 시 `204 No Content`, 없으면 `404`.

```bash
curl -X DELETE http://127.0.0.1:8000/todos/1
```

## 개발

```bash
pip install -r requirements-dev.txt
ruff check .          # 린트
ruff format .         # 포매팅
pytest                # 테스트
```

CI(GitHub Actions)는 Python 3.10/3.11/3.12에서 위 세 가지를 실행합니다.
