import subprocess
import system

def updateGitTags():
	repo_path = "C:\Users\dshevchyk\Desktop\PersonalProjects\IgniteStrava\data\projects\StravaInIgnition"
	def run_git_cmd(cmd):
		try:
			p = subprocess.Popen(cmd, cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			out, err = p.communicate()
			if p.returncode == 0:
			    return out.strip()
			else:
			    system.util.getLogger("GitUtils").error("Git error: " + err)
			    return "Error"
		except Exception as e:
			system.util.getLogger("GitUtils").error("Exception running Git: " + str(e))
			return "Exception"
            
    # 1. Get current branch
	branch = run_git_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"])
	
	# 2. Get short commit hash
	commit_hash = run_git_cmd(["git", "rev-parse", "--short", "HEAD"])
	
	# 3. Get last commit message
	commit_msg = run_git_cmd(["git", "log", "-1", "--pretty=%B"])
	
	# 4. Get last commit author
	author = run_git_cmd(["git", "log", "-1", "--pretty=%an"])

    # Define the paths to your tags
	base_tag_path = "[default]Git/GitInfo"
	paths = [
	    base_tag_path + "/Branch",
	    base_tag_path + "/CommitHash",
	    base_tag_path + "/CommitMessage",
	    base_tag_path + "/Author",
	    base_tag_path + "/LastUpdate"
	]
    
    # Define the values to write
	values = [
	    branch, 
	    commit_hash, 
	    commit_msg, 
	    author, 
	    system.date.now()
	]
	
	# Write to the tags simultaneously 
	system.tag.writeBlocking(paths, values)
	system.util.getLogger("GitUtils").info("Git context tags updated successfully.")