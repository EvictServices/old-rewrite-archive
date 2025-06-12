from discord.ext.commands import check
from cashews import cache
from typing import TYPE_CHECKING

from .context import Context

if TYPE_CHECKING:
    from vesta.framework import Vesta

def roleplay_enabled():
    """
    Check if roleplay commands are enabled for the guild.
    """
    async def predicate(ctx: Context):
        record = await ctx.bot.pool.fetchval(
            """
            SELECT enabled
            FROM roleplay_enabled
            WHERE guild_id = $1
            """,
            ctx.guild.id,
        )
        if not record:
            await ctx.embed(
                message=(
                    f"Roleplay commands are not enabled for this server!\n"
                    f"-# Enable using `{ctx.clean_prefix}roleplay true`"
                ),
                message_type="warned",
            )
            return False
        return True

    return check(predicate)


def has_economy():
    """
    Check if a user has an economy account.
    """
    async def predicate(ctx: Context):
        record = await ctx.bot.pool.fetchrow(
            """
            SELECT user_id FROM economy 
            WHERE user_id = $1
            """,
            ctx.author.id,
        )
        if not record:
            await ctx.embed(
                message=f"You do not have an economy account! Use `{ctx.clean_prefix}open` to create one!",
                message_type="warned",
            )
            return False
        
        return True

    return check(predicate)


def has_company():
    """
    Check if the user owns a company in the server.
    """
    async def predicate(ctx: Context):
        business = await ctx.bot.pool.fetchrow(
            """
            SELECT 1 FROM businesses 
            WHERE owner_id = $1 AND guild_id = $2
            """,
            ctx.author.id,
            ctx.guild.id,
        )
        if not business:
            await ctx.embed(
                message="You don't own a business here!",
                message_type="warned",
                tip=f"Create one using `{ctx.clean_prefix}business create`",
            )
            
            return False
        
        return True

    return check(predicate)

def jail_enabled():
    """
    Check if the jail system is setup for the guild.
    """
    async def predicate(ctx: Context):
        config = await ctx.bot.pool.fetchrow(
            """
            SELECT * FROM jail.config 
            WHERE guild_id = $1
            """,
            ctx.guild.id,
        )

        if not config:
            await ctx.embed(
                "The jail system is not setup for this server!\n"
                f"-# Use `{ctx.clean_prefix}setup` to configure it.",
                message_type="warned",
            )
            
            return False
        
        return True

    return check(predicate)

@cache(
    ttl="3h",
    key="blacklist:{object_id}:{object_type}",
)
async def is_blacklisted(
    bot: "Vesta", object_id: int, object_type: str
) -> bool:
    """
    Check if a user or guild is blacklisted.
    """
    if object_type == "user":
        query = """
        SELECT 1 FROM blacklist 
        WHERE user_id = $1
        """
    
    elif object_type == "guild":
        query = """
        SELECT 1 FROM guildblacklist 
        WHERE guild_id = $1
        """
    
    else:
        query = """
        SELECT 1 FROM blacklists 
        WHERE object_id = $1 AND object_type = $2
        """
        return bool(
            await bot.pool.fetchval(
                query, object_id, object_type
            )
        )

    return bool(await bot.pool.fetchval(query, object_id))


async def invalidate_blacklist_cache(
    object_id: int, object_type: str
):
    """
    Invalidate the blacklist cache for a given object.
    """
    await cache.delete(f"blacklist:{object_id}:{object_type}")
