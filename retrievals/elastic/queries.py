from dataclasses import dataclass
from typing import Any


@dataclass
class BaseQuery:
    def to_dict(self):
        raise NotImplementedError("Subclasses should implement this!")


@dataclass
class Match(BaseQuery):
    field: str
    value: Any

    def to_dict(self):
        return {"match": {self.field: self.value}}


@dataclass
class MatchPhrase(Match):
    def to_dict(self):
        return {"match_phrase": {self.field: self.value}}


@dataclass
class MatchAll(BaseQuery):
    def to_dict(self):
        return {"match_all": {}}


@dataclass
class Bool(BaseQuery):
    must: list[BaseQuery]

    def to_dict(self):
        return {"bool": {"must": [q.to_dict() for q in self.must]}}

if __name__ == "__main__":
    match = Match("title", "python")
    print(match.to_dict())
    match_phrase = MatchPhrase("title", "python")
    print(match_phrase.to_dict())
    match_all = MatchAll()
    print(match_all.to_dict())
    bool_query = Bool([match, match_phrase])
    print(bool_query.to_dict())

    query =  {"bool": 
              {"must": [{"match" : {"lemmatized_text": "Как ответить на требование"}}, {"match_phrase": {"sys_ids": "1"}}]}}
    
    print(query)
    match = MatchPhrase("sys_ids", "1")
    match_phrase = Match("lemmatized_text", "Как ответить на требование")
    bool_query = Bool([match_phrase, match])

    print(bool_query.to_dict())