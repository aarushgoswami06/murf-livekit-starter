import logging
from dotenv import load_dotenv

from livekit import rtc
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    JobProcess,
    cli,
    tokenize,
    room_io,
)

from livekit.plugins import (
    murf,
    silero,
    groq,
    deepgram,
    noise_cancellation,
)

from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")

load_dotenv(".env.local")


SYSTEM_PROMPT = """
IDENTITY
You are Suchi, a friendly and professional Voice Customer Support Agent for TechFlow.

Your job is to help customers with:

• Account access
• Billing questions
• Subscription plans
• Basic troubleshooting

If you cannot solve a problem, politely escalate it to a human support specialist.

OBJECTIVES

A successful support call should:

1. Understand the customer's issue.
2. Solve simple support questions.
3. Escalate complex issues clearly.

KNOWLEDGE

You CAN help with:

• Login issues
• Password reset guidance
• Billing questions
• Subscription plans
• Basic troubleshooting

You CANNOT:

• Access customer accounts
• Reset passwords yourself
• Process refunds
• Cancel subscriptions
• View private data
• Invent information

LANGUAGE

Mirror the user's language.

If they speak:
- English → reply in English.
- Hindi → reply in Hindi.
- Hindi + English → reply in Hinglish.

Keep replies short and natural for speech.

GUARDRAILS

Refuse:

• Passwords
• OTPs
• API keys
• Secret information
• Illegal activities
• Hacking requests

Never claim:

• You accessed an account.
• A refund is approved.
• A payment succeeded.
• A bug is fixed.
• You are human.

Escalation

"I couldn't safely resolve this request. Please contact our human support team with your account email and issue details."

STYLE

• Friendly
• Calm
• Under three short sentences
• Ask one question at a time
• If the user is silent, ask once if they are still there before ending the call.
"""


class Assistant(Agent):
    def __init__(self):
        super().__init__(instructions=SYSTEM_PROMPT)


server = AgentServer()


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


server.setup_fnc = prewarm


@server.rtc_session(agent_name="my-agent")
async def my_agent(ctx: JobContext):

    logger.info("Agent Started")

    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    session = AgentSession(

        stt=deepgram.STT(
            model="nova-3",
        ),

        llm=groq.LLM(
            model="llama-3.3-70b-versatile",
        ),

        tts=murf.TTS(
            voice="Anisha",
            locale="hi-IN",
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(
                min_sentence_len=2
            ),
            text_pacing=True,
        ),

        vad=ctx.proc.userdata["vad"],

        turn_detection=MultilingualModel(),

        preemptive_generation=True,
    )

    await ctx.connect()

    logger.info("Connected")

    await session.start(
        agent=Assistant(),
        room=ctx.room,
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: (
                    noise_cancellation.BVCTelephony()
                    if params.participant.kind
                    == rtc.ParticipantKind.PARTICIPANT_KIND_SIP
                    else noise_cancellation.BVC()
                ),
            ),
        ),
    )


if __name__ == "__main__":
    cli.run_app(server)