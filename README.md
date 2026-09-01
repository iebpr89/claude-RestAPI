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

## 테스트

```bash
pytest
```
