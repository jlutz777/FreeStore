<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta content="text/html; charset=utf-8" http-equiv="content-type">
</head>
<body>
<form method="POST" action="/checkin">
    <div>{{! form.shopperName.label }} {{! form.shopperName }}</div>
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