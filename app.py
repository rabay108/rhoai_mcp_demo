import os
import re
from mcp.server.mcpserver import MCPServer

# Initialize FastMCP on 0.0.0.0:8080 for OpenShift Pod networking
mcp = MCPServer(name="SportsEventGreetingServer")

# Top 10 major sports events mapped to specialized greetings
TOP_10_SPORTS_GREETINGS: dict[str, str] = {
    "olympics": (
        "Welcome to the Olympic Games! Where the world's greatest athletes unite "
        "under the Olympic flame in pursuit of faster, higher, stronger — together."
    ),
    "wimbledon": (
        "Welcome to The Championships, Wimbledon! Enjoy world-class grass-court tennis, "
        "strawberries and cream, and timeless sporting tradition at SW19."
    ),
    "icc cricket world cup": (
        "Welcome to the ICC Cricket World Cup! Get ready for electrifying sixes, "
        "nail-biting finishes, and the pinnacle of international cricket."
    ),
    "super bowl": (
        "Welcome to the Super Bowl! Experience championship gridiron football, "
        "unforgettable halftime entertainment, and the battle for the Vince Lombardi Trophy."
    ),
    "fifa world cup": (
        "Welcome to the FIFA World Cup! Join billions of fans across the globe "
        "celebrating the beautiful game on football's grandest stage."
    ),
    "uefa champions league final": (
        "Welcome to the UEFA Champions League Final! European club football's elite "
        "clash under the floodlights for the iconic big-eared trophy."
    ),
    "tour de france": (
        "Bienvenue au Tour de France! Witness extraordinary endurance across iconic "
        "mountain climbs and sprint stages in the battle for the Yellow Jersey."
    ),
    "the masters": (
        "Welcome to The Masters Tournament at Augusta National! Step onto the hallowed "
        "fairways and Amen Corner in pursuit of the legendary Green Jacket."
    ),
    "nba finals": (
        "Welcome to the NBA Finals! Where basketball's brightest superstars compete "
        "on the hardwood for the Larry O'Brien Championship Trophy."
    ),
    "formula 1 monaco grand prix": (
        "Welcome to the Formula 1 Monaco Grand Prix! Feel the roar of precision engineering "
        "through the legendary street circuit of Monte Carlo."
    ),
}

# Common shorthand aliases -> canonical key in TOP_10_SPORTS_GREETINGS
EVENT_ALIASES: dict[str, str] = {
    "olympic games": "olympics",
    "summer olympics": "olympics",
    "winter olympics": "olympics",
    "cricket world cup": "icc cricket world cup",
    "icc world cup": "icc cricket world cup",
    "superbowl": "super bowl",
    "world cup": "fifa world cup",
    "champions league": "uefa champions league final",
    "champions league final": "uefa champions league final",
    "masters": "the masters",
    "masters tournament": "the masters",
    "monaco gp": "formula 1 monaco grand prix",
    "monaco grand prix": "formula 1 monaco grand prix",
    "f1 monaco": "formula 1 monaco grand prix",
}


def _normalize(text: str) -> str:
    cleaned = re.sub(r"[^a-z0-9\s]", " ", text.lower())
    return re.sub(r"\s+", " ", cleaned).strip()


@mcp.tool()
def get_sports_event_greeting(event_name: str) -> str:
    """
    Call this tool ONCE per user request and immediately return its output to the user
    without calling this tool again.    
    Returns a specialized welcome greeting for top global sports events
    (Olympics, Wimbledon, ICC Cricket World Cup, Super Bowl, FIFA World Cup,
    UEFA Champions League Final, Tour de France, The Masters, NBA Finals,
    Formula 1 Monaco Grand Prix), or a generic welcome message for any other event.

    Args:
        event_name: The name of the sports event (e.g., "Wimbledon", "Superbowl", "US Open").
    """
    normalized = _normalize(event_name)
    canonical = EVENT_ALIASES.get(normalized, normalized)

    if canonical in TOP_10_SPORTS_GREETINGS:
        return TOP_10_SPORTS_GREETINGS[canonical]

    display_name = event_name.strip() or "the Sports Event"
    return (
        f"Welcome to {display_name}! We are thrilled to have you join us "
        f"for an exciting celebration of sportsmanship and competition."
    )

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8080")),
    )
