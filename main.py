
import requests

def main():
    username = str(input("Enter the github username: ")).strip()
    activity = f"https://api.github.com/users/{username}/events"
    try:
        response = requests.get(activity, timeout=10)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list):
            if data:
                user_activity(data) 
            else:
                print("User does not exist or has no public activity.")
        else:
            display_error("Unexpected response format from GitHub API")
    except requests.exceptions.HTTPError as http_err:
        status_code = getattr(response, "status_code", None)
        match status_code:
            case 400:
                display_error("Bad request\nPlease check your input")
            case 401:
                display_error("Unauthorized\nInvalid API key")
            case 403:
                display_error("Forbidden\nAccess Denied.")
            case 404:
                display_error("Not Found\nPlease check your input")
            case 500:
                display_error("Internal Server Error\nPlease try again")
            case 502:
                display_error("Bad Gateway\nPlease try again")
            case 503:
                display_error("Service Unavailable\nServer is down")
            case 504:
                display_error("Gateway Timeout\nPlease try again")
            case _:
                display_error(f"HTTP error occurred:\n{http_err}")
    except requests.exceptions.ConnectionError:
        display_error("Connection Error\nPlease check your internet connection")
    except requests.exceptions.Timeout:
        display_error("Timeout Error\nPlease try again")
    except requests.exceptions.TooManyRedirects:
        display_error("Too Many Redirects\nPlease try again")
    except requests.exceptions.RequestException as req_err:
        display_error(f"An error occurred while making the request:\n{req_err}")
    except requests.exceptions.JSONDecodeError:
        display_error("Error decoding JSON response\nPlease try again")


def display_error(message):
    print(message)


def user_activity(activity):
    for event in activity:
        if not isinstance(event, dict):
            print(f"Skipping unsupported event entry: {event!r}")
            continue

        event_type = event.get("type", "Unknown Event Type")
        repo_data = event.get("repo")
        repo_name = repo_data.get("name", "Unknown Repository") if isinstance(repo_data, dict) else "Unknown Repository"

    match event_type:
        case "PushEvent":
            commits = event.get("payload", {}).get("commits", [])
            print(f"Pushed {len(commits)} commits to {repo_name}")
        case "PullRequestEvent":
            print(f"Opened or updated a pull request in {repo_name}")
        case "IssuesEvent":
            print(f"Created or updated an issue in {repo_name}")
        case "IssueCommentEvent":
            print(f"Commented on an issue in {repo_name}")
        case "PullRequestReviewEvent":
            print(f"Reviewed a pull request in {repo_name}")
        case "PullRequestReviewCommentEvent":
            print(f"Commented on a pull request review in {repo_name}")
        case "CommitCommentEvent":
            print(f"Commented on a commit in {repo_name}")
        case "ForkEvent":
            print(f"Forked {repo_name}")
        case "WatchEvent":
            print(f"Starred {repo_name}")
        case "CreateEvent":
            print(f"Created a branch, tag, or repository in {repo_name}")
        case "DeleteEvent":
            print(f"Deleted a branch or tag in {repo_name}")
        case "ReleaseEvent":
            print(f"Published a release in {repo_name}")
        case "MemberEvent":
            print(f"Added a collaborator to {repo_name}")
        case "PublicEvent":
            print(f"Made {repo_name} public")
        case "GollumEvent":
            print(f"Updated the wiki for {repo_name}")
        case _:
            print(f"{event_type} in {repo_name}")



if __name__ == "__main__":
    main()