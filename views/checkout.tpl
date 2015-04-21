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
var categories = {};
var previousTotals = {};

% for cat in categoryChoices:
categories[{{cat[0]}}] = { id: '{{cat[0]}}', name: '{{cat[1]}}', dailyLimit: {{cat[2]}}, monthlyLimit: {{cat[3]}}, isFamilyWide: {{str(cat[4]).lower()}}};
previousTotals[{{cat[0]}}] = {};
% end

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

$(document).ready(function () {
    $('form').submit(function() {
        var continueSubmit = !alertLimitReached();
        if (continueSubmit)
        {
            continueSubmit = confirm("Are you sure you want to check out?");
        }
        return continueSubmit;
    });

    calculateLimits();
});

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

        if (!isFamilyWide)
        {
            latestTotal = item_val;

            if (dep_id in previousTotals[cat_id])
            {
                latestTotal += previousTotals[cat_id][dep_id];
            }
        }
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

        $(this).removeClass("item_warning item_over_limit item_limit_reached");

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

    setTimeout(function () {
        if (changedItem != null)
        {
            changedItem.focus();
        }    
    }, 10);
}
</script>
<div class="your-form">
    <form method="POST" action="{{post_url}}" role="form" class="form_horizontal">
    <div class="page-header">
    <h3>Checkout</h3>
    </div>
    <div class="row" style="margin-left:0px; margin-right:0px">
    <div class="form-group ">
        <label class="col-sm-2 control-label">Checkin Time</label>
        <div class="col-sm-10">
            <label>{{visit.checkin.strftime("%I:%M:%S %p")}} ({{timeInStore}} in store)</label>
            <input type="hidden" id="checkin" name="checkin" type="text" value="{{visit.checkin.strftime("%m/%d/%Y %H:%M:%S")}}" />
            <input type="hidden" id="family_id" name="family_id" value="{{visit.family.id}}" />
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
                <td>{{dependent.firstName}}</td>
                <td style="text-align: center;">{{dependentAge}}</td>
                % for option in categoryChoices:
                <td style="text-align: center;">
                % inputName = "row_" + str(dependent.id) + "_col_" + str(option[0])
                % thisVal = previousShoppingItems.get(inputName, '')
                <!-- Set the value to 0 for the household if empty
                     to trigger the colors -->
                % if option[4] and thisVal == '' and depIndex == 0:
                % thisVal = 0
                % end
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