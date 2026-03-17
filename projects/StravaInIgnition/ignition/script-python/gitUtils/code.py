import subprocess
import system
import time

def updateGitTags(tag_provider="default", instance_name="GitInfo"):
    # Define the path to your Ignition project folder
    repo_path = "C:\Users\dshevchyk\Desktop\PersonalProjects\IgniteStrava\data\projects\StravaInIgnition"
    logger = system.util.getLogger("GitUtils")
    
    # --- 1. Ensure UDT Definition and Instance Exist ---
    base_provider = "[{}]".format(tag_provider)
    udt_name = "GitContext"
    udt_def_path = "{}_types_/{}".format(base_provider, udt_name)
    instance_path = "{}{}".format(base_provider, instance_name)
    
    # Check if the UDT Definition exists; if not, build it.
    if not system.tag.exists(udt_def_path):
        logger.info("UDT Definition '{}' not found. Creating it...".format(udt_name))
        udt_def = {
            "name": udt_name,
            "tagType": "UdtType",
            "tags": [
                {"name": "Branch", "valueSource": "memory", "dataType": "String"},
                {"name": "CommitHash", "valueSource": "memory", "dataType": "String"},
                {"name": "CommitMessage", "valueSource": "memory", "dataType": "String"},
                {"name": "Author", "valueSource": "memory", "dataType": "String"},
                {"name": "LastUpdate", "valueSource": "memory", "dataType": "DateTime"},
                {"name": "IsDirty", "valueSource": "memory", "dataType": "Boolean"},
                {"name": "LatestRelease", "valueSource": "memory", "dataType": "String"},
                {"name": "CommitsBehind", "valueSource": "memory", "dataType": "Int4"},
                {"name": "CommitDate", "valueSource": "memory", "dataType": "DateTime"},
                {"name": "RemoteURL", "valueSource": "memory", "dataType": "String"}
            ]
        }
        # Write the definition to the provider's data types folder
        system.tag.configure("{}_types_".format(base_provider), [udt_def], "m")
        
    # Check if the UDT Instance exists; if not, build it.
    if not system.tag.exists(instance_path):
        logger.info("UDT Instance '{}' not found. Creating it...".format(instance_name))
        udt_instance = {
            "name": instance_name,
            "typeId": udt_name,
            "tagType": "UdtInstance"
        }
        # Create the instance in the root of the tag provider
        system.tag.configure(base_provider, [udt_instance], "m")
        
        # Give the Ignition Tag Engine a tiny fraction of a second to initialize the new tags
        # before we attempt to write to them at the end of this script.
        time.sleep(0.5)

    # --- 2. Helper Function for Git ---
    def run_git_cmd(cmd):
        try:
            p = subprocess.Popen(cmd, cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            if p.returncode == 0:
                return out.strip()
            else:
                logger.warn("Git command failed: {} | Error: {}".format(" ".join(cmd), err))
                return None
        except Exception as e:
            logger.error("Exception running Git: " + str(e))
            return None

    # --- 3. Gather Git Info ---
    branch = run_git_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"]) or "Unknown"
    commit_hash = run_git_cmd(["git", "rev-parse", "--short", "HEAD"]) or "Unknown"
    commit_msg = run_git_cmd(["git", "log", "-1", "--pretty=%B"]) or "Unknown"
    author = run_git_cmd(["git", "log", "-1", "--pretty=%an"]) or "Unknown"
    
    status_out = run_git_cmd(["git", "status", "--porcelain"])
    is_dirty = True if status_out else False
    
    latest_release = run_git_cmd(["git", "describe", "--tags", "--abbrev=0"]) or "No Tags"
    
    behind_str = run_git_cmd(["git", "rev-list", "--count", "HEAD..@{u}"])
    commits_behind = int(behind_str) if behind_str and behind_str.isdigit() else 0
    
    commit_unix = run_git_cmd(["git", "log", "-1", "--format=%ct"])
    if commit_unix and commit_unix.isdigit():
        commit_date = system.date.fromMillis(int(commit_unix) * 1000)
    else:
        commit_date = None
        
    remote_url = run_git_cmd(["git", "config", "--get", "remote.origin.url"]) or "Unknown"

    # --- 4. Write Values to Tags ---
    paths = [
        instance_path + "/Branch",
        instance_path + "/CommitHash",
        instance_path + "/CommitMessage",
        instance_path + "/Author",
        instance_path + "/LastUpdate",
        instance_path + "/IsDirty",
        instance_path + "/LatestRelease",
        instance_path + "/CommitsBehind",
        instance_path + "/CommitDate",
        instance_path + "/RemoteURL"
    ]
    
    values = [
        branch, commit_hash, commit_msg, author, 
        system.date.now(), is_dirty, latest_release, 
        commits_behind, commit_date, remote_url
    ]
    
    system.tag.writeBlocking(paths, values)
    logger.info("Git context tags updated successfully.")