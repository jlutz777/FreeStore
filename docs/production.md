# Production
When code is ready to be pushed to production, you use git push, similar to heroku.

You first need to set up a git remote to the vm that you wish to push to.
`
jlutz777@freestore:~/workspace (master) $ git remote -v
dokku   dokku@104.131.23.85:customers (fetch)
dokku   dokku@104.131.23.85:customers (push)
origin  https://github.com/jlutz777/FreeStore.git (fetch)
origin  https://github.com/jlutz777/FreeStore.git (push)
`

The digital ocean VM also needs SSH keys set up properly.

After these are done, you can do `git push dokku` to push the code live.