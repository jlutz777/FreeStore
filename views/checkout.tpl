% from utils.utils import *
% include renders
% renders_namespace = _
% get_field_errors = renders_namespace['get_field_errors']
% get_menu = renders_namespace['get_menu']

% from datetime import date

% def calculateAge(born):
%    today = date.today()
%    theAge = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
%    if theAge < 0:
%        theAge = 0
%    end
%    return theAge
% end

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta content="text/html; charset=utf-8" http-equiv="content-type">
<style>
.item_warning
{
    background-color: orange;
    font-weight: normal;
}

.item_limit_reached
{
    background-color: red;
    font-weight: normal;
}
</style>
</head>
<body>
% get_menu()
<script type="text/javascript">
// Categories are a hash of each category and its associated information
// (id, name, daily limit, monthly limit, if it is family-wide or individual, etc.)
var categories = {};
// Previous totals are how many items have been purchased for each family member
// in the time allotted (currently since the beginning of the month)
// previousTotals is a hash of a hash in the form of:
// previousTotals[category id][family member's id] = total previously purchased
var previousMonthlyTotals = {};
var previousYearlyTotals = {};

% # Loop through all the categories and get the data, also set up an empty object for
% # the previous totals
% for cat in categoryChoices:
categories[{{cat["id"]}}] = {
    id: '{{cat["id"]}}',
    name: '{{cat["name"]}}',
    dailyLimit: {{cat["dailyLimit"]}},
    monthlyLimit: {{cat["monthlyLimit"]}},
    % if cat["yearlyLimit"] is not None:
    yearlyLimit: {{cat["yearlyLimit"]}},
    % else:
    yearlyLimit: 10000,
    % end
    isFamilyWide: {{str(cat["familyWideLimit"]).lower()}}};
previousMonthlyTotals[{{cat["id"]}}] = {};
previousYearlyTotals[{{cat["id"]}}] = {};
% end

% # Loop through and set up the previous categories
% for cat in monthlyCategoryTotals:
previousMonthlyTotals[{{cat[0]}}][{{cat[1]}}] = {{cat[2]}};
% end

% # Loop through and set up the previous categories
% for cat in yearlyCategoryTotals:
previousYearlyTotals[{{cat[0]}}][{{cat[1]}}] = {{cat[2]}};
% end

function alertLimitReached()
{
    var reached = false;
    $('.shopping_item.item_over_limit').each(function()
        {
            $(this).removeClass('item_over_limit');
            $('#alert_modal').modal({show:true});
            reached = true;
            return false;
        });
    return reached;
}

// On submit, we have to make sure no limits have been reached.
// If no limits are reached, then show a confirmation before submitting
$(document).ready(function ()
{
    $('form').submit(function()
    {
        if (window.onbeforeunload === null)
        {
            return true;
        }
            
        if (!alertLimitReached())
        {
            // Only check out if the alert wasn't shown
            if (!($("#alert_modal").data('bs.modal') || {}).isShown)
            {
                $('#confirm_modal').modal({show:true});
            }
        }
        
        return false;
    });
    
    $('#continue_checkout').click(function()
    {
        // Clear the onload so you don't get the message and can submit
        window.onbeforeunload = null;
        $('form').submit();
    });

    calculateLimits();
    
    showPrevTotals();
});

// This is pretty complicated, but basically you are setting CSS to indicate
// if you are close to or at limits for each person and each category
function calculateLimits(e)
{
    var changedItem = null;

    $('.shopping_item').each(function()
    {
        var item_name = $(this)[0].name;
        var temp = item_name.split("row_")[1];
        temp = temp.split("_col_");
        var dep_id = parseInt(temp[0], 10);
        var cat_id = parseInt(temp[1], 10);
        
        var orig_item_val = $(this).val();
        var item_val = Number(orig_item_val);

        // Make sure only valid numbers can be typed in the inputs
        if (isNaN(item_val) || item_val < 0 || orig_item_val === '')
        {
            if (orig_item_val !== '')
            {
                $(this).val('');
                changedItem = $(this);
            }

            $(this).removeClass("item_warning item_over_limit item_limit_reached");

            return;
        }

        var curr_cat = categories[cat_id];
        var isFamilyWide = curr_cat.isFamilyWide;
        var latestMonthlyTotal = 0;
        var latestYearlyTotal = 0;

        // If a category is not family-wide (so it is per individual), then
        // calculate the new total for this time period by adding the current value
        // to the previous totals from the db
        if (!isFamilyWide)
        {
            latestMonthlyTotal = item_val;
            latestYearlyTotal = item_val;

            if (dep_id in previousMonthlyTotals[cat_id])
            {
                latestMonthlyTotal += previousMonthlyTotals[cat_id][dep_id];
            }
            
            if (dep_id in previousYearlyTotals[cat_id])
            {
                latestYearlyTotal += previousYearlyTotals[cat_id][dep_id];
            }
        }
        // If it is family-wide, then you need to add up the values in the inputs and
        // add it to the previous totals of all family members
        else
        {
            item_val = 0;
            $(".category_" + cat_id).each(function()
            {
                var innerVal = parseInt($(this).val(), 10);
                if (!isNaN(innerVal))
                {
                    item_val += innerVal
                }
            });

            latestMonthlyTotal = item_val;
            latestYearlyTotal = item_val;

            for (var this_dep_id in previousMonthlyTotals[cat_id])
            {
                if(previousMonthlyTotals[cat_id].hasOwnProperty(this_dep_id))
                {
                    latestMonthlyTotal += previousMonthlyTotals[cat_id][this_dep_id];
                }
            }
            
            for (var this_dep_id in previousYearlyTotals[cat_id])
            {
                if(previousYearlyTotals[cat_id].hasOwnProperty(this_dep_id))
                {
                    latestYearlyTotal += previousYearlyTotals[cat_id][this_dep_id];
                }
            }
        }

        // Remove all classes so you can selectively add any needed below
        $(this).removeClass("item_warning item_over_limit item_limit_reached");

        // If you are over the limit, clear out the current input so you cannot submit
        // this value
        if (latestMonthlyTotal > curr_cat.monthlyLimit || item_val > curr_cat.dailyLimit ||
            latestYearlyTotal > curr_cat.yearlyLimit)
        {
            $(this).val('');
            changedItem = $(this);
            $(this).addClass("item_over_limit");
        }
        else if (latestMonthlyTotal == curr_cat.monthlyLimit || item_val == curr_cat.dailyLimit ||
                 latestYearlyTotal == curr_cat.yearlyLimit)
        {
            $(this).addClass("item_limit_reached");
        }
        else if (latestMonthlyTotal+1 == curr_cat.monthlyLimit || item_val+1 == curr_cat.dailyLimit ||
                 latestYearlyTotal+1 == curr_cat.yearlyLimit)
        {
            $(this).addClass("item_warning");            
        }
    });

    alertLimitReached();

    // Browser bug requires a set timeout for the focus
    setTimeout(function () {
        if (changedItem != null)
        {
            changedItem.focus();
        }    
    }, 10);
}

// Show a nice message for the previous totals so during checkout you
// can easily see previous totals
function showPrevTotals()
{
    var prevText = '';
    var monthlyDeps = {};
    var yearlyDeps = {};

    for (var cat_id in previousMonthlyTotals)
    {
        for (var dep_id in previousMonthlyTotals[cat_id])
        {
            if (dep_id in monthlyDeps)
            {
                monthlyDeps[dep_id] += ", " + previousMonthlyTotals[cat_id][dep_id];
            }
            else
            {
                monthlyDeps[dep_id] = previousMonthlyTotals[cat_id][dep_id];
            }            
            monthlyDeps[dep_id] += " " + categories[cat_id].name;
        }
    }
    
    for (var cat_id in previousYearlyTotals)
    {
        for (var dep_id in previousYearlyTotals[cat_id])
        {
            if (dep_id in yearlyDeps)
            {
                yearlyDeps[dep_id] += ", " + previousYearlyTotals[cat_id][dep_id];
            }
            else
            {
                yearlyDeps[dep_id] = previousYearlyTotals[cat_id][dep_id];
            }            
            yearlyDeps[dep_id] += " " + categories[cat_id].name;
        }
    }
    
    prevText += "Month:<br />";
    for (var dep_id in monthlyDeps)
    {
        var dep_name = $(".dep-" + dep_id + "-name").text();
        prevText += monthlyDeps[dep_id] + " for " + dep_name + "<br />";
    }
    
    prevText += "Year:<br />";
    for (var dep_id in yearlyDeps)
    {
        var dep_name = $(".dep-" + dep_id + "-name").text();
        prevText += yearlyDeps[dep_id] + " for " + dep_name + "<br />";
    }
    
    $("#prev_totals").html(prevText);
}

function warnBeforeNavigate()
{
    var somethingIsNotZero = false;
    $('.shopping_item').each(function()
    {
        var item_name = $(this)[0].name;
        var temp = item_name.split("row_")[1];
        temp = temp.split("_col_");
        var dep_id = parseInt(temp[0], 10);
        var cat_id = parseInt(temp[1], 10);
        
        var orig_item_val = $(this).val();
        var item_val = Number(orig_item_val);

        // Make sure only valid numbers can be typed in the inputs
        if (!isNaN(item_val) && orig_item_val !== '' && item_val > 0)
        {
            somethingIsNotZero = true;
            return;
        }
    });
    
    if (somethingIsNotZero)
    {
       return "You didn't check out yet!  Click Stay On Page to actually check out below.";
    }
};

window.onbeforeunload = warnBeforeNavigate;
</script>
<div id="confirm_modal" class="modal fade">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title">Confirm</h4>
      </div>
      <div class="modal-body">Are you sure you want to checkout?
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">No</button>
        <button id="continue_checkout" type="button" class="btn btn-primary">Yes</button>
      </div>
    </div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div><!-- /.modal -->
<div id="alert_modal" class="modal fade">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title">Alert</h4>
      </div>
      <div class="modal-body">You are beyond the item limit.
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
      </div>
    </div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div><!-- /.modal -->
<div class="your-form container-fluid">
    <form method="POST" action="{{post_url}}" role="form" class="form_horizontal">
    <div class="page-header">
    <h3>Checkout</h3>
    </div>
    % if visit.family.adminComments is not None and visit.family.adminComments != '':
    <div class="row">
    <div class="form-group ">
        <label class="col-sm-4 control-label" style="color:red">ADDITIONAL COMMENTS</label>
        <div class="col-sm-8">
            <label style="color:red">{{visit.family.adminComments}}</label>
        </div>
    </div>
    </div>
    % end
    <div class="row">
    <div class="form-group ">
        <label for="comments" class="col-sm-4 control-label">Checkout Comments</label>
        <div class="col-sm-8">
            % if visit.family.checkoutComments is not None and visit.family.checkoutComments != '':
            <input class="form-control" id="comments" name="comments" type="text" value="{{visit.family.checkoutComments}}">
            % else:
            <input class="form-control" id="comments" name="comments" type="text" value="">
            % end
        </div>
    </div>
    </div>
    <div class="row">
    <div class="form-group ">
        <label class="col-sm-4 control-label">Checkin Time</label>
        <div class="col-sm-8">
            <label>{{utc_time_to_local_time(visit.checkin)}} ({{timeInStore}} in store)</label>
            <input type="hidden" id="checkin" name="checkin" type="text" value="{{formatted_str_date_time(visit.checkin)}}" />
            <input type="hidden" id="family_id" name="family_id" value="{{visit.family.id}}" />
        </div>
    </div>
    </div>
    <div class="row">
    <div class="form-group ">
        <label class="col-sm-4 control-label">Previous Totals:</label>
        <div class="col-sm-8" id="prev_totals">
            (None)
        </div>
    </div>
    </div>
    <div class="row" style="margin-top:20px;">
        <table class="col-sm-12">
            <tr>
                % for dependent in visit.family.dependents:
                    % if dependent.isPrimary:
                        <th>{{dependent.lastName}} Household&nbsp;&nbsp;&nbsp;&nbsp;</th>
                        % break
                    % end
                % end
                <th style="text-align:center;">&nbsp;&nbsp;Age&nbsp;&nbsp;</th>
                % for option in categoryChoices:
                % if not option["disabled"]:
                <th style="text-align:center;">{{option["name"]}}</th>
                % end
                % end
            </tr>
            % depIndex = -1
            % for dependent in visit.family.dependents:
            % depIndex += 1
            <tr>
                % dependentAge = calculateAge(dependent.birthdate)
                <td class="dep-{{dependent.id}}-name">{{dependent.firstName}}</td>
                <td style="text-align: center;">{{dependentAge}}</td>
                % for option in categoryChoices:
                % if not option["disabled"]:
                <td style="text-align: center;">
                % # This is a convention used elsewhere to more easily figure out
                % # which dependent and category this input is for 
                % inputName = "row_" + str(dependent.id) + "_col_" + str(option["id"])
                % thisVal = previousShoppingItems.get(inputName, '')
                <!-- Set the value to 0 for the household if empty
                     to trigger the colors -->
                % if option["familyWideLimit"] and thisVal == '' and depIndex == 0:
                % thisVal = 0
                % end
                % # Some categories are limited to a specific age range, so check it
                % if (option["minAge"] is None or dependentAge >= option["minAge"]) and (option["maxAge"] is None or dependentAge <= option["maxAge"]):
                % if not option["familyWideLimit"] or depIndex == 0:
                <input type="text" name="{{inputName}}" onchange="calculateLimits()" maxlength="2" style="width:30px;" class="shopping_item category_{{option["id"]}}" value="{{thisVal}}"></input>
                % end
                % else:
                {{thisVal}}
                <input type="hidden" name="{{inputName}}" value="{{thisVal}}"></input>
                % end
                </td>
                % end
                % end
            </tr>
            % end
        </table>
    </div>
    <div class="row">
    <div class="form-group" style="margin-top: 20px;"> 
        <div class="col-sm-12">
            <button type="submit" class="btn btn-default">Checkout</button>
        </div>
    </div>
    </div>
    </form>
</div>
</body>
</html>