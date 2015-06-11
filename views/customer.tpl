% include renders
% renders_namespace = _ 
% get_field_errors = renders_namespace['get_field_errors']
% get_menu = renders_namespace['get_menu']

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta content="text/html; charset=utf-8" http-equiv="content-type">
</head>
<body>
% get_menu()
<script src="/js/jquery.mask.min.js"></script>
<script type="text/javascript">
$(document).ready(function () {
    $('#add_another_button').click(function ()
    {
        clone_field_list('.fieldset:last');
    });
    
    $('.remove_button').click(function (e)
    {
        if ($('.remove_button').length > 1)
        {
            var dependentGrandParent = $(e.target).parents("#dependent-fieldset");
            dependentGrandParent.remove();
        }
    });

    $('#delete_button').click(function (e)
    {
        var continueSubmit = confirm("Are you sure you want to delete this customer?");
        
        if (continueSubmit)
        {
            $.ajax({url: '{{post_url}}',
                type: 'DELETE',
                success: function(result)
                {
                    // TODO: delete with errors
                    window.location.href = '{{checkin_url}}';
                }
               });
        }
        e.preventDefault();
    });

    $('#noCheckin').click(function()
    {
        $('#checkinCust').val('false');
        $('#thisForm').submit();
    });

    $('#phone').mask('(000) 000-0000', {clearIfNotMatch: true, placeholder: "(XXX) XXX-XXXX"});
    $('#zip').mask('00000', {clearIfNotMatch: true, placeholder: "XXXXX"});
    $('.dependent-birthdate').mask("00/00/0000", {clearIfNotMatch: true, placeholder: "MM/DD/YYYY"});
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
        // Remove the old datepicker and re-add so it doesn't share with the cloned one
        if (id.indexOf('-birthdate') != -1)
        {
            var elemWithoutMask = $(this).clone(false);
            $(this).replaceWith(elemWithoutMask);
            elemWithoutMask.mask("00/00/0000", {clearIfNotMatch: true, placeholder: "MM/DD/YYYY"});
        }
    });
    new_element.find('label').each(function() {
        var new_for = $(this).attr('for').replace('-' + (elem_num - 1) + '-', '-' + elem_num + '-');
        $(this).attr('for', new_for);
    });
    $(selector).after(new_element);
}
</script>
<div class="your-form">
    % if form.errors:
    <div class="page-header">
    <h3 style="color:red">Correct The Errors Below!</h3>
    </div>
    % end
    % #if customer_id:
    <!--<div class="row">
        <form method="POST" action="/checkin" role="form" class="form_horizontal">
            <div class="form-group ">
                <div class="col-sm-10">
                    <input type="hidden" id="customer_id" name="customer_id" value="{{customer_id}}" />
                    <button type="submit" class="btn btn-default">Check In</button>
                </div>
            </div>
        </form>
    </div>-->
    % if aaa.current_user.role == 'admin':
    <div class="row">
        <div class="form-group ">
            <div class="col-sm-10">
                <button class="btn btn-default" id="delete_button">Delete</button>
            </div>
        </div>
    </div>
    % end
    % #end
    <form id="thisForm" method="POST" action="{{post_url}}" role="form" class="form_horizontal">
    % if customer_id:
    <div class="row" style="margin-top:10px">
        <div class="form-group"> 
            <div class="col-sm-10">
                <button type="submit" class="btn btn-default">Save Customer And Check In</button>
            </div>
        </div>
    </div>
    % end
    <div class="page-header">
    <h3>Primary Household Member</h3>
    </div>
    <div class="row">
    % dependent_index = -1
    % for dependent in form.dependents:
    % dependent_index += 1
    % if not dependent.isPrimary.data:
    % continue
    % end
        <input class="form-control" id="dependents-{{dependent_index}}-isPrimary" name="dependents-{{dependent_index}}-isPrimary" type="hidden" value="True">
        <div class="form-group ">
            <label for="dependents-{{dependent_index}}-firstName" class="col-sm-2 control-label">First Name</label>
            <div class="col-sm-10">
                <input autofocus class="form-control" id="dependents-{{dependent_index}}-firstName" name="dependents-{{dependent_index}}-firstName" type="text" value="{{dependent.firstName.data}}">
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
                <input class="form-control dependent-birthdate" id="dependents-{{dependent_index}}-birthdate" name="dependents-{{dependent_index}}-birthdate" type="datetime" value="{{dependent.birthdate.data.strftime("%m/%d/%Y")}}">
                % else:
                <input class="form-control dependent-birthdate" id="dependents-{{dependent_index}}-birthdate" name="dependents-{{dependent_index}}-birthdate" type="datetime" value="">
                % end
            </div>
            % get_field_errors(dependent.birthdate)
        </div>
            % if dependent["id"].data is not None:
                <input class="form-control" id="dependents-{{dependent_index}}-id" name="dependents-{{dependent_index}}-id" type="hidden" value="{{dependent["id"].data}}">
            % else:
                <input class="form-control" id="dependents-{{dependent_index}}-id" name="dependents-{{dependent_index}}-id" type="hidden" value="">
            % end
    % end
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
        <!--<label for="state" class="col-sm-2 control-label">State</label>
        <div class="col-sm-10">
            <input class="form-control" id="state" name="state" required type="text" value="{{form.state.data}}">
        </div>-->
        <input id="state" name="state" type="hidden" value="Ohio">
        % #get_field_errors(form.state)
    </div>
    <div class="form-group ">
        <label for="zip" class="col-sm-2 control-label">Zip</label>
        <div class="col-sm-10">
            <input class="form-control" id="zip" name="zip" required type="text" value="{{form.zip.data}}">
        </div>
        % get_field_errors(form.zip)
    </div>
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
        <label for="comments" class="col-sm-2 control-label">Checkin Comments</label>
        <div class="col-sm-10">
            % if form.comments.data is not None and not form.comments.errors:
            <input class="form-control" id="comments" name="comments" type="text" value="{{form.comments.data}}">
            % else:
            <input class="form-control" id="comments" name="comments" type="text" value="">
            % end
        </div>
        % get_field_errors(form.comments)
    </div>
    % if aaa.current_user.role == 'admin':
    <div class="form-group ">
        <label for="adminComments" style="color:red" class="col-sm-2 control-label">Admin Comments</label>
        <div class="col-sm-10">
            % if form.adminComments.data is not None and not form.adminComments.errors:
            <input class="form-control" style="color:red" id="adminComments" name="adminComments" type="text" value="{{form.adminComments.data}}">
            % else:
            <input class="form-control" style="color:red" id="adminComments" name="adminComments" type="text" value="">
            % end
        </div>
        % get_field_errors(form.adminComments)
    </div>
    % else:
    % # Non-admins see a readonly field
    % if form.adminComments.data is None or form.adminComments.data == '':
        <input id="adminComments" name="adminComments" type="hidden" value="">
    % else:
    <div class="form-group ">
        <label for="adminComments" style="color:red" class="col-sm-2 control-label">Admin Comments</label>
        <div class="col-sm-10">
        <input class="form-control" style="color:red" readonly id="adminComments" name="adminComments" type="text" value="{{form.adminComments.data}}">
        </div>
    </div>
    % end
    % end
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
    <h3>Household Members</h3>
    </div>
    % dependent_index = -1
    % for dependent in form.dependents:
    % dependent_index += 1
    % if dependent.isPrimary.data:
    % continue
    % end
    <div class="row" style="margin-left:0px; margin-right:0px">
    <div class="form-group fieldset" data-toggle="fieldset" id="dependent-fieldset">
        Household Member
    <div data-toggle="fieldset-entry">
        <input type="hidden" id="dependents-{{dependent_index}}-isPrimary" name="dependents-{{dependent_index}}-isPrimary" value="">
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
                <input class="form-control dependent-birthdate" id="dependents-{{dependent_index}}-birthdate" name="dependents-{{dependent_index}}-birthdate" type="datetime" value="{{dependent.birthdate.data.strftime("%m/%d/%Y")}}">
                % else:
                <input class="form-control dependent-birthdate" id="dependents-{{dependent_index}}-birthdate" name="dependents-{{dependent_index}}-birthdate" type="datetime" value="">
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
    <div class="row">
        <div class="form-group"> 
            <div class="col-sm-10">
                <button type="button" class="btn btn-success" id="add_another_button">Add Household Member</button>
            </div>
        </div>
    </div>
    <div class="row" style="margin-top:10px">
        <div class="form-group"> 
            <div class="col-sm-10">
                <button type="submit" class="btn btn-default">Save Customer And Check In</button>
            </div>
        </div>
    </div>
    <div class="row" style="margin-top:10px">
        <div class="form-group"> 
            <div class="col-sm-10">
                <button type="button" id="noCheckin" class="btn btn-info">Save With NO Check In</button>
            </div>
        </div>
    </div>
    <input type="hidden" id="checkinCust" name="checkinCust" value="true" />
    </form>
</div>
% if customer_id:
<div class="your-form">
    <div class="page_header">
        <h3>Visits</h3>
    </div>
    <div class="row">
        <div class="form-group ">
        <div class="row" style="margin-left:0px; margin-right:0px">
        <div class="col-sm-2"><span style="font-weight:bold"></span></div>
        <div class="col-sm-2"><span style="font-weight:bold">Checkin</span></div>
        <div class="col-sm-2"><span style="font-weight:bold">Checkout</span></div>
        </div>
        % for visit in visits:
            <div class="row" style="margin-left:0px; margin-right:0px">
            <div class="col-sm-2">
                <a href="{{visit_url_root}}/{{visit.id}}">Visit</a>
            </div>
            <div class="col-sm-2">
                {{visit.checkin.strftime("%m/%d/%Y %H:%M")}}
            </div>
            % if visit.checkout is None:
            <div class="col-sm-2">
                -None-
            </div>
            % else:
            <div class="col-sm-2">
                {{visit.checkout.strftime("%m/%d/%Y %H:%M")}}
            </div>
            % end
            </div>
        % end
        </div>
    </div>
</div>
% end
</body>
</html>

