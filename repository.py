# from pygit2 import Repository
from ghapi.all import GhApi
from registry import WildsRegistry
from rich import print
from rich.console import Console
console = Console(force_terminal=True)

api = GhApi()
reg = WildsRegistry()
# repo = reg.all[0]
# repo_gh = api.repos.get("getwilds", repo["name"])
# repo_gh['default_branch']

def check_for_main(repo):
  repo_gh = api.repos.get("getwilds", repo["name"])
  default = repo_gh['default_branch']
  if "main" != default:
    console.print(f'[bold red]{repo["name"]}[/bold red] needs a main branch as default; instead got {default}')
    # raise Exception(f'[bold red]{repo["name"]}[/bold red] needs a main branch as default; instead got {default}')
  else:
    console.print(f"[bold green]{repo["name"]}[/bold green] all good")
  # repo = Repository(".")
  # if "mains" not in list(repo.branches.local):
  #   raise Exception(f'main branch not found for {repo}')

if __name__ == "__main__":
  [check_for_main(repo) for repo in reg.all]

#   repo = Repository(".")
#   check_for_main(repo)
