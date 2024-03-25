from pydantic import BaseModel


class CustomBaseModel(BaseModel):
    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        return {k: v for k, v in d.items() if v is not None}
