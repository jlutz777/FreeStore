<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta content="text/html; charset=utf-8" http-equiv="content-type">
<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.0/css/bootstrap.min.css">

<!-- Optional theme -->
<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.0/css/bootstrap-theme.min.css">

<!-- Latest compiled and minified JavaScript -->
<script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.0/js/bootstrap.min.js"></script>
</head>
<body>
<form method="POST" action="/checkin">
    <div>{{! form.shopperName.label }} {{! form.shopperName }}</div>
    <div>{{! form.shopperBirthday.label }} {{! form.shopperBirthday }}</div>
    <div>{{! form.email.label }} {{! form.email }}</div>
    <div>{{! form.phone.label }} {{! form.phone }}</div>
    <div>{{! form.address.label }} {{! form.address }}</div>
    <div>{{! form.zip.label }} {{! form.zip }}</div>
    <div>{{! form.dependentName.label }} {{! form.dependentName }}</div>
    <div>{{! form.dependentBirthday.label }} {{! form.dependentBirthday }}</div>
    <input type="submit" value="Submit">
</form>

% if form.errors:
<ul class="errors">
% for field_name, field_errors in form.errors.iteritems():
% if field_errors:
% for error in field_errors:
<li>{{! form[field_name].label }}: {{ error }}</li>
% end
% end
% end
</ul>
% end

</body>
</html>