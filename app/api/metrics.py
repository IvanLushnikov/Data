from fastapi import APIRouter, BackgroundTasks
from app.services.metrika import fetch_logs

router = APIRouter()

@router.post("/import")
async def import_metrika(background_tasks: BackgroundTasks):
    # получаем вчерашнюю дату
    today = datetime.utcnow().date()
    start = (today - timedelta(days=1)).isoformat()
    end = today.isoformat()
    # ставим задачу фонового импорта
    background_tasks.add_task(fetch_and_store, start, end)
    return {"status": "scheduled"}

async def fetch_and_store(start, end):
    lines = await fetch_logs(start, end)
    # парсим CSV и пишем в БД
    for row in parse_csv(lines):
        await save_to_db(row)
