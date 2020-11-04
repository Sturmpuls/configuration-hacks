# Open Git Bash
# Check whether connection to Github over HTTPS Port 443 is generally possible
connect -H $HTTP_PROXY -d ssh.github.com 443

# Start SSH Agent (also add this command to .bash_profile)
eval "$(ssh-agent -s)"

# Create SSH Key
ssh-keygen -t rsa -b 4096 -C "user@example.com"
Enter file in which to save the key (/c/Users/florian.frosch/.ssh/id_rsa): /w/.ssh/id_rsa

# Add SSH-Key to SSH Agent
ssh-add /w/.ssh/id_rsa

# Add Proxies to Github Config
git config --global http.proxy $HTTP_PROXY
git config --global https.proxy $HTTP_PROXY

# Create/Edit ~/.ssh/config and add the following
	Host *
	  ProxyCommand connect -H $HTTP_PROXY %h %p 
	 
	# force github.com:22 to go to ssh.github.com:443 as only HTTPS port is allowed by my proxy
	Host github.com
	  # Automatically load the RSA key for Github when the agent is started
	  IdentityFile /w/.ssh/id_rsa
	  Hostname ssh.github.com
	  Port 443 

# Check whether it worked
ssh -T git@github.com


# Resources
- [rakhesh.com](https://rakhesh.com/windows/notes-on-using-git-from-behind-a-firewall-tunneling-ssh-through-a-proxy-git-credential-helpers-and-so-on/) helped me immensely to figure out how to make this work
- [yougg](https://gist.github.com/yougg/5d2b3353fc5e197a0917aae0b3287d64) provided me with a starting point
- [Github - Working with SSH Keys](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/working-with-ssh-key-passphrases) better way to set up SSH-Agent to auto-load Key