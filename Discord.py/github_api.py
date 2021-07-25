import requests
from github import Github


async def github_api(github_token):
    GITHUB_TOKEN = github_token
    # end local constants

    g = Github(GITHUB_TOKEN)
    repo = g.get_repo("Puncher1/Testing")

    main_branch = repo.get_branch("main")
    commit = main_branch.commit.commit

    html_url = commit.html_url
    author = commit.author
    message = commit.message
    sha_short = commit.sha[:7]

    string = f"[**[Testing:main] Last commit**](https://github.com/Puncher1/Testing)" \
             f"\n[`{sha_short}`]({html_url}) {message} - {author.name}"

    return string