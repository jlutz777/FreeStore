% include renders
% renders_namespace = _
% get_field_errors = renders_namespace['get_field_errors']
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
            var dependentGrandParent = $(e.target).parents("#shoppingitem-fieldset");
            dependentGrandParent.remove();
        }
    });
});

function clone_field_list(selector) {
    var new_element = $(selector).parent().clone(true);
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
    <div class="page-header">
    <h3>Checkout</h3>
    </div>
    <div class="row" style="margin-left:0px; margin-right:0px">
    Family email: {{visit.family.email}}
    <div class="form-group ">
        <label for="checkin" class="col-sm-2 control-label">Checkin Time</label>
        <div class="col-sm-10">
            <input class="form-control" readonly id="checkin" name="checkin" type="text" value="{{form.checkin.data.strftime("%m/%d/%Y %H:%M:%S")}}" />
            <input type="hidden" id="family_id" name="family_id" value="{{visit.family.id}}" />
        </div>
        % get_field_errors(form.checkin)
    </div>
    </div>
    % shoppingitem_index = -1
    % for shoppingitem in form.items:
    % shoppingitem_index += 1
    <div class="row" style="margin-left:0px; margin-right:0px">
    <div class="form-group fieldset" data-toggle="fieldset" id="shoppingitem-fieldset">
        Item
    <div data-toggle="fieldset-entry">
        <div class="form-group ">
            <label for="items-{{shoppingitem_index}}-name" class="col-sm-2 control-label">Name</label>
            <div class="col-sm-10">
                % if shoppingitem["name"].data is not None:
                <input class="form-control" id="items-{{shoppingitem_index}}-name" name="items-{{shoppingitem_index}}-name" type="text" value="{{shoppingitem["name"].data}}">
                % else:
                <input class="form-control" id="items-{{shoppingitem_index}}-name" name="items-{{shoppingitem_index}}-name" type="text" value="">
                % end
            </div>
            % get_field_errors(shoppingitem["name"])
        </div>
        <div class="form-group ">
            <label for="items-{{shoppingitem_index}}-category" class="col-sm-2 control-label">Category</label>
            <div class="col-sm-10">
                % if shoppingitem.category.data is not None and not shoppingitem.category.errors:
                <select class="form-control" id="items-{{shoppingitem_index}}-category" name="items-{{shoppingitem_index}}-category">
                    % for option in shoppingitem["category"].choices:
                    <option value="{{option.id}}">{{option.name}</option>
                    % end
                    # {{shoppingitem.category.data}}
                </select>
                % else:
                <select class="form-control" id="items-{{shoppingitem_index}}-category" name="items-{{shoppingitem_index}}-category">
                    % for option in shoppingitem["category"].choices:
                    <option value="{{option[0]}}">{{option[1]}}</option>
                    % end
                    # {{shoppingitem.category.data}}
                </select>
                % end
            </div>
            % get_field_errors(shoppingitem.category)
        </div>
        <div class="form-group ">
            <div class="col-sm-10">
            % if shoppingitem["id"].data is not None:
                <input class="form-control" id="items-{{shoppingitem_index}}-id" name="items-{{shoppingitem_index}}-id" type="hidden" value="{{shoppingitem["id"].data}}">
            % else:
                <input class="form-control" id="items-{{shoppingitem_index}}-id" name="items-{{shoppingitem_index}}-id" type="hidden" value="">
            % end
            </div>
        </div>
    </div>
    <div class="form-group"> 
        <div class="col-sm-offset-2 col-sm-10">
            <button type="button" class="remove_button btn btn-danger" data-toggle="fieldset-remove-row">Remove</button>
        </div>
    </div>
    </div>
    </div>
    % end
    <div class="form-group"> 
        <div class="col-sm-10">
            <button type="button" class="btn btn-success" id="add_another_button">Add Item</button>
        </div>
    </div>
    <div class="form-group"> 
        <div class="col-sm-10">
            <button type="submit" class="btn btn-default">Checkout</button>
        </div>
    </div>
    </form>
</div>
</body>
</html>