# Deploy on EC2

This document explains how to run the voting app on an EC2 instance. The Polls table is Amazon DynamoDB. Create the table before you launch the instance.


## One-Time Setup

The file `deploy/userdata.sh` is used in the deployment process, and you must change one line before you deploy.

* Open `deploy/userdata.sh` in Cursor or `nano`.
* Near the top of the file you will find the line:

  ```
  REPO_URL="https://github.com/YOUR_GITHUB_USERNAME/voting-dynamodb.git"
  ```

* Change `YOUR_GITHUB_USERNAME` to your GitHub username.
* Commit this change to the git repo, and push it back to your GitHub account.

  ```
  git add deploy/userdata.sh
  git commit -m "set github account"
  git push origin main
  ```


If the `git push` command fails, check the url of `origin` and make sure it points at your fork of the repo.

```
git remote -v
```


## Create the Polls table

In the DynamoDB console, choose **Create table**.

* Table name: `Polls`
* Partition key: `pollId`, type String
* Capacity mode: On-demand


Create the table and wait until its status is Active. Launch the instance after the table exists. Gunicorn describes `Polls` when it starts, and it keeps restarting until that call succeeds.


## Launch the instance

`deploy/userdata.sh` does the following:

* Install Python and git
* Clone the repo
* Create the virtualenv
* Start Gunicorn


In the launch dialog:

* (Optional, but encouraged) Name the instance "Voting app"
* Use the default `t3.micro` instance type
* Select your `vockey` for authentication
* Choose the IAM instance profile `LabInstanceProfile`
* Ensure that HTTP and SSH are enabled in the security group
* Open the "Advanced" tab, and scroll to the bottom
* Paste the contents of `deploy/userdata.sh` into **User data**


When you launch the instance, AWS boots it and runs the userdata script. That takes a minute or two. Gunicorn then describes the `Polls` table. `/health` returns 200 when that call succeeds.

Associate your Elastic IP with this instance so your DNS name reaches it.


## Debugging

The Cloud-init process writes the userdata output to `/var/log/cloud-init-output.log`. If the app does not start, SSH to the instance and read that file.


## Other useful commands on the EC2 instance

- `systemctl status voting` — see the status of the Gunicorn process
- `curl -s http://localhost/health` — call `/health`. A 200 means the web server is running and it can describe the `Polls` table
- `sudo systemctl restart voting` — restart the web process after a config or code change
- `sudo journalctl -u voting -f` — follow the voting (gunicorn) logs
