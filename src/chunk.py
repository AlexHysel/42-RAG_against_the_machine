from pydantic import BaseModel, Field, model_validator, FilePath


class Chunk(BaseModel):
    start: int = Field(ge=0)
    end: int = Field(ge=0)
    content: str = Field(min_length=1)
    file_path: FilePath | None = None

    @classmethod
    def create(offset: int,
            content: str,
            file_path: None | FilePath = None
            ) -> Chunk:
        return Chunk(start=offset, end=len(content)+offset, content=content, file_path=file_path)

    @model_validator(mode="after")
    def check_start_and_end(self) -> "Chunk":
        if self.end < self.start:
            raise ValueError("end must be greater than or equal to start")
        return self
