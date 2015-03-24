<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta content="text/html; charset=utf-8" http-equiv="content-type">
<meta name="viewport" content="width=device-width,initial-scale=1">
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<link rel="stylesheet" href="/css/bootstrap.min.css">
<link rel="stylesheet" href="/css/bootstrap-theme.min.css">
<script src="/js/bootstrap.min.js"></script>
</head>
<body>
    <div class="container">
        <form action="login" method="post" name="Login" class="form-signin">
            <div class="header">
                <h2 class="form-signin-heading">Free Store Customer Application</h2>
            </div>
            <div class="row">
                <input name="username" type="text" class="input-block-level" placeholder="User name">
            </div>
            <div class="row">
                <input name="password" type="password" class="input-block-level" placeholder="Password">
            </div>
            <div class="row">
                <button class="btn btn-large btn-primary" type="submit">Sign in</button>
            </div>
            <div class="row">
            % if defined('errMessage'):
                <span>* {{ errMessage }}</span>
            % end
            </div>
        </form>
    </div>
</body>
</html>