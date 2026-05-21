import nox

nox.options.sessions = ["tests", "lint"]


@nox.session(python=["3.10", "3.11"])
def tests(session):
    session.install("-r", "requirements-dev.txt")
    session.run("pytest", "-q")


@nox.session(python=["3.10", "3.11"])
def lint(session):
    session.install("ruff")
    session.run("ruff", "check", ".")


@nox.session(python=["3.10"])
def format(session):
    session.install("ruff")
    session.run("ruff", "format", ".")
