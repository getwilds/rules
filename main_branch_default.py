from ghapi.all import GhApi
from rich.console import Console

from registry import WildsRegistry

console = Console(force_terminal=True)
api = GhApi()
reg = WildsRegistry()


def check_for_main(repo):
    """Returns 0 if rule satisfied, 1 if not satisfied"""
    repo_gh = api.repos.get("getwilds", repo["name"])
    default = repo_gh["default_branch"]
    if "main" != default:
        console.print(
            f"[bold red]{repo['name']}[/bold red] needs a main branch as default; instead got {default}"
        )
        return 1
    else:
        console.print(f"[bold green]{repo['name']}[/bold green] all good")
        return 0


if __name__ == "__main__":
    out = [check_for_main(repo) for repo in reg.all]
    if sum(out) > 0:
        raise Exception("at least 1 repo did not satisfy rule, see above")
