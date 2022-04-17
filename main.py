import time
from . import github, twitter



# Github API
# Ref: https://docs.github.com/en/rest/reference/search
github_search_string = "spring"
github_search_repo_size = "size:>=20000"
github_search_repo_filters = "sort=updated&order=desc"
github_search_repo_query = f"{github_search_string} language:java {github_search_repo_size}" # Spaces must be used instead of "+" for the PyGithub API to work properly



#############################################
#                 MAIN CODE                 #
#############################################
def main():
    try:
        while True:
            paginatedRepositories = github.search_github_repos(github_search_repo_query)
            print(f"Found {paginatedRepositories.totalCount} repos found with query \"{github_search_repo_query}\"")
            totalRepos = paginatedRepositories.totalCount
            currentRepo = 1
            for repo in paginatedRepositories:
                repo_name = repo.full_name
                print(f"\n\n\n\n\nParsing repo {repo_name} -- {repo.language} -- ({currentRepo}/{totalRepos})")
                if repo.language == "Java":
                    method_names = github.get_all_long_method_names_from_c_like_repo(repo_name)
                    twitter.tweet_method_names(method_names, repo_name)
                else:
                    print(f"{repo_name} is not a Java project")
                    time.sleep(5)
                currentRepo = currentRepo + 1
    # get_all_long_method_names_from_c_like_repo("codecentric/spring-boot-admin") # Repo with one method long method name to verify that code is working properly
    except Exception as e:
        print(f"Could not fetch any other repositories after page due to {e}")

if (__name__ == "__main__"):
    main()