<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta content="text/html; charset=utf-8" http-equiv="content-type">
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<link rel="stylesheet" href="/css/bootstrap.min.css">
<link rel="stylesheet" href="/css/bootstrap-theme.min.css">
<script src="/js/bootstrap.min.js"></script>
</head>
<body>
    <div class="container">
        <form action="login" method="post" name="Login" class="form-signin">
            <h2 class="form-signin-heading">Please sign in</h2>
            <input name="username" type="text" class="input-block-level" placeholder="User name">
            <input name="password" type="password" class="input-block-level" placeholder="Password">
            <button class="btn btn-large btn-primary" type="submit">Sign in</button>
            % if defined('errMessage'):
                <span>* {{ errMessage }}</span>
            % end
        </form>
    </div>
</body>
</html>