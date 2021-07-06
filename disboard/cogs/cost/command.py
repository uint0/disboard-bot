import datetime as dt

import discord
import discord.ext.commands as commands

import util.discord
import util.converter

import handlers.cost.cost as cost_handler
import handlers.cost.exceptions as cost_exceptions
import config


USAGE_MSG = """
Usage:
  !cost
    report <report_view> (date | current_billing | current_month) [...timeframe_args]
    summary
""".strip()


class CostCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._cost = cost_handler.Cost()
    

    @commands.group()
    @util.discord.require_channel(config.discord.DISCORD_CHANNEL_AZURE)
    async def cost(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(USAGE_MSG)


    @cost.command()
    @util.discord.require_channel(config.discord.DISCORD_CHANNEL_AZURE)
    @util.discord.raises_exception(cost_exceptions.CostViewNotFoundException)
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

        img = await self._cost.report(report, report_spec)
        await ctx.send(file=discord.File(img, f'costs.png'))


    @cost.command()
    @util.discord.require_channel(config.discord.DISCORD_CHANNEL_AZURE)
    async def summary(self, ctx):
        summary = await self._cost.summary()

        billing_period_length = (util.time.midnight(summary.end_date) - util.time.midnight(summary.start_date)).days
        days_remaining = (util.time.midnight(summary.end_date) - util.time.midnight(dt.date.today())).days
        days_elapsed   = billing_period_length - days_remaining

        embed = discord.Embed(
            title="Cost Summary",
            description=f"{summary.start_date:%Y-%m-%d} to {summary.end_date:%Y-%m-%d}",
            color=0xffff1a
        )
        embed.set_author(name="Azure Cost Management")
        embed.set_thumbnail(url='https://pbs.twimg.com/profile_images/1283873419117789184/n5W9EoMe_400x400.jpg')
        embed.add_field(
            name="Days Remaining",
            value=f"{days_remaining} day(s)",
            inline=True
        )

        embed.add_field(
            name="Total Cost",
            value=f"${summary.total_costs:.2f}",
        )
        embed.add_field(
            name="Linear Cost Forecast",
            value=f"${billing_period_length * summary.total_costs / days_elapsed:.2f}",
            inline=True
        )
        embed.set_footer(text=f"Latest Cost Reporting: {summary.latest_reported_date:%Y-%m-%d}")

        await ctx.send(embed=embed)
