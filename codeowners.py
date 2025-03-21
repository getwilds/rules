import base64
import re

from fastcore import net
from ghapi.all import GhApi
from rich.console import Console

from registry import WildsRegistry

console = Console(force_terminal=True)
api = GhApi()
reg = WildsRegistry()


def check_for_codeowners(repo):
    """Returns 0 if rule satisfied, 1 if not satisfied"""

    badge_status = repo["badge_status"]
    if badge_status not in ["prototype", "stable"]:
        console.print(
            (
                f"[bold yellow]{repo['name']}[/bold yellow] does not need a"
                f"CODEOWNERS file, badge status [u]{badge_status}[/u]"
            )
        )
        return 0

    try:
        codeowners = api.repos.get_content(
            "getwilds", repo["name"], ".github/CODEOWNERS"
        )
    except net.HTTP404NotFoundError:
        console.print(
            (
                f"[bold red]{repo['name']}[/bold red] does not have a CODEOWNERS file"
                f"badge status [u]{badge_status}[/u]"
            )
        )
        return 1

    codeowners_str = base64.b64decode(codeowners["content"]).decode("utf-8")
    users = re.findall(r"@(\w+)", codeowners_str)

    if len(users) < 2:
        console.print(
            f"[bold red]{repo['name']}[/bold red] needs 2-3 codeowners; instead got {len(users)}"
        )
        return 1
    else:
        console.print(
            f"[bold green]{repo['name']}[/bold green] all good, CODEOWNERS file found"
        )
        return 0


if __name__ == "__main__":
    console.print("Checking codeowners...")
    out = [check_for_codeowners(repo) for repo in reg.all]
    if sum(out) > 0:
        raise Exception("at least 1 repo did not satisfy rule, see above")
