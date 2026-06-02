# 0.2.x TODO  BenchChef Backend Domain Foundation

## TODO 0.2.0 — Connection Profile Foundation

### Purpose

Create the first persistent backend domain layer for BenchChef.

This step introduces the connection configuration model used to describe a target SpaghettiChef runtime.

### Work To Do


#### 0. Create superuser django admin

 

```bash
python manage.py createsuperuser
# start server:


python manage.py runserver 0.0.0.0:18090
```

Open:

```text
http://localhost:18090/admin
```

and login with the credentials you created.




#### 1. Use existing Django apps

Apps already created:

```text
connections
probes
benchmarks
reports
```

This step focuses primarily on the `connections` app.

#### 2. Add `ConnectionProfile` model

Create:

```text
backend-django/connections/models.py
```

Add a first model representing a SpaghettiChef connection configuration.

Suggested fields:

```text
name
base_url
role_header
enabled
created_at
updated_at
```

 

Example intent:

```text
BenchChef Local Runtime
http://localhost:18080
ADMIN
enabled=true
```

#### 3. Create database migration

After each models.py change, run :
```bash
cd backend-django 
source .venv/bin/activate

python manage.py makemigrations
python manage.py migrate
```

#### 4. Register model in Django admin

Create or update:

```text
backend-django/connections/admin.py
```

Register:

```text
ConnectionProfile
```

The model should become visible in:

```text
/admin
```

#### 5. Add serializer

Create:

```text
backend-django/connections/serializers.py
```

Add:

```text
ConnectionProfileSerializer
```

#### 6. Add REST API views

Create:

```text
backend-django/connections/views.py
```

Add basic API endpoints for:

```text
connection profile list
connection profile detail
```

#### 7. Register API routes

Create:

```text
backend-django/connections/urls.py
```

Expose routes similar to:

```text
GET    /api/connections
POST   /api/connections
GET    /api/connections/{id}
PUT    /api/connections/{id}
DELETE /api/connections/{id}
```

Register the app URLs in:

```text
backend-django/benchchef/urls.py
```




#### 8. Verify API behavior

Start backend:

```bash
python manage.py runserver 0.0.0.0:18090
```

Test:

```bash
curl -fsS http://localhost:18090/api/connections
```

Expected:

```text
valid JSON response
```

### Acceptance Criteria

```text
ConnectionProfile model exists
database migration succeeds
model visible in Django admin
serializer exists
REST endpoints exist
GET /api/connections works
POST /api/connections works
backend starts successfully
```


Use this small full CRUD test sequence, to routes similar to:

```text
GET    /api/connections
POST   /api/connections
GET    /api/connections/{id}
PUT    /api/connections/{id}
DELETE /api/connections/{id}
```

#### 1. GET — list connections

Should return an array.

```bash
curl -fsS http://localhost:18090/api/connections/
```

Expected initially:

```json
[]
```

or existing objects.

---

#### 2. POST — create connection

```bash
curl -fsS \
  -X POST \
  http://localhost:18090/api/connections/ \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Local SpaghettiChef",
    "base_url": "http://localhost:18080",
    "role_header": "ADMIN",
    "enabled": true
  }'
```

Expected:

```json
{
  "id": 1,
  "name": "Local SpaghettiChef",
  ...
}
```

Note the returned `id`.

---

### 3. GET — list again

Verify persistence.

```bash
curl -fsS http://localhost:18090/api/connections/
```

Should now contain your created profile.

---

### 4. GET — detail by id

Replace `1` if needed.

```bash
curl -fsS http://localhost:18090/api/connections/1/
```

Expected:

```json
{
  "id": 1,
  "name": "Local SpaghettiChef",
  ...
}
```

---

#### 5. PUT — full update

```bash
curl -fsS \
  -X PUT \
  http://localhost:18090/api/connections/1/ \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Local SpaghettiChef Updated",
    "base_url": "http://localhost:18180",
    "role_header": "OPERATOR",
    "enabled": false
  }'
```

Then verify:

```bash
curl -fsS http://localhost:18090/api/connections/1/
```

---

#### 6. DELETE — remove object

```bash
curl -fsS \
  -X DELETE \
  http://localhost:18090/api/connections/1/
```

Expected:

```text
empty response
```

---

#### 7. Final GET — verify deletion

```bash
curl -fsS http://localhost:18090/api/connections/
```

Should be empty again.

If all 7 work, your **0.2.0 CRUD layer is proven**.



### Suggested Commit

```bash
git status
git add .
git commit -m '0.2.0 - Add connection profile foundation'
```
