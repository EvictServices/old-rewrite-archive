import asyncio

from discord import (
    Embed, 
    Message,
    Member
)
from discord.ext.commands import (
    Cog, 
    command, 
    parameter,
    cooldown,
    BucketType,
    group
)

from random import randint, choice
from typing import Optional

from vesta.framework import Vesta, Context
from vesta.framework.tools.handlers.vape import valid_flavors
from vesta.framework.tools.formatter import plural

class Fun(Cog):
    def __init__(self, bot: Vesta):
        self.bot = bot

    @command(
        name="penis", 
        aliases=["size", "dih"],
        description="Get a members penis size."
    )
    async def penis(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to get the penis size of."
        )
    ) -> Message:
        """
        Get a members penis size.
        """
        embed = Embed(
            title=f"{member.name}'s penis size",
            description=f"8{'==='[randint(1, 20) :]}D",
            color=ctx.author.top_role.color,
        )
        return await ctx.send(embed=embed)
    
    @command(
        name="impersonate",
        aliases=["mock"],
        description="Impersonate a member."
    )
    @cooldown(1, 10, BucketType.user)
    async def impersonate(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to impersonate."
        ),
        *,
        content: str
    ) -> Message:
        """
        Impersonate a member.
        """
        await ctx.message.delete(delete_after=0.5)
        webhook = await ctx.channel.create_webhook(
            name=f"{member.display_name}",
            avatar=member.display_avatar.url,
            reason=f"Impersonated by {ctx.author.display_name}"
        )
        await webhook.send(content)
        await webhook.delete(delete_after=0.5)

    @command(
        name="gay",
        description="Check how gay you are.",
        aliases=["howgay"]
    )
    async def gay(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to check the gayness of."
        )
    ) -> Message:
        """
        Check how gay you or another member is.
        """
        embed = Embed(
            title=f"**{member.name}** gay rate",
            description=f"**{member.display_name}** is {randint(1, 100)}% gay.",
            color=ctx.author.top_role.color,
        )
        return await ctx.send(embed=embed)
    
    @command(
        name="lesbian",
        description="Check how much of a lesbian you or another member is.",
        aliases=["les", "howlesbian"]
    )
    async def lesbian(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to check the lesbian percentage of."
        )
    ) -> Message:
        """
        Check how much of a lesbian you or another member is.
        """
        embed = Embed(
            title=f"**{member.name}** lesbian rate",
            description=f"**{member.display_name}** is {randint(1, 100)}% lesbian.",
            color=ctx.author.top_role.color,
        )
        return await ctx.send(embed=embed)
    
    @command(
        name="choose",
        description="Choose between two options.",
        aliases=["pick"]
    )
    async def choose(
        self, 
        ctx: Context, 
        *, 
        options: str = parameter(
            default=lambda ctx: ctx.message.content.split(",")[1],
            description="The options to choose between, seperated by a comma."
        )
    ) -> Message:
        """
        Choose between two options, seperated by a comma.
        """
        if len(options) != 2:
            return await ctx.embed(
                message="You must provide two options!",
                message_type="warned",
            )
        
        embed = Embed(
            description=(
                f"I choose **{choice(options.split(','))}**\n"
                f"-# From {', '.join(options.split(','))}"
            ),
            color=ctx.author.top_role.color,
        )

        return await ctx.send(embed=embed)
    
    @group(
        name="vape",
        description="Hit and manage your vape.",
        invoke_without_command=True,
        aliases=["juul"]
    )
    async def vape(
        self, 
        ctx: Context,
    ) -> Message:
        """
        Hit and manage your vape.
        """
        record = await self.bot.pool.fetchrow(
            """
            SELECT * FROM vape 
            WHERE user_id = $1
            """,
            ctx.author.id
        )
        if record is None:
            return await ctx.embed(
                message=(
                    "You don't have a vape!\n"
                    f"-# Use `{ctx.clean_prefix}vape flavor` to set a vape"
                ),
                message_type="no_juul",
            )

        return await ctx.embed(
            message=(
                f"You have **{record['flavor']}** vape\n"
                f"-# You have hit your vape **{record['hits']}** times"
            ),
            message_type="juul",
        )
    
    @vape.command(
        name="hit",
        description="Hit your vape."
    )
    async def vape_hit(
        self,
        ctx: Context,
    ) -> Message:
        """
        Hit your vape.
        """
        record = await self.bot.pool.fetchrow(
            """
            SELECT * FROM vape 
            WHERE user_id = $1
            """,
            ctx.author.id
        )
        if record is None:
            return await ctx.embed(
                message="You don't have a vape!",
                message_type="no_juul",
            )
        
        await self.bot.pool.execute(
            """
            UPDATE vape SET hits = hits + 1 
            WHERE user_id = $1
            """,
            ctx.author.id
        )
        hits = await self.bot.pool.fetchrow(
            """
            SELECT * FROM vape 
            WHERE user_id = $1
            """,
            ctx.author.id
        )
        juul = await ctx.embed(
            message="Hitting your vape...",
            message_type="juul",
        )
        await asyncio.sleep(1)
        await ctx.embed(
            message=(
                f"Hit your **{record['flavor']}** vape\n"
                f"-# You have hit your vape **{hits['hits']}** times"
            ),
            message_type="juul",
            edit=juul
        )

    @vape.command(
        name="flavor", 
        aliases=["flavour", "set"],
        description="Set your vape flavor."
    )
    @cooldown(1, 5, BucketType.member)
    async def vape_flavor(
        self, 
        ctx: Context, 
        *, 
        flavor: str
    ) -> Message:
        """
        Set your vape flavor.
        """
        flavor = flavor.title()
        if flavor not in valid_flavors:
            flavors_list = ", ".join(valid_flavors)
            return await ctx.embed(
                message=f"Invalid flavor. Valid flavors are: {flavors_list}",
                message_type="no_juul",
            )

        await self.bot.pool.execute(
            """
            INSERT INTO vape (user_id, flavor, hits)
            VALUES ($1, $2, 0)
            ON CONFLICT (user_id)
            DO UPDATE SET flavor = $2
            """,
            ctx.author.id,
            flavor,
        )

        return await ctx.embed(
            message=f"Your vape flavor has been set to ``{flavor}``",
            message_type="juul",
        )
    
    @vape.command(
        name="flavors",
        description="View the available vape flavors."
    )
    async def vape_flavors(
        self, 
        ctx: Context,
    ) -> Message:
        """
        View the available vape flavors.
        """
        return await ctx.paginate(
            entries=valid_flavors,
            embed = Embed(
                title="Available Vape Flavors",
                color=ctx.author.top_role.color
            )
        )

    @group(
        name="blunt",
        aliases=["joint"],
        invoke_without_command=True,
        description="Smoke a blunt."
    )
    async def blunt(
        self, 
        ctx: Context,
    ) -> Message:
        """
        Smoke a blunt.
        """
        await ctx.send_help(ctx.command)

    @blunt.command(
        name="light",
        aliases=["broll"],
        description="Light the blunt."
    )
    @cooldown(1, 5, BucketType.member)
    async def blunt_light(
        self, 
        ctx: Context):
        """
        Light the blunt.
        """
        record = await self.bot.pool.fetchrow(
            """
            SELECT * FROM blunt 
            WHERE guild_id = $1
            """,
            ctx.guild.id,
        )
        if record:
            user = ctx.guild.get_member(record.get("user_id"))
            return await ctx.embed(
                message=(
                    f"A blunt is already held by **{user or record.get('user_id')}**\n"
                    f"It has been hit {plural(record.get('hits')):time} by {plural(record.get('members')):member}"
                ),
                message_type="blunt",
            )

        await self.bot.pool.execute(
            """
            INSERT INTO blunt (guild_id, user_id) 
            VALUES($1, $2)
            """,
            ctx.guild.id,
            ctx.author.id,
        )

        blunt = await ctx.embed(
            message="Rolling up a blunt...",
            message_type="blunt",
        )
        await asyncio.sleep(2)
        return await ctx.embed(
            message=(
                "Lit up a blunt.\n"
                f"-# Use `{ctx.prefix}blunt hit` to smoke it"
            ),
            message_type="blunt",
            edit=blunt,
        )

    @blunt.command(
        name="pass", 
        aliases=["give"],
        description="Pass the blunt to another member."
    )
    @cooldown(1, 5, BucketType.member)
    async def blunt_pass(
        self, 
        ctx: Context, 
        *, 
        member: Member = parameter(
            default=lambda ctx: ctx.author,
            description="The member to pass the blunt to."
        )
    ) -> Message:
        """
        Pass the blunt to another member.
        """
        record = await self.bot.pool.fetchrow(
            """
            SELECT * FROM blunt 
            WHERE guild_id = $1
            """,
            ctx.guild.id,
        )

        if not record:
            return await ctx.embed(
                message=(
                    "There is no blunt to pass\n"
                    f"-# Use `{ctx.clean_prefix}blunt light` to roll one up"
                ),
                message_type="blunt",
            )

        if record.get("user_id") != ctx.author.id:
            member = ctx.guild.get_member(record.get("user_id"))
            return await ctx.embed(
                message=(
                    "You don't have the blunt\n"
                    f"-# Steal it from **{member or record.get('user_id')}** first"
                ),
                message_type="blunt",
            )

        if member == ctx.author:
            return await ctx.embed(
                message="You can't pass the blunt to yourself!",
                message_type="blunt",
            )

        await self.bot.pool.execute(
            """
            UPDATE blunt SET user_id = $1, passes = passes + 1 
            WHERE guild_id = $2
            """,
            member.id,
            ctx.guild.id,
        )

        return await ctx.embed(
            message=(
                f"The **blunt** has been passed to **{member}**!\n"
                f"> It has been passed around **{plural(record.get('passes') + 1):time}**"
            ),
            message_type="blunt",
        )

    @cooldown(1, 5, BucketType.member)
    @blunt.command(name="steal", aliases=["take"])
    async def blunt_steal(self, ctx: Context):
        """
        Steal the blunt from another member.
        """
        record = await self.bot.pool.fetchrow(
            """
            SELECT * FROM blunt 
            WHERE guild_id = $1
            """,
            ctx.guild.id,
        )

        if not record:
            return await ctx.embed(
                message=(
                    "There is **no** blunt to steal!\n"
                    f"-# Use `{ctx.clean_prefix}blunt light` to roll one up!"
                ),
                message_type="blunt",
            )

        if record.get("user_id") == ctx.author.id:
            return await ctx.embed(
                message=(
                    "You **already** have the blunt!\n"
                    f"-# Use `{ctx.clean_prefix}blunt pass` to pass it to someone else!"
                ),
                message_type="blunt",
            )

        member = ctx.guild.get_member(record.get("user_id"))

        if randint(1, 100) <= 50:
            return await ctx.embed(
                message=(
                    f"**{member or record.get('user_id')}** is hogging the blunt\n"
                    f"-# Use `{ctx.clean_prefix}blunt pass` to pass it to someone else!"
                ),
                message_type="blunt",
            )

        await self.bot.pool.execute(
            """
            UPDATE blunt SET user_id = $2 
            WHERE guild_id = $1
            """,
            ctx.guild.id,
            ctx.author.id,
        )

        return await ctx.embed(
            message=(
                f"You just stole the **blunt** from **{member or record.get('user_id')}**\n"
                f"-# Use `{ctx.clean_prefix}blunt hit` to smoke it!"
            ),
            message_type="blunt",
        )

    @cooldown(1, 5, BucketType.member)
    @blunt.command(name="hit", aliases=["smoke", "chief"])
    async def blunt_hit(self, ctx: Context):
        """
        Hit the blunt.
        """
        record = await self.bot.pool.fetchrow(
            """
            SELECT * FROM blunt 
            WHERE guild_id = $1
            """,
            ctx.guild.id,
        )

        if not record:
            return await ctx.embed(
                message=(
                    "There is **no** blunt to hit!\n"
                    f"-# Use `{ctx.clean_prefix}blunt light` to roll one up!"
                ),
                message_type="blunt",
            )

        if record.get("user_id") != ctx.author.id:
            member = ctx.guild.get_member(record.get("user_id"))
            return await ctx.embed(
                message=(
                    "You don't have the blunt!\n"
                    f"-# Use `{ctx.clean_prefix}blunt pass` to pass it to someone else!"
                    f"-# Steal it from **{member or record.get('user_id')}**!"
                ),
                message_type="blunt",
            )

        members = record.get("members", [])
        if ctx.author.id not in members:
            members.append(ctx.author.id)

        blunt = await ctx.embed(
            message="Hitting the blunt..",
            message_type="blunt",
        )

        async with ctx.typing():
            await asyncio.sleep(randint(1, 2))

            if (
                record["hits"] + 1 >= 10
                and randint(1, 100) <= 25
            ):
                await self.bot.pool.execute(
                    """
                    DELETE FROM blunt 
                    WHERE guild_id = $1
                    """,
                    ctx.guild.id,
                )

                await ctx.embed(
                    message=(
                        f"The **blunt** burned out after {plural(record.get('hits') + 1):hit} by"
                        f" **{plural(len(members)):member}**"
                    ),
                    message_type="blunt",
                    edit=blunt,
                )

            await self.bot.pool.execute(
                """
                UPDATE blunt SET hits = hits + 1, members = $2 
                WHERE guild_id = $1
                """,
                ctx.guild.id,
                members,
            )

        return await ctx.embed(
            message=(
                "You just hit the blunt!\n"
                f"-# It has been hit **{plural(record.get('hits') + 1):time}** by"
                f" **{plural(len(members)):member}**"
            ),
            message_type="blunt",
            edit=blunt,
        )

async def setup(bot: Vesta):
    await bot.add_cog(Fun(bot))