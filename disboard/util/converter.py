import dateutil.parser

import discord.ext.commands as commands

import util.time


class DateTimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        dt = dateutil.parser.parse(argument)
        return util.time.midnight(dt)


class AliasedStr(commands.Converter):
    def __init__(self, aliases={}, *, case_sensitive=False, reflexive=True):
        self._prop_case_sensitive = case_sensitive
        self._prop_reflexive = reflexive

        self._aliases = self._normalize_aliases(aliases)
    
    def _normalize_aliases(self, aliases):
        norm_aliases = {}

        for alias_list, name in aliases.items():
            norm_aliases.update({
                self._normalize_case(alias): name for alias in alias_list
            })

            if self._prop_reflexive:
                norm_aliases[self._normalize_case(name)] = name

        return norm_aliases
    
    def _normalize_case(self, s):
        return s if self._prop_case_sensitive else s.lower()

    async def convert(self, ctx, argument):
        return self._aliases.get(self._normalize_case(argument))
