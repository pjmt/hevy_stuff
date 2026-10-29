"""Typer CLI entry point."""

from __future__ import annotations

import typer

from hevy import __version__

app = typer.Typer(help="Hevy tools")


@app.command()
def version() -> None:
    """Print the package version."""
    typer.echo(__version__)


@app.command()
def workouts() -> None:
    """List workouts from the API."""
    from hevy.services.hevy_client import HevyClient

    with HevyClient() as client:
        for w in client.list_workouts():
            typer.echo(f"{w.id}  {w.title}  sets={w.sets}")

@app.command()
def userinfo() -> None:
    """Get user info from the API."""
    from hevy.services.hevy_client import HevyClient

    with HevyClient() as client:
        u = client.get_userinfo()
        typer.echo(f"{u.id}  {u.name}")
