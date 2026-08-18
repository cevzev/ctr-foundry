# travel_assistant/main.py — Python entry point that hosts TravelBuddy: it creates
from tools import convert_currency, get_local_time, get_weather
# the Foundry model client, defines the agent, and starts the Responses server.
# Complete the one TODO inside main() below.
import os

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import ResponsesHostServer
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv(override=True)


def main() -> None:
    # Foundry model client, built from your .env settings.
    client = FoundryChatClient(
        project_endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        credential=DefaultAzureCredential(),
    )

    tools = [
        get_weather,        # <-- kept from Step 2
        get_local_time,     # <-- kept from Step 2
        convert_currency,   # <-- kept from Step 2
        client.get_mcp_tool(                          # <-- add this entry
            name=os.environ["MCP_SERVER_LABEL"],
            url=os.environ["MCP_SERVER_URL"],
            approval_mode="never_require",
        ),
    ]

    # TODO: write TravelBuddy's system instructions. Describe a friendly travel
    # assistant that gives practical, concise trip-planning advice — local context,
    # budget awareness, and safety-minded tips.
    agent = Agent(
        client=client,
        name="travel-buddy",
        instructions=(
            # ... keep your Step 2 instructions here, unchanged ...
            "Use the OctoTrip Flights MCP server when the traveler asks about "
            "flights, routes, fares, or schedules; pass IATA airport codes and a "
            "departure date (YYYY-MM-DD) — if the traveler doesn't give one, call "
            "get_local_time and use the date part of its iso_time as today's date — "
            "and summarize the options you find."
        ),
        tools=tools,        # <-- the list you just extended above
        default_options={"store": False},
    )

    ResponsesHostServer(agent).run()


if __name__ == "__main__":
    main()
