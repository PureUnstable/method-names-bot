import sys
import os
import logging
import time
import github_api, twitter_api


# Logging
LOGGING_FOLDER = "./logs"


# Github API
# Ref: https://docs.github.com/en/rest/reference/search
GITHUB_SEARCH_STRING = "api"
GITHUB_SEARCH_REPO_SIZE = "size:>=20000"
GITHUB_SEARCH_REPO_FILTERS = "sort=updated&order=desc"
GITHUB_SEARCH_REPO_QUERY = f"{GITHUB_SEARCH_STRING} language:java {GITHUB_SEARCH_REPO_SIZE}" # Spaces must be used instead of "+" for the PyGithub API to work properly


def configure_logger():
    os.makedirs(LOGGING_FOLDER, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(module)s.%(funcName)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(filename=f'{LOGGING_FOLDER}/log_{time.time_ns()}.txt', mode='a', encoding=None, delay=False),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    configure_logger()    
    try:
        while True:
            paginatedRepositories = github_api.search_github_repos(GITHUB_SEARCH_REPO_QUERY)
            logging.info(f"Found {paginatedRepositories.totalCount} repos with query \"{GITHUB_SEARCH_REPO_QUERY}\"")
            totalRepos = paginatedRepositories.totalCount
            currentRepo = 1
            for repo in paginatedRepositories:
                repo_name = repo.full_name
                logging.info(f"Parsing repo {repo_name} -- {repo.language} -- ({currentRepo}/{totalRepos})\n\n\n\n\n")
                if repo.language == "Java":
                    method_names = github_api.get_all_long_method_names_from_c_like_repo(repo_name)
                    twitter_api.tweet_method_names(method_names, repo_name)
                else:
                    logging.info(f"{repo_name} is not a Java project")
                    time.sleep(5)
                currentRepo = currentRepo + 1
    except Exception as e:
        logging.error(f"Could not fetch any other repositories after page due to {e}")


if (__name__ == "__main__"):
    # test()
    main()






def test():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(module)s.%(funcName)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(filename=f'./logs/test_log_{time.time_ns()}.txt', mode='a', encoding=None, delay=False),
            logging.StreamHandler(sys.stdout)
        ]
    )
    # method_names = github_api.get_all_long_method_names_from_c_like_repo("spring-projects/spring-security") # Repo with one method long method name to verify that code is working properly
    method_names = github_api.get_all_long_method_names_from_c_like_repo("apache/druid")
    twitter_api.tweet_method_names(method_names, "apache/druid")
    print(method_names)