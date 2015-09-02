<!DOCTYPE html>
<html lang="en">
<head>
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <meta content="text/html; charset=utf-8" http-equiv="content-type">
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <link rel="stylesheet" href="/css/bootstrap.min.css">
    <link rel="stylesheet" href="/css/bootstrap-theme.min.css">
    <script src="/js/bootstrap.min.js"></script>
</head>
<body>
    <div class="container" style="width:600px">
        <form action="login" method="POST" name="Login" role="form">
            <h2 class="h2 text-center">Free Store Customer Application</h2>
            <div class="form-group" style="margin-top:30px">
                <div class="row">
                <label for="username" class="col-sm-4 control-label">User name</label>
                <div class="col-sm-8">
                    <input autofocus class="form-control" id="username" name="username" type="text" />
                </div>
                </div>
            </div>
            <div class="form-group">
                <div class="row">
                <label for="password" class="col-sm-4 control-label">Password</label>
                <div class="col-sm-8">
                    <input autofocus class="form-control" id="password" name="password" type="password" />
                </div>
                </div>
            </div>
            % if defined('error_message'):
            <div class="row">
                <span>* {{ error_message }}</span>
            </div>
            % end
            <div class="row text-center">
                <button class="btn btn-large btn-primary" type="submit">Sign in</button>
            </div>
        </form>
    </div>
</body>
</html>