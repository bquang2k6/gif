import requests
import re
from urllib.parse import urlparse, unquote

def get_default_branch(username, repo, token=None):
    """Lấy nhánh mặc định của repository."""
    api_url = f"https://api.github.com/repos/{username}/{repo}"
    headers = {"Authorization": f"token {token}"} if token else {}
    response = requests.get(api_url, headers=headers)
    
    if response.status_code != 200:
        raise ValueError(f"Không thể truy cập repository: {response.json().get('message', 'Unknown error')}")
    
    return response.json().get('default_branch', 'main')

def parse_github_url(url):
    """Phân tích URL GitHub để lấy username, repo, branch, và path."""
    url = unquote(url.strip())
    pattern = r'https?://github\.com/([^/]+)/([^/]+)(?:/tree/([^/]+)(?:/(.+))?)?'
    match = re.match(pattern, url)
    
    if not match:
        raise ValueError("URL không đúng định dạng GitHub!")
    
    username, repo, branch, path = match.groups()
    path = path or ""
    return username, repo, branch, path

def get_gifs_from_repo(repo_url, token=None):
    """Lấy tất cả file GIF từ một repository hoặc thư mục."""
    try:
        username, repo, branch, folder_path = parse_github_url(repo_url)
        if not branch:  # Nếu không có branch trong URL, lấy branch mặc định
            branch = get_default_branch(username, repo, token)
        
        api_url = f"https://api.github.com/repos/{username}/{repo}/contents/{folder_path}?ref={branch}"
        headers = {"Authorization": f"token {token}"} if token else {}
        
        response = requests.get(api_url, headers=headers)
        if response.status_code != 200:
            raise ValueError(f"Không thể truy cập repository: {response.json().get('message', 'Unknown error')}")
        
        files = response.json()
        raw_links = []
        
        for file in files:
            if isinstance(file, dict) and file['name'].endswith('.gif'):
                raw_link = f"https://raw.githubusercontent.com/{username}/{repo}/refs/heads/{branch}/{folder_path}/{file['name']}" if folder_path else f"https://raw.githubusercontent.com/{username}/{repo}/refs/heads/{branch}/{file['name']}"
                raw_links.append(f'"{raw_link}",')
        
        return raw_links
    except ValueError as e:
        return [f"Error: {str(e)}"]

def main():
    # URL mặc định
    repo_url = "https://github.com/bquang2k6/gif"
    # Token để trống nếu repository công khai, hoặc thay bằng token của bạn nếu riêng tư
    token = None  # Thay bằng token nếu cần: "your_github_token_here"
    
    print(f"Đang lấy các file GIF từ {repo_url}...")
    raw_links = get_gifs_from_repo(repo_url, token)
    
    print("\nDanh sách link raw của các file GIF:")
    if raw_links:
        for link in raw_links:
            print(link)
    else:
        print("Không tìm thấy file GIF nào trong repository.")

if __name__ == "__main__":
    main()