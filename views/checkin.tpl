% include renders
% renders_namespace = _ 
% render_form = renders_namespace['render_form'] 

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta content="text/html; charset=utf-8" http-equiv="content-type">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<link rel="stylesheet" href="/css/bootstrap.min.css">
<link rel="stylesheet" href="/css/bootstrap-theme.min.css">
<script src="/js/bootstrap.min.js"></script>
<script type="text/javascript">
$(document).ready(function () {
    $('#add_another_button').click(function () {
        clone_field_list('.fieldset:last');
    });
    
    $('.remove_button').click(function (e) {
        if ($('.remove_button').length > 1)
        {
            e.target.parentElement.parentElement.removeChild(e.target.parentElement);
        }
    });
});

function clone_field_list(selector) {
    var new_element = $(selector).clone(true);
    var elem_id = new_element.find(':input')[0].id;
    var elem_num = parseInt(elem_id.replace(/.*-(\d{1,4})-.*/m, '$1')) + 1;
    new_element.find(':input').each(function() {
        if (this.className === 'remove_button')
            return;
        var id = $(this).attr('id').replace('-' + (elem_num - 1) + '-', '-' + elem_num + '-');
        $(this).attr({'name': id, 'id': id}).val('').removeAttr('checked');
    });
    new_element.find('label').each(function() {
        var new_for = $(this).attr('for').replace('-' + (elem_num - 1) + '-', '-' + elem_num + '-');
        $(this).attr('for', new_for);
    });
    $(selector).after(new_element);
}
</script>
</head>
<body>
<div class="your-form">
    % render_form(form, action_url=post_url, action_text='Submit Form')
</div>
</body>
</html>