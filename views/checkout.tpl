% include renders
% renders_namespace = _
% get_menu = renders_namespace['get_menu']

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta content="text/html; charset=utf-8" http-equiv="content-type">
</head>
<body>
% get_menu()
<script type="text/javascript">
$(document).ready(function () {
    $('#add_another_button').click(function () {
        clone_field_list('.fieldset:last');
    });
    
    $('.remove_button').click(function (e) {
        if ($('.remove_button').length > 1)
        {
            var dependentGrandParent = $(e.target).parents("#dependent-fieldset");
            dependentGrandParent.remove();
        }
    });
});

function clone_field_list(selector) {
    var new_element = $(selector).clone(true);
    var elem_id = new_element.find(':input')[0].id;
    var elem_num = parseInt(elem_id.replace(/.*-(\d{1,4})-.*/m, '$1')) + 1;
    new_element.find(':input').each(function() {
        if (this.className.indexOf('remove_button') > -1)
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
<div class="your-form">
    <form method="POST" action="{{post_url}}" role="form" class="form_horizontal">
    </form>
</div>
% end
</body>
</html>