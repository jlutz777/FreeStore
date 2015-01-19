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
    color: yellow;
    font-weight: normal;
}

.item_limit_reached
{
    color: orange;
    font-weight: normal;
}

.item_over_limit
{
    color: red;
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
        return !alertLimitReached();
    });
});

function calculateLimits()
{
    $('.shopping_item').each(function()
    {
        var item_name = $(this)[0].name;
        var temp = item_name.split("row_")[1];
        temp = temp.split("_col_");
        var dep_id = parseInt(temp[0], 10);
        var cat_id = parseInt(temp[1], 10);
        
        var item_val = parseInt($(this).val(), 10);

        if (isNaN(item_val))
        {
            if ($(this).val() !== '')
            {
                $(this).val('');
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
}
</script>
<div class="your-form">
    <form method="POST" action="{{post_url}}" role="form" class="form_horizontal">
    <div class="page-header">
    <h3>Checkout</h3>
    </div>
    <div class="row" style="margin-left:0px; margin-right:0px">
    <div class="form-group ">
        <label for="checkin" class="col-sm-2 control-label">Checkin Time</label>
        <div class="col-sm-10">
            <input class="form-control" readonly id="checkin" name="checkin" type="text" value="{{visit.checkin.strftime("%m/%d/%Y %H:%M:%S")}}" />
            <input type="hidden" id="family_id" name="family_id" value="{{visit.family.id}}" />
        </div>
    </div>
    </div>
    <div class="row" style="margin-top:20px; margin-left:0px; margin-right:0px">
        <table>
            <tr>
                % for dependent in visit.family.dependents:
                    % if dependent.isPrimary:
                        <th>{{dependent.lastName}} Family&nbsp;&nbsp;&nbsp;&nbsp;</th>
                        % break
                    % end
                % end
                % for option in categoryChoices:
                <th>{{option[1]}}</th>
                % end
            </tr>
            % for dependent in visit.family.dependents:
            <tr>
                % dependentAge = calculateAge(dependent.birthdate)
                <td>{{dependent.firstName}} ({{dependentAge}})</td>
                % for option in categoryChoices:
                <td><input type="text" name="row_{{dependent.id}}_col_{{option[0]}}" onchange="calculateLimits()" class="shopping_item category_{{option[0]}}" value=""></input></td>
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