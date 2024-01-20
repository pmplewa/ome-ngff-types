import invoke


@invoke.task
def format(ctx):
    print("## Run ruff")
    ctx.run("ruff format .")
    ctx.run("ruff check . --fix")


@invoke.task
def check(ctx):
    print("## Run ruff")
    ctx.run("ruff format . --check")
    ctx.run("ruff check .")
    print("## Run mypy")
    ctx.run("mypy . --check-untyped-defs")


@invoke.task
def test(ctx):
    print("## Run pytest")
    ctx.run("pytest --verbose tests")
