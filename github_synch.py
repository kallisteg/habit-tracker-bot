# github_synch.py
import requests
import base64
import json
import os
from typing import Optional, Dict, Any
import csv
from io import StringIO

class GitHubCSVSync:
    def __init__(self, repo_owner: str, repo_name: str, file_path: str, github_token: str, branch: str = "main"):
        """
        Initialize GitHub CSV synchronization.
        
        Args:
            repo_owner: GitHub username or organization name
            repo_name: Repository name
            file_path: Path to the CSV file in the repository (e.g., "data/habit_list.csv")
            github_token: GitHub personal access token
            branch: Branch name (default: "main")
        """
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.file_path = file_path
        self.github_token = github_token
        self.branch = branch
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "HabitTrackerBot/1.0"
        }
        
    def _get_file_sha(self) -> Optional[str]:
        """Get the current SHA of the file in the repository."""
        url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/contents/{self.file_path}"
        params = {"ref": self.branch}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                return response.json()["sha"]
            elif response.status_code == 404:
                # File doesn't exist yet
                return None
            else:
                print(f"Error getting file SHA: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Exception getting file SHA: {e}")
            return None
    
    def download_csv(self) -> list:
        """
        Download CSV file from GitHub repository.
        
        Returns:
            List of dictionaries representing CSV data
        """
        url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/contents/{self.file_path}"
        params = {"ref": self.branch}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                # Decode the content
                content = response.json()["content"]
                decoded_content = base64.b64decode(content).decode('utf-8')
                
                # Parse CSV
                csv_data = []
                csv_reader = csv.DictReader(StringIO(decoded_content))
                for row in csv_reader:
                    csv_data.append(row)
                
                print(f"✅ Successfully downloaded {len(csv_data)} rows from {self.file_path}")
                return csv_data
                
            elif response.status_code == 404:
                print(f"📄 File {self.file_path} not found in repository. Creating new file.")
                return []
            else:
                print(f"❌ Error downloading file: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            print(f"❌ Exception downloading file: {e}")
            return []
    
    def upload_csv(self, csv_data: list) -> bool:
        """
        Upload CSV data to GitHub repository.
        
        Args:
            csv_data: List of dictionaries representing CSV data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert CSV data to string
            output = StringIO()
            if csv_data:
                fieldnames = csv_data[0].keys()
                writer = csv.DictWriter(output, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(csv_data)
            else:
                # Empty CSV with default headers
                writer = csv.DictWriter(output, fieldnames=['user_id', 'habits'])
                writer.writeheader()
            
            csv_content = output.getvalue()
            
            # Encode content
            encoded_content = base64.b64encode(csv_content.encode('utf-8')).decode('utf-8')
            
            # Get current SHA if file exists
            current_sha = self._get_file_sha()
            
            # Prepare commit data
            commit_data = {
                "message": f"Update {self.file_path} via Habit Tracker Bot",
                "content": encoded_content,
                "branch": self.branch
            }
            
            if current_sha:
                commit_data["sha"] = current_sha
            
            # Upload to GitHub
            url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/contents/{self.file_path}"
            
            response = requests.put(url, headers=self.headers, json=commit_data)
            
            if response.status_code in [200, 201]:
                print(f"✅ Successfully uploaded {len(csv_data)} rows to {self.file_path}")
                return True
            else:
                print(f"❌ Error uploading file: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Exception uploading file: {e}")
            return False
    
    def sync_from_github(self, local_file_path: str) -> bool:
        """
        Download CSV from GitHub and save to local file.
        
        Args:
            local_file_path: Local path to save the CSV file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            csv_data = self.download_csv()
            
            # Save to local file
            with open(local_file_path, 'w', newline='', encoding='utf-8') as file:
                if csv_data:
                    fieldnames = csv_data[0].keys()
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(csv_data)
                else:
                    # Create empty file with headers
                    writer = csv.DictWriter(file, fieldnames=['user_id', 'habits'])
                    writer.writeheader()
            
            print(f"✅ Synced {len(csv_data)} rows from GitHub to {local_file_path}")
            return True
            
        except Exception as e:
            print(f"❌ Exception syncing from GitHub: {e}")
            return False
    
    def sync_to_github(self, local_file_path: str) -> bool:
        """
        Read local CSV file and upload to GitHub.
        
        Args:
            local_file_path: Local path to the CSV file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Read local file
            csv_data = []
            if os.path.exists(local_file_path):
                with open(local_file_path, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    csv_data = list(reader)
            
            # Upload to GitHub
            return self.upload_csv(csv_data)
            
        except Exception as e:
            print(f"❌ Exception syncing to GitHub: {e}")
            return False

# Environment variable configuration
def get_github_config() -> Dict[str, str]:
    """
    Get GitHub configuration from environment variables.
    
    Returns:
        Dictionary with GitHub configuration
    """
    return {
        "repo_owner": os.getenv("GITHUB_REPO_OWNER", ""),
        "repo_name": os.getenv("GITHUB_REPO_NAME", ""),
        "github_token": os.getenv("GITHUB_TOKEN", ""),
        "file_path": os.getenv("GITHUB_FILE_PATH", "data/habit_list.csv"),
        "branch": os.getenv("GITHUB_BRANCH", "main")
    }

def create_github_sync() -> Optional[GitHubCSVSync]:
    """
    Create GitHubCSVSync instance from environment variables.
    
    Returns:
        GitHubCSVSync instance or None if configuration is incomplete
    """
    config = get_github_config()
    
    if not all([config["repo_owner"], config["repo_name"], config["github_token"]]):
        print("⚠️  GitHub configuration incomplete. Set GITHUB_REPO_OWNER, GITHUB_REPO_NAME, and GITHUB_TOKEN environment variables.")
        return None
    
    return GitHubCSVSync(
        repo_owner=config["repo_owner"],
        repo_name=config["repo_name"],
        file_path=config["file_path"],
        github_token=config["github_token"],
        branch=config["branch"]
    ) 