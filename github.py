import math
import time
from datetime import datetime
from typing import List
from github import Github, RateLimitExceededException
from github.Repository import Repository
# from github.ContentFile import ContentFile
# from github.PaginatedList import PaginatedList
from . import secrets, regex_utils



g = Github(secrets.GITHUB_PERSONAL_ACCESS_TOKEN)



def wait_for_rate_limit_reset() -> None:
    reset_time = g.rate_limiting_resettime + 30
    datetime_stamp = datetime.fromtimestamp(reset_time)
    sleep_seconds = math.floor(reset_time - time.time())
    print("\n\n\n\n\n")
    print(f"GitHub rate limit reached. Sleeping for {sleep_seconds} seconds until {datetime_stamp}")
    print("\n\n\n\n\n")
    time.sleep(sleep_seconds)


# def check_github_rate_limit() -> None:
#     if (g.rate_limiting[0] <= 0):
#         wait_for_rate_limit_reset()


def search_github_repos(query: str):
    try:
        paginatedRepos = g.search_repositories(query=query, sort="updated", order="desc")
        return paginatedRepos
    except RateLimitExceededException as e:
        wait_for_rate_limit_reset()
        return search_github_repos()


def get_folder_contents(repo: Repository, folder_path: str):
    try:
        folder_contents = repo.get_contents(folder_path)
        return folder_contents
    except RateLimitExceededException as e:
        wait_for_rate_limit_reset()
        return get_folder_contents(repo, folder_path)


def get_repo(repo_name: str) -> Repository:
    try:
        repo = g.get_repo(repo_name)
        return repo
    except RateLimitExceededException as e:
        wait_for_rate_limit_reset()
        return get_repo(repo_name)

def is_folder_allow_listed(folder_path: str) -> bool:
    return (not folder_path.startswith(".") and folder_path not in ["ci", "cd", "doc", "docs", "documentation", "images", "git", "gradle", "maven", "idea", "etc", "test", "javadoc", "resources", "scripts"])


def get_all_long_method_names_from_c_like_repo(repo_name: str)  -> List[tuple]:
    all_long_method_names_their_files = []
    try:
        repo = get_repo(repo_name)
        print(f"{g.rate_limiting[0]} GitHub requests remaining")
        contents = get_folder_contents(repo, "")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                if is_folder_allow_listed(file_content.name):
                    print(f"{file_content.path}")
                    contents.extend(get_folder_contents(repo, file_content.path))
            else:
                if file_content.name.endswith(".java"):
                    print(file_content.name)
                    methodNames = regex_utils.get_long_method_names_c_like(file_content.decoded_content.decode("utf-8"))
                    if (len(methodNames) > 0):
                        for method_name in methodNames:
                            all_long_method_names_their_files.append((method_name, file_content.name))
                        # tweet_method_names(methodNames, repo_name, file_content.name)
    except Exception as e:
        print(f"Repo {repo_name} cannot be parsed due to {e}")
    return all_long_method_names_their_files


# def get_all_contents_of_llvm_like_repo_recursively(repo_name):
#     try:
#         repo = g.get_repo(repo_name)
#         contents = repo.get_contents("")
#         while contents:
#             file_content = contents.pop(0)
#             if file_content.type == "dir":
#                 contents.extend(repo.get_contents(file_content.path))
#             else:
#                 if file_content.name.endswith(".java"):
#                     methodNames = regex_utils.get_long_method_names_llvm_like(file_content.decoded_content.decode("utf-8"))
#                     if (len(methodNames) > 0):
#                         tweet_method_names(methodNames, repo_name, file_content.name)
#     except Exception as e:
#         print(f"Repo {repo_name} cannot be parsed due to {e}")