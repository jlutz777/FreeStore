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
    <div class="page-header">
    <h3>Family Information</h3>
    </div>
    <div class="row">
    <div class="form-group ">
        <label for="email" class="col-sm-2 control-label">Email</label>
        <div class="col-sm-10">
            <input class="form-control" id="email" name="email" type="text" value="{{form.email.data}}">
        </div>
        % get_field_errors(form.email)
    </div>
    <div class="form-group ">
        <label for="phone" class="col-sm-2 control-label">Phone</label>
        <div class="col-sm-10">
            <input class="form-control" id="phone" name="phone" type="text" value="{{form.phone.data}}">
        </div>
        % get_field_errors(form.phone)
    </div>
    <div class="form-group ">
        <label for="address" class="col-sm-2 control-label">Street Address</label>
        <div class="col-sm-10">
            <input class="form-control" id="address" name="address" type="text" value="{{form.address.data}}">
        </div>
        % get_field_errors(form.address)
    </div>
    <div class="form-group ">
        <label for="city" class="col-sm-2 control-label">City</label>
        <div class="col-sm-10">
            <input class="form-control" id="city" name="city" required type="text" value="{{form.city.data}}">
        </div>
        % get_field_errors(form.city)
    </div>
    <div class="form-group ">
        <label for="state" class="col-sm-2 control-label">State</label>
        <div class="col-sm-10">
            <input class="form-control" id="state" name="state" required type="text" value="{{form.state.data}}">
        </div>
        % get_field_errors(form.state)
    </div>
    <div class="form-group ">
        <label for="zip" class="col-sm-2 control-label">Zip</label>
        <div class="col-sm-10">
            <input class="form-control" id="zip" name="zip" required type="text" value="{{form.zip.data}}">
        </div>
        % get_field_errors(form.zip)
    </div>
    % if form.datecreated.data is not None:
    <div class="form-group ">
        <label for="datecreated" class="col-sm-2 control-label">Date Created</label>
        <div class="col-sm-10">
            <input class="form-control" readonly id="datecreated" name="datecreated" type="text" value="{{form.datecreated.data.strftime("%m/%d/%Y")}}">
        </div>
        % get_field_errors(form.datecreated)
    </div>
    % end
    </div>
    <div class="page-header">
    <h3>Dependents</h3>
    </div>
    % dependent_index = -1
    % for dependent in form.dependents:
    % dependent_index += 1
    <div class="row" style="margin-left:0px; margin-right:0px">
    <div class="form-group fieldset" data-toggle="fieldset" id="dependent-fieldset">
        Dependent
    <div data-toggle="fieldset-entry">
        <div class="form-group ">
            <label for="dependents-{{dependent_index}}-isPrimary" class="col-sm-2 control-label">Primary</label>
            <div class="col-sm-10">
                <input
                % if dependent.isPrimary.data:
                checked
                % end
                class="form-control" id="dependents-{{dependent_index}}-isPrimary" name="dependents-{{dependent_index}}-isPrimary" type="checkbox" value="{{dependent.isPrimary.data}}">
            </div>
            % get_field_errors(dependent.isPrimary)
        </div>
        <div class="form-group ">
            <label for="dependents-{{dependent_index}}-firstName" class="col-sm-2 control-label">First Name</label>
            <div class="col-sm-10">
                <input class="form-control" id="dependents-{{dependent_index}}-firstName" name="dependents-{{dependent_index}}-firstName" type="text" value="{{dependent.firstName.data}}">
            </div>
            % get_field_errors(dependent.firstName)
        </div>
        <div class="form-group ">
            <label for="dependents-{{dependent_index}}-lastName" class="col-sm-2 control-label">Last Name</label>
            <div class="col-sm-10">
                <input class="form-control" id="dependents-{{dependent_index}}-lastName" name="dependents-{{dependent_index}}-lastName" type="text" value="{{dependent.lastName.data}}">
            </div>
            % get_field_errors(dependent.lastName)
        </div>
        <div class="form-group ">
            <label for="dependents-{{dependent_index}}-birthdate" class="col-sm-2 control-label">Birthday</label>
            <div class="col-sm-10">
                % if dependent.birthdate.data is not None and not dependent.birthdate.errors:
                <input class="form-control" id="dependents-{{dependent_index}}-birthdate" name="dependents-{{dependent_index}}-birthdate" type="datetime" value="{{dependent.birthdate.data.strftime("%m/%d/%Y")}}">
                % else:
                <input class="form-control" id="dependents-{{dependent_index}}-birthdate" name="dependents-{{dependent_index}}-birthdate" type="datetime" value="">
                % end
            </div>
            % get_field_errors(dependent.birthdate)
        </div>
        <div class="form-group ">
            <div class="col-sm-10">
            % if dependent["id"].data is not None:
                <input class="form-control" id="dependents-{{dependent_index}}-id" name="dependents-{{dependent_index}}-id" type="hidden" value="{{dependent["id"].data}}">
            % else:
                <input class="form-control" id="dependents-{{dependent_index}}-id" name="dependents-{{dependent_index}}-id" type="hidden" value="">
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
            <button type="button" class="btn btn-success" id="add_another_button">Add Dependent</button>
        </div>
    </div>
    <div class="form-group"> 
        <div class="col-sm-10">
            <button type="submit" class="btn btn-default">Submit Customer</button>
        </div>
    </div>
    </form>
</div>
% if customer_id:
<div class="your-form">
    <div class="form-group ">
    % for visit in visits:
        <div class="col-sm-10">
            {{visit.checkin}}, {{visit.checkout}}
        </div>
    % end
    </div>
    <form method="POST" action="/checkin" role="form" class="form_horizontal">
        <div class="form-group ">
            <div class="col-sm-10">
                <input type="hidden" id="customer_id" name="customer_id" value="{{customer_id}}" />
                <button type="submit" class="btn btn-default">Check In</button>
            </div>
        </div>
    </form>
</div>
% end
</body>
</html>