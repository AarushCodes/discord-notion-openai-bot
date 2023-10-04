import requests
from datetime import datetime, timezone


class notion:
    
    def __init__(self,databaseid,notiontoken):
        self.databaseid = databaseid
        self.notiontoken = notiontoken

        self.headers = {
        "Authorization": "Bearer " + notiontoken,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
        }

    
    
    def createpage(self,data: dict):
        DATABASE_ID = self.databaseid
        create_url = "https://api.notion.com/v1/pages"
        payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}
        res = requests.post(create_url, headers=self.headers, json=payload)
        statuscode = res.status_code
        return statuscode
    
    def addnewidea(self, idea, description='Not specified...', aiaskedresult='not asked to ai'):
        published_date = datetime.now().astimezone(timezone.utc).isoformat()
        data = {
        "Idea": {"title": [{"text": {"content": idea}}]},
        "Description": {"rich_text": [{"text": {"content": description}}]},
        "time and date": {"date": {"start": published_date, "end": None}},
        "AI suggestions": {"rich_text": [{"text": {"content": aiaskedresult}}]}
        }
        statuscode = self.createpage(data)
        return statuscode

