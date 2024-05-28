import json
import uuid
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from ..utils.paper_collector import get_daily_papers


class PaperProfile(BaseModel):
    pk: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: Optional[str] = Field(default=None)
    abstract: Optional[str] = Field(default=None)


class PaperProfileDB:
    def __init__(self) -> None:
        self.data: Dict[str, PaperProfile] = {}

    def add_paper(self, paper: PaperProfile) -> None:
        self.data[paper.pk] = paper

    def update_paper(self, paper_pk: str, updates: Dict[str, Optional[str]]) -> bool:
        if paper_pk in self.data:
            for key, value in updates.items():
                if value is not None:
                    setattr(self.data[paper_pk], key, value)
            return True
        return False

    def get_paper(self, paper_pk: str) -> Optional[PaperProfile]:
        return self.data.get(paper_pk)

    def delete_paper(self, paper_pk: str) -> bool:
        if paper_pk in self.data:
            del self.data[paper_pk]
            return True
        return False

    def query_papers(self, **conditions: Dict[str, Any]) -> List[PaperProfile]:
        result = []
        for paper in self.data.values():
            if all(getattr(paper, key) == value for key, value in conditions.items()):
                result.append(paper)
        return result

    def save_to_file(self, file_name: str) -> None:
        with open(file_name, "w") as f:
            json.dump({pk: paper.dict()
                      for pk, paper in self.data.items()}, f, indent=2)

    def load_from_file(self, file_name: str) -> None:
        with open(file_name, "r") as f:
            data = json.load(f)
            self.data = {pk: PaperProfile(**paper_data)
                         for pk, paper_data in data.items()}

    def update_db(self, data: Dict[str, List[Dict[str, Any]]]) -> None:
        for date, papers in data.items():
            for paper_data in papers:
                paper = PaperProfile(**paper_data)
                self.add_paper(paper)

    def fetch_and_add_papers(self, num: int, domain: str) -> None:
        data, _ = get_daily_papers(domain, query=domain, max_results=num)
        transformed_data = {}
        for date, value in data.items():
            papers = []
            papers.append({"abstract": value["abstract"]})
            papers.append({"info": value["info"]})
            transformed_data[date] = papers
        self.update_db(transformed_data)