from fluid import Fluid
from pydantic import BaseModel

from package_name.operations import addition

app = Fluid(
    mkdocs_dir=None  # "./docs"
)


class AdditionResult(BaseModel):
    addition: int


class FluidTestService:

    @app.post
    def add(self, a: int, b: int) -> AdditionResult:
        s = addition(a, b)
        return AdditionResult(addition=s)


if __name__ == '__main__':
    app.run_app(FluidTestService())
