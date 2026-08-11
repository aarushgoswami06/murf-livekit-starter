import asyncio
import os

from dotenv import load_dotenv
from livekit import api

load_dotenv(".env.local")


async def main():
    url = os.getenv("LIVEKIT_URL")
    api_key = os.getenv("LIVEKIT_API_KEY")
    api_secret = os.getenv("LIVEKIT_API_SECRET")
    trunk_id = os.getenv("SIP_OUTBOUND_TRUNK_ID")

    print("LIVEKIT_URL:", url)
    print("TRUNK_ID:", trunk_id)

    if not url:
        raise RuntimeError("LIVEKIT_URL is missing")

    if not api_key:
        raise RuntimeError("LIVEKIT_API_KEY is missing")

    if not api_secret:
        raise RuntimeError("LIVEKIT_API_SECRET is missing")

    if not trunk_id:
        raise RuntimeError("SIP_OUTBOUND_TRUNK_ID is missing")

    lk = api.LiveKitAPI(
        url=url,
        api_key=api_key,
        api_secret=api_secret,
    )

    try:
        result = await lk.sip.list_sip_outbound_trunk(
    api.ListSIPOutboundTrunkRequest()
)

        print("\n========== OUTBOUND SIP TRUNKS ==========")

        trunks = result.items

        if not trunks:
            print("No outbound SIP trunks found.")
            return

        for trunk in trunks:
            print("\nTrunk:")
            print(trunk)

            if getattr(trunk, "sip_trunk_id", None) == trunk_id:
                print("\n*** MATCHING TRUNK FOUND ***")
                print(trunk)

        print("\n=========================================")

    finally:
        await lk.aclose()


if __name__ == "__main__":
    asyncio.run(main())