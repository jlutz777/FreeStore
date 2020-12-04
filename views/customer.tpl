% from utils.utils import *
% include renders
% renders_namespace = _ 
% get_field_errors = renders_namespace['get_field_errors']
% get_menu = renders_namespace['get_menu']

<!DOCTYPE html>
<html lang="en">
<head>
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <meta content="text/html; charset=utf-8" http-equiv="content-type">
</head>
<body>
% get_menu()
<script src="/js/jquery.mask.min.js"></script>
<script type="text/javascript">
    var isExisting = false;
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
        
        $('#volunteer_checkin_button').click(function (e)
        {
            $('#checkinCust').val('false');
            $('#checkinVolunteer').val('true');
            $('#thisForm').submit();
        });
    
        // By default we want to check in the customer when changing them, but
        // this extra hidden input is checked on the server side when you don't want
        // the customer checked in
        $('#noCheckin').click(function()
        {
            $('#checkinCust').val('false');
            $('#thisForm').submit();
        });
    
        $('#phone').mask('(000) 000-0000', {clearIfNotMatch: true, placeholder: "(XXX) XXX-XXXX"});
        $('#zip').mask('00000', {clearIfNotMatch: true, placeholder: "XXXXX"});
        $('.dependent-birthdate').mask("00/00/0000", {clearIfNotMatch: true, placeholder: "MM/DD/YYYY"});
        
        % if customer_id:
        isExisting = true;
        % end
        
        checkCustomerAndVisitorStatus();
    });
    
    function capitalizeAndCheckName(dependent_id) {
        capitalizeFirstAndLastNames(dependent_id);
        checkPrimaryName(dependent_id);
    }
    
    function capitalizeFirstAndLastNames(dependent_id) {
        var firstNameField = $(`#dependents-${dependent_id}-firstName`);
        var lastNameField = $(`#dependents-${dependent_id}-lastName`);
        
        var first_name = firstNameField.val();
        var last_name = lastNameField.val();
        
        firstNameField.val(first_name.charAt(0).toUpperCase() + first_name.slice(1));
        lastNameField.val(last_name.charAt(0).toUpperCase() + last_name.slice(1));
    }
    
    function checkPrimaryName(dependent_id) {
        var first_name = $(`#dependents-${dependent_id}-firstName`).val();
        var last_name = $(`#dependents-${dependent_id}-lastName`).val();
        
        $.ajax({url: '/customercheck',
            type: 'GET',
            data: {
              'firstName': first_name,
              'lastName': last_name,
              'this_customer_id': {{customer_id or -1}}
            },
            success: function(result)
            {
                if (result.length > 0)
                {
                    var matchString = '';
                    for (i=0; i<result.length; i++)
                    {
                        var individualMatch = result[i];
                        matchString += individualMatch.fullName + '\n';
                    }
                    var matchChild = $('#matchingCustomer').show().children(":nth-child(2)");
                    matchChild.text(matchString);
                    matchChild.html(matchChild.html().replace(/\n/g,'<br/>'));
                    matchChild.parentsUntil(".form-group").addClass('has-error');
                }
                else
                {
                    $('#matchingCustomer').hide().parentsUntil(".form-group").removeClass('has-error');
                }
            }
           });
    }
    
    // This function duplicates the current dependent structure and creates a new one
    // This keeps the customer simple unless we need extra dependents
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
        $(selector).parent().after(new_element);
    }
    
    function checkCustomerAndVisitorStatus()
    {
        if ($('#isCustomer').prop('checked'))
        {
            $('#visits').show();
            $('.dependent').show();
            $('#dependents_header').show();
            $('#add_another_button').parent().parent().show();
        }
        else
        {
            $('#visits').hide();
            $('.dependent').hide();
            $('#dependents_header').hide();
            $('#add_another_button').parent().parent().hide();
        }
        
        if ($('#isVolunteer').prop('checked'))
        {
            $('#volunteering').show();
            if (isExisting)
            {
                $('#volunteer_checkin').show();
            }
            else
            {
                $('#volunteer_checkin').hide();
            }
        }
        else
        {
            $('#volunteering').hide();
            $('#volunteer_checkin').hide();
        }
    }
</script>
<div class="container-fluid">
    % if form.errors:
    <div class="page-header">
        <h3 class="text-danger">Correct The Errors Below!</h3>
    </div>
    % end
    % if aaa.current_user.role == 'admin':
    <div class="row">
        <div class="col-sm-12">
            <button class="btn btn-danger" id="delete_button">Delete</button>
        </div>
    </div>
    % end
    <div class="row" id="volunteer_checkin" style="display:none; margin-top:10px;">
        <div class="col-sm-12">
            <button class="btn btn-info" id="volunteer_checkin_button">Volunteer Check In</button>
        </div>
    </div>
    <form id="thisForm" method="POST" action="{{post_url}}" role="form">
        <input id="state" name="state" type="hidden" value="Ohio">
        % if customer_id:
        <div class="row" style="margin-top:10px">
            <div class="col-sm-12">
                <button type="submit" class="btn btn-default">Save And Check In</button>
            </div>
        </div>
        % end
    <div class="page-header">
        <h3>Primary Household Member</h3>
    </div>
    <div class="form-horizontal">
    % dependent_index = -1
    % for dependent in form.dependents:
    % dependent_index += 1
    % if not dependent.isPrimary.data:
    % continue
    % end
        <input class="form-control" id="dependents-{{dependent_index}}-isPrimary" name="dependents-{{dependent_index}}-isPrimary" type="hidden" value="True">
        <div class="form-group 
        % if dependent.firstName.errors:
        has-error
        % end
        ">
            <label for="dependents-{{dependent_index}}-firstName" class="col-sm-2 control-label">First Name</label>
            <div class="col-sm-10">
                <input autofocus class="form-control" id="dependents-{{dependent_index}}-firstName" onblur="capitalizeAndCheckName({{dependent_index}})" name="dependents-{{dependent_index}}-firstName" type="text" value="{{dependent.firstName.data}}">
                % get_field_errors(dependent.firstName)
            </div>
        </div>
        <div class="form-group 
        % if dependent.lastName.errors:
        has-error
        % end
        ">
            
            <label for="dependents-{{dependent_index}}-lastName" class="col-sm-2 control-label">Last Name</label>
            <div class="col-sm-10">
                <input class="form-control" id="dependents-{{dependent_index}}-lastName" onblur="capitalizeAndCheckName({{dependent_index}})" name="dependents-{{dependent_index}}-lastName" type="text" value="{{dependent.lastName.data}}">
                % get_field_errors(dependent.lastName)
                <div id="matchingCustomer" class="page_header" style="display:none;">
                    <p class="help-block">Possible matching customer!</p>
                    <p class="help-block"></p>
                </div>
            </div>
        </div>
        <div class="form-group 
        % if dependent.birthdate.errors:
        has-error
        % end
        ">
            <label for="dependents-{{dependent_index}}-birthdate" class="col-sm-2 control-label">Birthday</label>
            <div class="col-sm-10">
                % if dependent.birthdate.data is not None and not dependent.birthdate.errors:
                <input class="form-control dependent-birthdate" id="dependents-{{dependent_index}}-birthdate" name="dependents-{{dependent_index}}-birthdate" type="datetime" value="{{formatted_str_date(dependent.birthdate.data)}}">
                % else:
                <input class="form-control dependent-birthdate" id="dependents-{{dependent_index}}-birthdate" name="dependents-{{dependent_index}}-birthdate" type="datetime" value="">
                % end
                % get_field_errors(dependent.birthdate)
            </div>
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
    </div>
    <div class="form-group 
        % if form.city.errors:
        has-error
        % end
        ">
        <label for="city" class="col-sm-2 control-label">City</label>
        <div class="col-sm-10">
            <input class="form-control" id="city" name="city" required type="text" value="{{form.city.data}}">
            % get_field_errors(form.city)
        </div>
    </div>
    <div class="form-group 
        % if form.zip.errors:
        has-error
        % end
        ">
        <label for="zip" class="col-sm-2 control-label">Zip</label>
        <div class="col-sm-10">
            <input class="form-control" id="zip" name="zip" required type="text" value="{{form.zip.data}}">
            % get_field_errors(form.zip)
        </div>
    </div>
    <div class="form-group ">
        <label for="email" class="col-sm-2 control-label">Email</label>
        <div class="col-sm-10">
            <input class="form-control" id="email" name="email" type="text" value="{{form.email.data}}">
        </div>
    </div>
    <div class="form-group ">
        <label for="phone" class="col-sm-2 control-label">Phone</label>
        <div class="col-sm-10">
            <input class="form-control" id="phone" name="phone" type="text" value="{{form.phone.data}}">
        </div>
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
    </div>
    <div class="form-group ">
        <label for="isCustomer" class="col-sm-2 control-label">Customer?</label>
        <div class="col-sm-10">
            <input class="form-control" id="isCustomer" name="isCustomer" type="checkbox" value="isCustomer" onchange="checkCustomerAndVisitorStatus()"
            % if form.isCustomer.data is None or form.isCustomer.data:
            checked
            % end
            >
        </div>
    </div>
    <div class="form-group ">
        <label for="isVolunteer" class="col-sm-2 control-label">Volunteer?</label>
        <div class="col-sm-10">
            <input class="form-control" id="isVolunteer" name="isVolunteer" type="checkbox" value="isVolunteer" onchange="checkCustomerAndVisitorStatus()"
            % if form.isVolunteer.data is not None and form.isVolunteer.data:
            checked
            % end
            >
        </div>
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
                <input class="form-control" readonly id="datecreated" name="datecreated" type="text" value="{{formatted_str_date(form.datecreated.data)}}">
                % get_field_errors(form.datecreated)
            </div>
        </div>
    % end
    </div>
    <div class="page-header" id="dependents_header">
        <h3>Household Members</h3>
    </div>
    % dependent_index = -1
    % for dependent in form.dependents:
    % dependent_index += 1
    % if dependent.isPrimary.data:
    % continue
    % end
    <div class="row dependent">
    <div class="form-group fieldset" data-toggle="fieldset" id="dependent-fieldset">
        Household Member
    <div data-toggle="fieldset-entry">
        <input type="hidden" id="dependents-{{dependent_index}}-isPrimary" name="dependents-{{dependent_index}}-isPrimary" value="">
        <div class="form-group 
        % if dependent.firstName.errors:
        has-error
        % end
        ">
            <label for="dependents-{{dependent_index}}-firstName" class="col-sm-2 control-label">First Name</label>
            <div class="col-sm-10">
                <input class="form-control" id="dependents-{{dependent_index}}-firstName" onblur="capitalizeFirstAndLastNames({{dependent_index}})" name="dependents-{{dependent_index}}-firstName" type="text" value="{{dependent.firstName.data}}">
                % get_field_errors(dependent.firstName)
            </div>
        </div>
        <div class="form-group 
        % if dependent.lastName.errors:
        has-error
        % end
        ">
            <label for="dependents-{{dependent_index}}-lastName" class="col-sm-2 control-label">Last Name</label>
            <div class="col-sm-10">
                <input class="form-control" id="dependents-{{dependent_index}}-lastName" onblur="capitalizeFirstAndLastNames({{dependent_index}})" name="dependents-{{dependent_index}}-lastName" type="text" value="{{dependent.lastName.data}}">
                % get_field_errors(dependent.lastName)
            </div>
        </div>
        <div class="form-group 
        % if dependent.birthdate.errors:
        has-error
        % end
        ">
            <label for="dependents-{{dependent_index}}-birthdate" class="col-sm-2 control-label">Birthday</label>
            <div class="col-sm-10">
                % if dependent.birthdate.data is not None and not dependent.birthdate.errors:
                    <input class="form-control dependent-birthdate" id="dependents-{{dependent_index}}-birthdate" name="dependents-{{dependent_index}}-birthdate" type="datetime" value="{{formatted_str_date(dependent.birthdate.data)}}">
                % else:
                    <input class="form-control dependent-birthdate" id="dependents-{{dependent_index}}-birthdate" name="dependents-{{dependent_index}}-birthdate" type="datetime" value="">
                % end
                % get_field_errors(dependent.birthdate)
            </div>
        </div>
        % if dependent["id"].data is not None:
            <input class="form-control" id="dependents-{{dependent_index}}-id" name="dependents-{{dependent_index}}-id" type="hidden" value="{{dependent["id"].data}}">
        % else:
            <input class="form-control" id="dependents-{{dependent_index}}-id" name="dependents-{{dependent_index}}-id" type="hidden" value="">
        % end
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
        <div class="col-sm-12">
            <button type="button" class="btn btn-success" id="add_another_button">Add Household Member</button>
        </div>
    </div>
    <div class="row" style="margin-top:10px">
        <div class="form-group"> 
            <div class="col-sm-10">
                <button type="submit" class="btn btn-default">Save And Check In</button>
            </div>
        </div>
    </div>
    <div class="row" style="margin-top:10px">
        <div class="col-sm-10">
            <button type="button" id="noCheckin" class="btn btn-info">Save With NO Check In</button>
        </div>
    </div>
    <input type="hidden" id="checkinCust" name="checkinCust" value="true" />
    <input type="hidden" id="checkinVolunteer" name="checkinVolunteer" value="false" />
    </form>
</div>
% if customer_id:
<div class="container-fluid" id ="visits">
    <div class="page-header">
        <h3>Visits</h3>
    </div>
    <div class="row">
        <div class="col-sm-4"></div>
        <div class="col-sm-4"><strong>Checkin</strong></div>
        <div class="col-sm-4"><strong>Checkout</strong></div>
    </div>
    % for visit in visits:
        <div class="row">
            <div class="col-sm-4">
                <a href="{{visit_url_root}}/{{visit.id}}">Visit</a>
            </div>
            <div class="col-sm-4">
                {{utc_time_to_local_time(visit.checkin)}}
            </div>
            % if visit.checkout is None:
            <div class="col-sm-4">
                -None-
            </div>
            % else:
            <div class="col-sm-4">
                {{utc_time_to_local_time(visit.checkout)}}
            </div>
            % end
        </div>
    % end
</div>

<div class="container-fluid" id ="volunteering">
    <div class="page-header">
        <h3>Volunteering</h3>
    </div>
    <div class="row">
        <div class="col-sm-4"></div>
        <div class="col-sm-4"><strong>Checkin</strong></div>
        <div class="col-sm-4"><strong>Checkout</strong></div>
    </div>
    % for volunteer in volunteers:
        <div class="row">
            <div class="col-sm-4">
                <a href="{{volunteer_url_root}}/{{volunteer.id}}">Volunteer</a>
            </div>
            <div class="col-sm-4">
                {{utc_time_to_local_time(volunteer.checkin)}}
            </div>
            % if volunteer.checkout is None:
            <div class="col-sm-4">
                -None-
            </div>
            % else:
            <div class="col-sm-4">
                {{utc_time_to_local_time(volunteer.checkout)}}
            </div>
            % end
        </div>
    % end
</div>
% end
</body>
</html>
