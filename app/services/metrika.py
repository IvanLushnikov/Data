# app/services/metrika.py
import os
import httpx
from datetime import datetime, timedelta

YANDEX_METRICA_OAUTH = os.getenv("YANDEX_METRICA_OAUTH_TOKEN")
COUNTER_ID = os.getenv("YANDEX_METRICA_COUNTER_ID")

async def fetch_logs(start_date: str, end_date: str, limit: int = 10000):
    """
    Запрашиваем сырые хиты/события из Яндекс.Метрики Logs API
    за указанный период.
    """
    url = "https://api-metrika.yandex.net/management/v1/counters/{cid}/logrequests".format(cid=COUNTER_ID)
    headers = {"Authorization": f"OAuth {YANDEX_METRICA_OAUTH}"}
    # Создаём задачу лога
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, headers=headers, json={
            "date1": start_date,
            "date2": end_date,
            "fields": ["ym:pv:URL", "ym:pv:browser", "ym:pv:referer", "ym:pv:clientID"],
            "limit": limit
        })
        resp.raise_for_status()
        job = resp.json()["log_request"]

    # Ждём готовности (в реальном коде — асинхронный retry/callback)
    job_id = job["id"]
    fetch_url = url + f"/{job_id}/download"
    # Сразу скачиваем (для упрощения)
    dl_resp = await client.get(fetch_url, headers=headers)
    dl_resp.raise_for_status()
    # dl_resp.text — CSV/TSV с данными
    return dl_resp.text.splitlines()
