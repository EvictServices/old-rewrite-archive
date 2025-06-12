from discord import (
    Member, 
    Message, 
    DMChannel, 
    app_commands,
    User,
)
from discord.ext.commands import (
    Cog,
    command,
    BucketType,
    cooldown,
    has_permissions,
    hybrid_group,
    parameter,
    hybrid_command,
    CheckFailure
)

from typing import Optional, Union
from cashews import cache

from .classes import RoleplaySend
from vesta.framework import Vesta, Context

class Roleplay(Cog):
    def __init__(self, bot: Vesta):
        """
        Interact with other users.
        """
        self.bot = bot
        self.description = "Perform different actions on other members."

    @cache(
        ttl="1h",
        key="roleplay_enabled:{guild_id}"
    )
    async def get_config(self, guild_id: int) -> bool:
        """
        Get the roleplay configuration for a guild.
        """
        record = await self.bot.pool.fetchval(
            """
            SELECT enabled
            FROM roleplay_enabled
            WHERE guild_id = $1
            """,
            guild_id,
        )
        return bool(record) if record is not None else False
    
    async def cog_before_invoke(self, ctx: Context):
        """
        Check if roleplay commands are enabled for the guild.
        """
        if ctx.guild is None:
            return
        
        if ctx.command in (
            self.roleplay,
            self.actions_group,
        ):
            return
        
        config = await self.get_config(ctx.guild.id)
        if not config:
            raise CheckFailure("Roleplay commands **are not enabled** for this server!")

    @hybrid_command(
        name="roleplay",
        description="Enable or disable roleplay commands for the guild."
    )
    @has_permissions(manage_guild=True)
    async def roleplay(
        self, 
        ctx: Context, 
        enabled: bool = parameter(
            default=True,
            description="Whether to enable or disable roleplay commands for the guild."
        )
    ):
        """
        Enable or disable roleplay commands for the guild.
        """
        config = await self.get_config(ctx.guild.id)
        if config == enabled:
            return await ctx.embed(
                message=f"Roleplay commands are already **{'enabled' if enabled else 'disabled'}** for this server!",
                message_type="warned",
            )
            
        await self.bot.pool.execute(
            """
            INSERT INTO roleplay_enabled (guild_id, enabled)
            VALUES ($1, $2)
            ON CONFLICT (guild_id)
            DO UPDATE SET enabled = EXCLUDED.enabled
            """,
            ctx.guild.id,
            enabled,
        )
        
        await cache.delete(f"roleplay_enabled:{ctx.guild.id}")
        await self.get_config(ctx.guild.id)
        
        return await ctx.embed(
            message=f"Roleplay commands have been **{'enabled' if enabled else 'disabled'}** for this server",
            message_type="approved",
        )

    @command(
        name="slap",
        description="Slap someone."
    )
    @cooldown(1, 1, BucketType.member)
    async def slap(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to slap."
        )
    ) -> Message:
        """
        Slap someone.
        """
        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, member=member, category=ctx.command.name
        )

    @command(
        name="hug",
        description="Hug someone."
    )
    @cooldown(1, 1, BucketType.member)
    async def hug(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to hug."
        )
    ) -> Message:
        """
        Hug someone.
        """
        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, member=member, category=ctx.command.name
        )

    @command(
        name="kiss",
        description="Kiss someone."
    )
    @cooldown(1, 1, BucketType.member)
    async def kiss(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to kiss."
        )
    ) -> Message:
        """
        Kiss someone.
        """
        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, member=member, category=ctx.command.name
        )

    @command(
        name="pat",
        description="Pat someone."
    )
    @cooldown(1, 1, BucketType.member)
    async def pat(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to pat."
        )
    ) -> Message:
        """
        Pat someone.
        """
        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, member=member, category=ctx.command.name
        )

    @command(
        name="tickle",
        description="Tickle someone."
    )
    @cooldown(1, 1, BucketType.member)
    async def tickle(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to tickle."
        )
    ) -> Message:
        """
        Tickle someone.
        """
        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, member=member, category=ctx.command.name
        )

    @command(
        name="feed",
        description="Feed someone."
    )
    @cooldown(1, 1, BucketType.member)
    async def feed(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to feed."
        )
    ) -> Message:
        """
        Feed someone.
        """
        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, member=member, category=ctx.command.name
        )

    @command(
        name="punch",
        description="Punch someone."
    )
    @cooldown(1, 1, BucketType.member)
    async def punch(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to punch."
        )
    ) -> Message:
        """
        Punch someone.
        """
        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, member=member, category=ctx.command.name
        )

    @command(
        name="highfive",
        description="Highfive someone."
    )
    @cooldown(1, 1, BucketType.member)
    async def highfive(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to highfive."
        )
    ) -> Message:
        """
        Highfive someone.
        """
        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, member=member, category=ctx.command.name
        )

    @command(
        name="bite",
        description="Bite someone."
    )
    @cooldown(1, 1, BucketType.member)
    async def bite(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to bite."
        )
    ) -> Message:
        """
        Bite someone.
        """
        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, member=member, category=ctx.command.name
        )

    @command(
        name="shoot",
        description="Shoot someone."
    )
    @cooldown(1, 1, BucketType.member)
    async def shoot(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to shoot."
        )
    ) -> Message:
        """
        Shoot someone.
        """
        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, member=member, category=ctx.command.name
        )

    @command(
        name="wave",
        description="Wave to someone."
    )
    @cooldown(1, 1, BucketType.member)
    async def wave(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to wave to."
        )
    ) -> Message:
        """
        Wave to someone.
        """
        return await RoleplaySend.send_nekos(
            self, ctx, member, ctx.command.name
        )

    @command(
        name="happy",
        description="Be happy with someone."
    )
    @cooldown(1, 1, BucketType.member)
    async def happy(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to be happy with."
        )
    ) -> Message:
        """
        Be happy with someone.
        """
        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, member=member, category=ctx.command.name
        )

    @command(
        name="peck",
        description="Peck someone."
    )
    @cooldown(1, 1, BucketType.member)
    async def peck(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to peck."
        )
    ) -> Message:
        """
        Peck someone.
        """
        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, member=member, category=ctx.command.name
        )

    @command(
        name="lurk",
        description="Lurk at someone."
    )
    @cooldown(1, 1, BucketType.member)
    async def lurk(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to lurk at."
        )
    ) -> Message:
        """
        Lurk at someone.
        """
        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, member=member, category=ctx.command.name
        )

    @command(
        name="sleep",
        description="Sleep with someone."
    )
    @cooldown(1, 1, BucketType.member)
    async def sleep(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to sleep with."
        )
    ) -> Message:
        """
        Sleep with someone.
        """
        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, member=member, category=ctx.command.name
        )

    @command(
        name="wink",
        description="Wink at someone."
    )
    @cooldown(1, 1, BucketType.member)
    async def wink(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to wink at."
        )
    ) -> Message:
        """
        Wink at someone.
        """
        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, member=member, category=ctx.command.name
        )

    @command(
        name="dance",
        description="Dance with someone."
    )
    @cooldown(1, 1, BucketType.member)
    async def dance(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to dance with."
        )
    ) -> Message:
        """
        Dance with someone.
        """
        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, member=member, category=ctx.command.name
        )

    @command(
        name="yawn",
        description="Yawn at someone."
    )
    @cooldown(1, 1, BucketType.member)
    async def yawn(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to yawn at."
        )
    ) -> Message:
        """
        Yawn at someone.
        """

        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, member=member, category=ctx.command.name
        )

    @command(
        name="nom",
        description="Nom someone."
    )
    @cooldown(1, 1, BucketType.member)
    async def nom(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to nom."
        )
    ) -> Message:
        """
        Nom someone.
        """
        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, member=member, category=ctx.command.name
        )
    
    @command(
        name="yeet",
        description="Yeet someone."
    )
    @cooldown(1, 1, BucketType.member)
    async def yeet(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to yeet."
        )
    ) -> Message:
        """
        Yeet someone.
        """
        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, member=member, category=ctx.command.name
        )

    @command(
        name="think",
        description="Think about someone."
    )
    @cooldown(1, 1, BucketType.member)
    async def think(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to think about."
        )
    ) -> Message:
        """
        Think about someone.
        """
        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, member=member, category=ctx.command.name
        )

    @command(
        name="bored",
        description="Be bored with someone."
    )
    @cooldown(1, 1, BucketType.member)
    async def bored(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to be bored with."
        )
    ) -> Message:
        """
        Be bored with someone.
        """
        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, member=member, category=ctx.command.name
        )

    @command(
        name="blush",
        description="Blush at someone."
    )
    @cooldown(1, 1, BucketType.member)
    async def blush(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to blush at."
        )
    ) -> Message:
        """
        Blush at someone.
        """
        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, member=member, category=ctx.command.name
        )

    @command(
        name="stare",
        description="Stare at someone."
    )
    @cooldown(1, 1, BucketType.member)
    async def stare(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to stare at."
        )
    ) -> Message:
        """
        Stare at someone.
        """
        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, member=member, category=ctx.command.name
        )

    @command(
        name="nod",
        description="Nod at someone."
    )
    @cooldown(1, 1, BucketType.member)
    async def nod(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to nod at."
        )
    ) -> Message:
        """
        Nod at someone.
        """
        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, member=member, category=ctx.command.name
        )

    @command(
        name="handhold",
        description="Hold hands with someone."
    )
    @cooldown(1, 1, BucketType.member)
    async def handhold(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to hold hands with."
        )
    ) -> Message:
        """
        Hold hands with someone.
        """
        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, member=member, category=ctx.command.name
        )

    @command(
        name="smug",
        description="Smug at someone."
    )
    @cooldown(1, 1, BucketType.member)
    async def smug(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to smug at."
        )
    ) -> Message:
        """
        Smug at someone.
        """
        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, member=member, category=ctx.command.name
        )

    @command(
        name="fuck",
        description="Fuck someone."
    )
    @cooldown(1, 1, BucketType.member)
    async def fuck(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to fuck."
        )
    ) -> Message:
        """
        Fuck someone.
        """
        return await RoleplaySend.cf_send(
            self=self, ctx=ctx, member=member, category=ctx.command.name
        )

    @command(
        name="spank",
        description="Spank someone."
    )
    @cooldown(1, 1, BucketType.member)
    async def spank(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to spank."
        )
    ) -> Message:
        """
        Spank someone.
        """
        return await RoleplaySend.cf_send(
            self=self, ctx=ctx, member=member, category=ctx.command.name
        )

    @command(
        name="nutkick",
        description="Nutkick someone."
    )
    @cooldown(1, 1, BucketType.member)
    async def nutkick(
        self, 
        ctx: Context, 
        member: Optional[Member] = parameter(
            default=lambda ctx: ctx.author,
            description="The member to nutkick."
        )
    ) -> Message:
        """
        Nutkick someone.
        """
        return await RoleplaySend.cf_send(
            self=self, ctx=ctx, member=member, category=ctx.command.name
        )

    @hybrid_group(
        name="actions",
        description="Perform different actions on other members.",
        with_app_command=True,
        invoke_without_command=True
    )
    @app_commands.allowed_installs(guilds=False, users=True)
    @app_commands.allowed_contexts(guilds=False, dms=True, private_channels=True)
    @app_commands.default_permissions(use_application_commands=True)
    async def actions_group(self, ctx: Context):
        """
        Roleplay commands for DMs.
        """
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @actions_group.command(
        name="fuck",
        description="Fuck someone."
    )
    async def roleplay_fuck(
        self, 
        ctx: Context, 
        user: Union[Member, User, None] = parameter(
            default=lambda ctx: ctx.author,
            description="Fuck a user."
        )
    ) -> Message:
        """
        Fuck someone (DMs only).
        """
        if not isinstance(ctx.channel, DMChannel):
            return await ctx.embed(
                message="This command can only be used in DMs!",
                message_type="warned"
            )

        return await RoleplaySend.cf_send(
            self=self, ctx=ctx, user=user, category=ctx.command.name
        )

    @actions_group.command(
        name="spank",
        description="Spank someone."
    )
    async def actions_spank(
        self, 
        ctx: Context, 
        user: Union[Member, User, None] = parameter(
            default=lambda ctx: ctx.author,
            description="Spank a user."
        )
    ) -> Message:
        """
        Spank someone (DMs only).
        """
        if not isinstance(ctx.channel, DMChannel):
            return await ctx.embed(
                message="This command can only be used in DMs!",
                message_type="warned"
            )

        return await RoleplaySend.cf_send(
            self=self, ctx=ctx, user=user, category=ctx.command.name
        )

    @actions_group.command(
        name="nutkick",
        description="Nutkick someone."
    )
    async def actions_nutkick(
        self, 
        ctx: Context, 
        user: Union[Member, User, None] = parameter(
            default=lambda ctx: ctx.author,
            description="Nutkick a user."
        )
    ) -> Message:
        """
        Nutkick someone (DMs only).
        """
        if not isinstance(ctx.channel, DMChannel):
            return await ctx.embed(
                message="This command can only be used in DMs!",
                message_type="warned"
            )

        return await RoleplaySend.cf_send(
            self=self, ctx=ctx, user=user, category=ctx.command.name
        )


    @actions_group.command(
        name="bite",
        description="Bite someone."
    )
    async def actions_bite(
        self, 
        ctx: Context, 
        user: Union[Member, User, None] = parameter(
            default=lambda ctx: ctx.author,
            description="Bite a user."
        )
    ) -> Message:
        """
        Bite someone (DMs only).
        """
        if not isinstance(ctx.channel, DMChannel):
            return await ctx.embed(
                message="This command can only be used in DMs!",
                message_type="warned"
            )

        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, user=user, category=ctx.command.name
        )

    @actions_group.command(
        name="cuddle",
        description="Cuddle someone."
    )
    async def actions_cuddle(
        self, 
        ctx: Context, 
        user: Union[Member, User, None] = parameter(
            default=lambda ctx: ctx.author,
            description="Cuddle a user."
        )
    ) -> Message:
        """
        Cuddle someone (DMs only).
        """
        if not isinstance(ctx.channel, DMChannel):
            return await ctx.embed(
                message="This command can only be used in DMs!",
                message_type="warned"
            )

        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, user=user, category=ctx.command.name
        )

    @actions_group.command(
        name="poke",
        description="Poke someone."
    )
    async def actions_poke(
        self, 
        ctx: Context, 
        user: Union[Member, User, None] = parameter(
            default=lambda ctx: ctx.author,
            description="Poke a user."
        )
    ) -> Message:
        """
        Poke someone (DMs only).
        """
        if not isinstance(ctx.channel, DMChannel):
            return await ctx.embed(
                message="This command can only be used in DMs!",
                message_type="warned"
            )

        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, user=user, category=ctx.command.name
        )

    @actions_group.command(
        name="kiss",
        description="Kiss someone."
    )
    async def actions_kiss(
        self, 
        ctx: Context, 
        user: Union[Member, User, None] = parameter(
            default=lambda ctx: ctx.author,
            description="Kiss a user."
        )
    ) -> Message:
        """
        Kiss someone (DMs only).
        """
        if not isinstance(ctx.channel, DMChannel):
            return await ctx.embed(
                message="This command can only be used in DMs!",
                message_type="warned"
            )

        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, user=user, category=ctx.command.name
        )

    @actions_group.command(
        name="hug",
        description="Hug someone."
    )
    async def actions_hug(
        self, 
        ctx: Context, 
        user: Union[Member, User, None] = parameter(
            default=lambda ctx: ctx.author,
            description="Hug a user."
        )
    ) -> Message:
        """
        Hug someone (DMs only).
        """
        if not isinstance(ctx.channel, DMChannel):
            return await ctx.embed(
                message="This command can only be used in DMs!",
                message_type="warned"
            )

        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, user=user, category=ctx.command.name
        )

    @actions_group.command(
        name="pat",
        description="Pat someone."
    )
    async def actions_pat(
        self, 
        ctx: Context, 
        user: Union[Member, User, None] = parameter(
            default=lambda ctx: ctx.author,
            description="Pat a user."
        )
    ) -> Message:
        """
        Pat someone (DMs only).
        """
        if not isinstance(ctx.channel, DMChannel):
            return await ctx.embed(
                message="This command can only be used in DMs!",
                message_type="warned"
            )

        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, user=user, category=ctx.command.name
        )

    @actions_group.command(
        name="tickle",
        description="Tickle someone."
    )
    async def actions_tickle(
        self, 
        ctx: Context, 
        user: Union[Member, User, None] = parameter(
            default=lambda ctx: ctx.author,
            description="Tickle a user."
        )
    ) -> Message:
        """
        Tickle someone (DMs only).
        """
        if not isinstance(ctx.channel, DMChannel):
            return await ctx.embed(
                message="This command can only be used in DMs!",
                message_type="warned"
            )

        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, user=user, category=ctx.command.name
        )

    @actions_group.command(
        name="lick",
        description="Lick someone."
    )
    async def actions_lick(
        self, 
        ctx: Context, 
        user: Union[Member, User, None] = parameter(
            default=lambda ctx: ctx.author,
            description="Lick a user."
        )
    ) -> Message:
        """
        Lick someone (DMs only).
        """
        if not isinstance(ctx.channel, DMChannel):
            return await ctx.embed(
                message="This command can only be used in DMs!",
                message_type="warned"
            )

        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, user=user, category=ctx.command.name
        )


    @actions_group.command(
        name="slap",
        description="Slap someone."
    )
    async def actions_slap(
        self, 
        ctx: Context, 
        user: Union[Member, User, None] = parameter(
            default=lambda ctx: ctx.author,
            description="Slap a user."
        )
    ) -> Message:
        """
        Slap someone (DMs only).
        """
        if not isinstance(ctx.channel, DMChannel):
            return await ctx.embed(
                message="This command can only be used in DMs!",
                message_type="warned"
            )

        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, user=user, category=ctx.command.name
        )

    @actions_group.command(
        name="punch",
        description="Punch someone."
    )
    async def actions_punch(
        self, 
        ctx: Context, 
        user: Union[Member, User, None] = parameter(
            default=lambda ctx: ctx.author,
            description="Punch a user."
        )
    ) -> Message:
        """
        Punch someone (DMs only).
        """
        if not isinstance(ctx.channel, DMChannel):
            return await ctx.embed(
                message="This command can only be used in DMs!",
                message_type="warned"
            )

        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, user=user, category=ctx.command.name
        )

    @actions_group.command(
        name="shoot",
        description="Shoot someone."
    )
    async def actions_shoot(
        self, 
        ctx: Context, 
        user: Union[Member, User, None] = parameter(
            default=lambda ctx: ctx.author,
            description="Shoot a user."
        )
    ) -> Message:
        """
        Shoot someone (DMs only).
        """
        if not isinstance(ctx.channel, DMChannel):
            return await ctx.embed(
                message="This command can only be used in DMs!",
                message_type="warned"
            )

        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, user=user, category=ctx.command.name
        )

    @actions_group.command(
        name="nom",
        description="Nom someone."
    )
    async def actions_nom(
        self, 
        ctx: Context, 
        user: Union[Member, User, None] = parameter(
            default=lambda ctx: ctx.author,
            description="Nom a user."
        )
    ) -> Message:
        """
        Nom someone (DMs only).
        """
        if not isinstance(ctx.channel, DMChannel):
            return await ctx.embed(
                message="This command can only be used in DMs!",
                message_type="warned"
            )

        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, user=user, category=ctx.command.name
        )

    @actions_group.command(
        name="yeet",
        description="Yeet someone."
    )
    async def actions_yeet(
        self, 
        ctx: Context, 
        user: Union[Member, User, None] = parameter(
            default=lambda ctx: ctx.author,
            description="Yeet a user."
        )
    ) -> Message:
        """
        Yeet someone (DMs only).
        """
        if not isinstance(ctx.channel, DMChannel):
            return await ctx.embed(
                message="This command can only be used in DMs!",
                message_type="warned"
            )

        return await RoleplaySend.send_nekos(
            self=self, ctx=ctx, user=user, category=ctx.command.name
        )

async def setup(bot: "Vesta") -> None:
    await bot.add_cog(Roleplay(bot))
