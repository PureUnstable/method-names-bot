import math
import time
from datetime import datetime
from typing import List
from github import Github
from github.Repository import Repository
from github.ContentFile import ContentFile
# from github.PaginatedList import PaginatedList
import secrets, regex_utils


g = Github(secrets.GITHUB_PERSONAL_ACCESS_TOKEN)


def wait_for_rate_limit_reset() -> None:
    reset_time = g.rate_limiting_resettime + 30
    datetime_stamp = datetime.fromtimestamp(reset_time)
    sleep_seconds = math.floor(reset_time - time.time())
    print("\n\n\n\n\n")
    print(f"GitHub rate limit reached. Sleeping for {sleep_seconds} seconds until {datetime_stamp}")
    print("\n\n\n\n\n")
    time.sleep(sleep_seconds)


def search_github_repos(query: str):
    try:
        paginatedRepos = g.search_repositories(query=query, sort="updated", order="desc")
        return paginatedRepos
    except Exception as e:
        if "403" in e.__repr__():
            wait_for_rate_limit_reset()
            return search_github_repos()
        else:
            raise e


def get_contents(repo: Repository, folder_path: str):
    try:
        print(f"{folder_path}")
        folder_contents = repo.get_contents(folder_path)
        return folder_contents
    except Exception as e:
        if "403" in e.__repr__():
            wait_for_rate_limit_reset()
            return get_contents(repo, folder_path)
        else:
            raise e


def get_repo(repo_name: str) -> Repository:
    try:
        repo = g.get_repo(repo_name)
        return repo
    except Exception as e:
        if "403" in e.__repr__():
            wait_for_rate_limit_reset()
            return get_repo(repo_name)
        else:
            raise e


def is_folder_allow_listed(folder_path: str) -> bool:
    return (not folder_path.startswith(".") and folder_path not in ["ci", "cd", "doc", "docs", "documentation", "images", "git", "gradle", "maven", "idea", "etc", "test", "javadoc", "resources", "scripts"])


def get_folder_contents(repo: Repository, folder_name: str, folder_path: str) -> ContentFile:
    if is_folder_allow_listed(folder_name):
        return get_contents(repo, folder_path)
    return None


def is_file_parsable(file_content: ContentFile) -> bool:
    return (file_content.name.endswith(".java") and "src/" in file_content.path)


def get_long_method_names_from_file(file_content: ContentFile) -> List[str]:
    try:
        print(file_content.name)
        method_names = regex_utils.get_long_method_names_c_like(file_content.decoded_content.decode("utf-8"))
        return method_names
    except Exception as e:
        if "403" in e.__repr__():
            wait_for_rate_limit_reset()
            return get_long_method_names_from_file(file_content)
        else:
            raise e


def loop_through_repo_for_long_method_names(contents: List[ContentFile], repo: Repository) -> List[str]:
    all_long_method_names_their_files = []
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            folder_contents = get_folder_contents(repo, file_content.name, file_content.path)
            if folder_contents is not None:
                contents.extend(folder_contents)
        else:
            if is_file_parsable(file_content):
                all_long_method_names_their_files.extend(get_long_method_names_from_file(file_content))
    return all_long_method_names_their_files


def get_all_long_method_names_from_c_like_repo(repo_name: str)  -> List[tuple]:
    all_long_method_names_their_files = []
    try:
        repo = get_repo(repo_name)
        print(f"{g.rate_limiting[0]} GitHub requests remaining")
        contents = get_contents(repo, "")
        all_long_method_names_their_files = loop_through_repo_for_long_method_names(contents, repo)
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