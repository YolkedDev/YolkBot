
def is_on_team(ctx):
    return ctx.author.id in ctx.bot.team["member_ids"]
