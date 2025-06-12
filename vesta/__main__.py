import logging
import argparse
import asyncio
import os
import psutil

from cashews import cache
from os import getenv, environ
from contextlib import suppress

from vesta.framework import Vesta
from vesta.shared.config import Configuration

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("vesta.log"),
    ],
)

logger = logging.getLogger("vesta")

process = psutil.Process(os.getpid())
logger.info(
    f"Starting Vesta process with PID: {os.getpid()} [Parent: {process.ppid()}]"
)

redis_url = getenv("REDIS_URL", "redis://localhost:6379")
logger.info(f"Setting up cashews cache with Redis URL: {redis_url}")
try:
    cache.setup(redis_url, 
                client_side={"socket_timeout": 30.0},
                client_name="vesta-cashews")
    logger.info("Successfully initialized cashews cache with Redis")

except Exception as e:
    logger.error(f"Failed to setup cashews cache: {e}")
    logger.warning("Falling back to memory cache")
    cache.setup("mem://")

# cache.setup("mem://")

environ["JISHAKU_NO_UNDERSCORE"] = "True"
environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
environ["JISHAKU_HIDE"] = "True"
environ["JISHAKU_FORCE_PAGINATOR"] = "True"
environ["JISHAKU_RETAIN"] = "True"


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--shard-start", type=int, required=True
    )
    parser.add_argument(
        "--shard-end", type=int, required=True
    )
    parser.add_argument(
        "--shard-count", type=int, required=True
    )
    parser.add_argument(
        "--protocol", type=str, default="http"
    )
    parser.add_argument(
        "--host", type=str, default="0.0.0.0"
    )
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument(
        "--cluster-id", type=int, required=True
    )
    args = parser.parse_args()

    logger.info(f"Starting bot with cluster_id={args.cluster_id}, port={args.port}")
    
    bot = Vesta(
        Configuration(),
        port=args.port,
        cluster_id=args.cluster_id,
        shard_ids=list(
            range(args.shard_start, args.shard_end + 1)
        ),
        shard_count=args.shard_count,
    )

    async with bot:
        await bot.start()


if __name__ == "__main__":
    with (
        suppress(
            RuntimeError,
            KeyboardInterrupt,
            ProcessLookupError,
        ),
    ):
        asyncio.run(main())
