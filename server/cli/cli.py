import click

from django.db.models import Q
from core.models.models import Actor, Movie

from cli import action
from core.utils.db import db_restore

from .repl import repl
from core.utils import local


@click.group(invoke_without_command=True, context_settings={})
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        repl(ctx)


@cli.group()
def show():
    pass


@show.command(help="show the statistics information.")
def info():
    action.show_info()


@show.command('actors')
def show_actors():
    action.show_actors()


@cli.command
@click.argument('aid')
def collate(aid):
    local.collate(aid)


@cli.command
def collate_all():
    actors = Actor.objects.filter(rating__gt=0)

    for actor in actors:
        click.echo(f"collate the actress {actor.name}")
        local.collate_actor(actor)


@cli.group()
def refresh():
    pass


@refresh.command(name="actors")
def refresh_actors():
    action.refresh_actors()


@refresh.command(name="videos")
def refresh_videos():
    local.refresh_vedios()


''' --- DB mode ---- '''


@cli.group(short_help="Enter to Database mode")
def db():
    pass


@db.command()
def backup():
    click.echo("Backing up the database data to files...")
    # db.backup()
    click.echo("Backup is complete.")


@db.command()
def restore():
    click.echo("Restoring the backup data...")
    db_restore()
    click.echo("Restored the database data.")


''' --- Actor mode ---- '''


@cli.group('actor', invoke_without_command=True, short_help="Enter to Actor mode")
@click.argument('name')
@click.pass_context
def actor_mode(ctx, name):
    actor = Actor.objects.get(Q(name=name) | Q(sid=name))
    if actor is None:
        click.echo("Can't find the actor, ID or NAME is %s." % name)
        return
    if ctx.invoked_subcommand is None:
        ctx.obj = actor
        prompt_kwargs = {
            'message': '%s(%s)> ' % (actor.name, actor.sid)
        }
        repl(click.get_current_context(), prompt_kwargs=prompt_kwargs)
    else:
        ctx.obj = actor


@actor_mode.command('show')
@click.pass_context
def show_actors(ctx):
    actor = ctx.obj
    action.show_actor(actor)


@actor_mode.command('refresh')
@click.argument('option', type=click.Choice(['list', 'all']), required=False)
@click.pass_context
def refresh_actor(ctx, option):
    actor = ctx.obj
    if option is None:
        click.echo("refresh")

    if option == 'list':
        action.refresh_actor(actor.sid)
    if option == 'all':
        action.refresh_actor_movies(actor)

    action.show_actor(actor)


@actor_mode.command('list')
# @click.argument('option', type=click.Choice(['list', 'all']), required=False)
@click.pass_context
def actor_list_movies(ctx):
    actor = ctx.obj
    action.list_actor_movies(actor)


ACTRESS_ATTRS = ['rating', 'status', 'description']


@actor_mode.command('set')
@click.pass_context
@click.argument('attribute', type=click.Choice(ACTRESS_ATTRS))
@click.argument('value')
def change_actor_value(ctx, attribute, value):
    """ 'set <attribute> <value>
    """
    actor = ctx.obj
    # actress.[attribute] = value
    # setattr(actress, attribute, value)
    # actress.save()
    # TODO: 当前 actress 实例未改变值
    # Actor.objects.update({attribute: value}).where(
    #     id == actress.id).execute()
    actor.__setattr__(attribute, value)
    actor.save()
    actor.refresh_from_db()
    action.show_actor(actor)


'''---------- Movie mode ---------'''


@cli.group('movie', invoke_without_command=True, short_help="Enter to Movie mode")
@click.argument('code')
# @click.argument('number', required=False)
@click.pass_context
def movie_mode(ctx, code):
    code = code.upper()

    movie = Movie.objects.get(code=code)
    if movie is None:
        click.echo("Can't find the movie of CODE is %s." % code)
        return
    if ctx.invoked_subcommand is None:
        ctx.obj = movie
        prompt_kwargs = {
            'message': '%s> ' % code
        }
        repl(click.get_current_context(), prompt_kwargs=prompt_kwargs)
    else:
        ctx.obj = movie


@movie_mode.command('show')
@click.pass_context
def movie_show(ctx):
    movie = ctx.obj
    action.show_movie(movie)


@movie_mode.command('refresh')
@click.pass_context
def movie_refresh(ctx):
    movie = ctx.obj
    movie = action.refresh_movie(movie)
    action.show_movie(movie)


MOVIE_ATTRS = ['rating', 'description']


@movie_mode.command('set')
@click.pass_context
@click.argument('attribute', type=click.Choice(MOVIE_ATTRS))
@click.argument('value')
def movie_set(ctx, attribute, value):
    movie = ctx.obj

    movie.__setattr__(attribute, value)
    movie.save()

    movie.refresh_from_db()
    action.show_movie(movie)
