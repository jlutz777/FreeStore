% from datetime import datetime, timedelta
% include renders
% renders_namespace = _ 
% get_menu = renders_namespace['get_menu']

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta content="text/html; charset=utf-8" http-equiv="content-type">
<style>
.typeahead,
.tt-query,
.tt-hint {
  width: 396px;
  height: 30px;
  padding: 8px 12px;
  font-size: 24px;
  line-height: 30px;
  border: 2px solid #ccc;
  -webkit-border-radius: 8px;
     -moz-border-radius: 8px;
          border-radius: 8px;
  outline: none;
}

.tt-dropdown-menu {
  width: 422px;
  margin-top: 0px;
  padding: 8px 0;
  background-color: #fff;
  border: 1px solid #ccc;
  border: 1px solid rgba(0, 0, 0, 0.2);
  -webkit-border-radius: 8px;
     -moz-border-radius: 8px;
          border-radius: 8px;
  -webkit-box-shadow: 0 5px 10px rgba(0,0,0,.2);
     -moz-box-shadow: 0 5px 10px rgba(0,0,0,.2);
          box-shadow: 0 5px 10px rgba(0,0,0,.2);
}

.tt-suggestion {
  padding: 3px 20px;
  font-size: 18px;
  line-height: 24px;
}

.tt-suggestion.tt-cursor {
  color: #fff;
  background-color: #0097cf;

}
</style>
</head>
<body>
% get_menu()
<script type="text/javascript">
var customerSearch = function(q, cb) {
   return $.post('customersearch', { 'searchTerm': q}, function(data)
   {
      return cb(data);
   });
};
$(window).load(function()
{
$('#customername').typeahead({
  hint: true,
  highlight: true,
  minLength: 1
},
{
  name: 'customers',
  displayKey: 'fullName',
  source: customerSearch
}).on('typeahead:selected', onSelected);
  
function onSelected(e,d)
{
  window.location = '/customer/' + d.family_id;
}
});
</script>
<div id="hbox">
  <div class="box">
      <h2>Search for Customer</h2>
      <form action="customersearch" method="post" name="customersearch">
        <div id="the-basics">
          <input class="typeahead" type="text" id="customername" name="customername" />
        </div>
          <button type="submit" >OK</button>
      </form>
      <br />
  </div>
  <br style="clear: left;" />
  <div>
    %def td_format(td_object):
    %    seconds = int(td_object.total_seconds())
    %    periods = [
    %            ('year',        60*60*24*365),
    %            ('month',       60*60*24*30),
    %            ('day',         60*60*24),
    %            ('hour',        60*60),
    %            ('minute',      60),
    %            ('second',      1)
    %            ]

    %    strings=[]
    %    for period_name,period_seconds in periods:
    %            if seconds > period_seconds:
    %                    period_value , seconds = divmod(seconds,period_seconds)
    %                    if period_value == 1:
    %                            strings.append("%s %s" % (period_value, period_name))
    %                    else:
    %                            strings.append("%s %ss" % (period_value, period_name))
    %                    end
    %            end
    %    end
    %
    %    return ", ".join(strings)
    %end
    % for visit in currentVisits:
      % for dependent in visit.family.dependents:
        % if dependent.isPrimary:
          <p>{{dependent.lastName}}:
          % timeInStore = td_format(datetime.now() - visit.checkin)
          {{timeInStore}}
          </p>
          % break
        % end
      % end
    % end
  </div>
</div>
</body>
</html>