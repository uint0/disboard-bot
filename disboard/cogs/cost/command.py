import discord
import discord.ext.commands as commands
import cogs.util.decorators as deco

import handlers.cost.cost as cost_handler
import util.converter
import config


USAGE_MSG = """
Usage:
  !cost
    report <report_view> (date | current_billing | current_month) [...timeframe_args]
    credit [history_n_cycles]
""".strip()


class CostCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._cost = cost_handler.Cost()
    

    @commands.group()
    @deco.require_channel(config.discord.DISCORD_CHANNEL_AZURE)
    async def cost(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(USAGE_MSG)


    @cost.command()
    @deco.require_channel(config.discord.DISCORD_CHANNEL_AZURE)
    async def report(self, ctx,
        report: str,
        report_timeframe: util.converter.AliasedStr({
            ('date', 'daterange', 'date_range'): 'custom',
            ('current_billing', 'current_invoice'): 'last_invoice',
            ('current_month', 'currentmonth'): 'monthtodate',
        }) = None,
        start_date: util.converter.DateTimeConverter = None,
        end_date: util.converter.DateTimeConverter = None
    ):
        if report == 'list':
            return await ctx.send('Reports: ' + ', '.join(self._cost.list_views()))

        if report_timeframe is None:
            return await ctx.send(USAGE_MSG)
        
        report_spec = cost_handler.ReportSpec(
            timeframe=report_timeframe,
            start_date=start_date,
            end_date=end_date
        )

        img = self._cost.report(report, report_spec)
        await ctx.send(file=discord.File(img, f'costs.png'))


    @cost.command()
    @deco.require_channel(config.discord.DISCORD_CHANNEL_AZURE)
    async def credit(self, ctx, history_n_cycles: int = 0):
        if history_n_cycles != 0:
            await ctx.send("Cycles != 0 is unimplemented :(")
            return

        await ctx.send("Unimplemented :(")
