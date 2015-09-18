% include renders
% renders_namespace = _
% get_field_errors = renders_namespace['get_field_errors']
% get_menu = renders_namespace['get_menu']

% from datetime import date

% def calculateAge(born):
%    today = date.today()
%    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
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
var previousTotals = {};

% # Loop through all the categories and get the data, also set up an empty object for
% # the previous totals
% for cat in categoryChoices:
categories[{{cat[0]}}] = { id: '{{cat[0]}}', name: '{{cat[1]}}', dailyLimit: {{cat[2]}}, monthlyLimit: {{cat[3]}}, isFamilyWide: {{str(cat[4]).lower()}}};
previousTotals[{{cat[0]}}] = {};
% end

% # Loop through and set up the previous categories
% for cat in categoryTotals:
previousTotals[{{cat[0]}}][{{cat[1]}}] = {{cat[2]}};
% end

function alertLimitReached()
{
    var reached = false;
    $('.shopping_item.item_over_limit').each(function()
        {
            alert("Beyond item limit.");
            reached = true;
            return false;
        });
    return reached;
}

// On submit, we have to make sure no limits have been reached.
// If no limits are reached, then show a confirmation before submitting
$(document).ready(function () {
    $('form').submit(function() {
        var continueSubmit = !alertLimitReached();
        if (continueSubmit)
        {
            continueSubmit = confirm("Are you sure you want to check out?");
        }
        // Clear the onload so you don't get the message
        if (continueSubmit)
        {
            window.onbeforeunload = null;
        }
        return continueSubmit;
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
        var latestTotal = 0;

        // If a category is not family-wide (so it is per individual), then
        // calculate the new total for this time period by adding the current value
        // to the previous totals from the db
        if (!isFamilyWide)
        {
            latestTotal = item_val;

            if (dep_id in previousTotals[cat_id])
            {
                latestTotal += previousTotals[cat_id][dep_id];
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

            latestTotal = item_val;

            for (var this_dep_id in previousTotals[cat_id])
            {
                if(previousTotals[cat_id].hasOwnProperty(this_dep_id))
                {
                    latestTotal += previousTotals[cat_id][this_dep_id];
                }
            }
        }

        // Remove all classes so you can selectively add any needed below
        $(this).removeClass("item_warning item_over_limit item_limit_reached");

        // If you are over the limit, clear out the current input so you cannot submit
        // this value
        if (latestTotal > curr_cat.monthlyLimit || item_val > curr_cat.dailyLimit)
        {
            $(this).val('');
            changedItem = $(this);
            $(this).addClass("item_over_limit");
        }
        else if (latestTotal == curr_cat.monthlyLimit || item_val == curr_cat.dailyLimit)
        {
            $(this).addClass("item_limit_reached");
        }
        else if (latestTotal+1 == curr_cat.monthlyLimit || item_val+1 == curr_cat.dailyLimit)
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
    var deps = {};

    for (var cat_id in previousTotals)
    {
        for (var dep_id in previousTotals[cat_id])
        {
            if (dep_id in deps)
            {
                deps[dep_id] += ", " + previousTotals[cat_id][dep_id];
            }
            else
            {
                deps[dep_id] = previousTotals[cat_id][dep_id];
            }            
            deps[dep_id] += " " + categories[cat_id].name;
        }
    }
    
    for (var dep_id in deps)
    {
        var dep_name = $(".dep-" + dep_id + "-name").text();
        prevText += deps[dep_id] + " for " + dep_name + "<br />";
    }
    $("#month_prev_totals").html(prevText);
}

window.onbeforeunload = function ()
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
</script>
<div class="your-form">
    <form method="POST" action="{{post_url}}" role="form" class="form_horizontal">
    <div class="page-header">
    <h3>Checkout</h3>
    </div>
    <div class="row" style="margin-left:0px; margin-right:0px">
    % if visit.family.adminComments is not None and visit.family.adminComments != '':
    <div class="form-group ">
        <label class="col-sm-2 control-label" style="color:red">ADDITIONAL COMMENTS</label>
        <div class="col-sm-10">
            <label style="color:red">{{visit.family.adminComments}}</label>
        </div>
    </div>
    % end
    <div class="form-group ">
        <label for="comments" class="col-sm-2 control-label">Checkout Comments</label>
        <div class="col-sm-10">
            % if visit.family.checkoutComments is not None and visit.family.checkoutComments != '':
            <input class="form-control" id="comments" name="comments" type="text" value="{{visit.family.checkoutComments}}">
            % else:
            <input class="form-control" id="comments" name="comments" type="text" value="">
            % end
        </div>
    </div>
    <div class="form-group ">
        <label class="col-sm-2 control-label">Checkin Time</label>
        <div class="col-sm-10">
            <label>{{visit.checkin.strftime("%I:%M:%S %p")}} ({{timeInStore}} in store)</label>
            <input type="hidden" id="checkin" name="checkin" type="text" value="{{visit.checkin.strftime("%m/%d/%Y %H:%M:%S")}}" />
            <input type="hidden" id="family_id" name="family_id" value="{{visit.family.id}}" />
        </div>
    </div>
    <div class="form-group ">
        <label class="col-sm-2 control-label">This Month Previous Totals:</label>
        <div class="col-sm-10" id="month_prev_totals">
            (None)
        </div>
    </div>
    </div>
    <div class="row" style="margin-top:20px; margin-left:0px; margin-right:0px">
        <table>
            <tr>
                % for dependent in visit.family.dependents:
                    % if dependent.isPrimary:
                        <th>{{dependent.lastName}} Household&nbsp;&nbsp;&nbsp;&nbsp;</th>
                        % break
                    % end
                % end
                <th style="text-align:center; width:30px;">&nbsp;&nbsp;Age&nbsp;&nbsp;</th>
                % for option in categoryChoices:
                <th style="text-align:center; width:75px;">{{option[1]}}</th>
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
                <td style="text-align: center;">
                % # This is a convention used elsewhere to more easily figure out
                % # which dependent and category this input is for 
                % inputName = "row_" + str(dependent.id) + "_col_" + str(option[0])
                % thisVal = previousShoppingItems.get(inputName, '')
                <!-- Set the value to 0 for the household if empty
                     to trigger the colors -->
                % if option[4] and thisVal == '' and depIndex == 0:
                % thisVal = 0
                % end
                % # Some categories are limited to a specific age range, so check it
                % if (option[5] is None or dependentAge >= option[5]) and (option[6] is None or dependentAge <= option[6]):
                % if not option[4] or depIndex == 0:
                <input type="text" name="{{inputName}}" onchange="calculateLimits()" maxlength="2" style="width:30px;" class="shopping_item category_{{option[0]}}" value="{{thisVal}}"></input>
                % end
                % else:
                {{thisVal}}
                <input type="hidden" name="{{inputName}}" value="{{thisVal}}"></input>
                % end
                </td>
                % end
            </tr>
            % end
        </table>
    </div>
    <div class="form-group" style="margin-top: 20px;"> 
        <div class="col-sm-10">
            <button type="submit" class="btn btn-default">Checkout</button>
        </div>
    </div>
    </form>
</div>
</body>
</html>