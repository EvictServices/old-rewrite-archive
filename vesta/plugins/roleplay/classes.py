from discord import (
    Embed,
    Member,
    Message,
    File
)

from yarl import URL
from aiohttp import ClientSession, TCPConnector
from typing import Optional, cast
from logging import getLogger
from random import randint

from .actions import ACTIONS
from vesta.framework import Context, Vesta
from vesta.framework.tools import dominant_color
from vesta.framework.tools.utilities import ordinal

log = getLogger("vesta/roleplay")

BASE_URL = URL.build(
    scheme="https", 
    host="nekos.best"
)

class RoleplaySend:
    """
    Class to handle sending requests to the Neko API and formatting the response as an embed.
    """
    def __init__(self, bot: Vesta):
        self.bot = bot

    async def send_nekos(
        self,
        ctx: Context,
        member: Optional[Member],
        category: str,
    ) -> Message:
        """
        Dispatches a request to the Neko API and sends the response as an embed.
        """
        url = BASE_URL.with_path(f"/api/v2/{category}")

        async with ClientSession(connector=TCPConnector()) as session:
            async with session.get(url, proxy="http://127.1:40000") as response:
                try:
                    data = await response.json()
                    if not data.get("results"):
                        log.error(f"API returned no results: {await response.text()}")
                        return await ctx.embed(
                            message="Something went wrong, please try again later!",
                            message_type="warned",
                        )

                except Exception as e:
                    log.error(f"Failed to parse API response: {str(e)} | Status: {response.status} | Body: {await response.text()}")
                    return await ctx.embed(
                        message="Something went wrong, please try again later!",
                        message_type="warned",
                    )

                if member and member != ctx.author:
                    amount = cast(
                        int,
                        await self.bot.pool.fetchval(
                            """
                            INSERT INTO roleplay (user_id, target_id, category)
                            VALUES ($1, $2, $3)
                            ON CONFLICT (user_id, target_id, category)
                            DO UPDATE SET amount = roleplay.amount + 1
                            RETURNING amount
                            """,
                            ctx.author.id,
                            member.id,
                            category,
                        ),
                    )

                if (
                    member is not None
                    and member != ctx.author
                ):
                    avatar = await ctx.author.display_avatar.read()
                    embed = Embed(color=await dominant_color(avatar))
                    if member != ctx.author:
                        embed.description = (
                        f"{ctx.author.mention} just **{ACTIONS[category]}** {member.display_name}"
                        + (
                            f" for the **{ordinal(amount)}** time"
                            if member != ctx.author
                            and amount
                            else ""
                        )
                    )

                embed.set_author(
                    name=ctx.author.display_name,
                    icon_url=ctx.author.display_avatar,
                )
                embed.set_image(url=data["results"][0]["url"])
                return await ctx.send(embed=embed)

    async def cf_send(
        self,
        ctx: Context,
        member: Optional[Member],
        category: str,
    ) -> Message:
        """
        Dispatches a request to Cloudflare R2 bucket and sends the response as an embed.
        """
        if category == "fuck":
            dir = f"/root/cdn.evict.bot/cdn_root/images/roleplay/{category}/{category}{randint(1, 11)}.gif"
        
        elif category == "nutkick":
            dir = f"/root/cdn.evict.bot/cdn_root/images/roleplay/{category}/{category}{randint(1, 8)}.gif"
        
        elif category == "spank":
            dir = f"/root/cdn.evict.bot/cdn_root/images/roleplay/{category}/{category}{randint(1, 13)}.gif"

        with open(dir, 'rb') as f:
            if member and member != ctx.author:
                amount = cast(
                    int,
                    await self.bot.pool.fetchval(
                        """
                        INSERT INTO roleplay (user_id, target_id, category)
                        VALUES ($1, $2, $3)
                        ON CONFLICT (user_id, target_id, category)
                        DO UPDATE SET amount = roleplay.amount + 1
                        RETURNING amount
                        """,
                        ctx.author.id,
                        member.id,
                        category,
                    ),
                )

                if member and member != ctx.author:
                    avatar = await ctx.author.display_avatar.read()
                    embed = Embed(color=await dominant_color(avatar))
                    embed.description = (
                        f"{ctx.author.mention} just **{ACTIONS[category]}** {member.display_name}"
                        + (
                            f" for the **{ordinal(amount)}** time"
                            if member != ctx.author and amount
                            else ""
                        )
                    )

                    embed.set_author(
                        name=ctx.author.display_name,
                        icon_url=ctx.author.display_avatar,
                    )
                    embed.set_image(url=f"attachment://{category}.gif")
                    return await ctx.send(embed=embed, file=File(f, f"{category}.gif"))