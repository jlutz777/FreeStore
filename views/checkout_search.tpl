% include renders
% renders_namespace = _ 
% get_menu = renders_namespace['get_menu']

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta content="text/html; charset=utf-8" http-equiv="content-type">
</head>
<body>
% get_menu()
<script type="text/javascript">
var currentVisitsElem;

$(window).load(function()
{
  currentVisitsElem = document.getElementById('currentVisits');

  function getCurrentVisits()
  {
     $.get('/currentVisits', function(data)
      {
          var currVisitsHTML = '';
          var i;
          for (i=0; i<data.length; i++)
          {
            currVisitsHTML += '<p><a href="/customer/' + data[i].familyId + '">';
            currVisitsHTML += data[i].lastName + ", " + data[i].firstName;
            currVisitsHTML += "</a>: " + data[i].timeInStore;
            currVisitsHTML += '</p><p style="margin-bottom:15px"><a href="/checkout/' + data[i].visitId;
            currVisitsHTML += '" role="button" class="btn btn-default">Checkout ';
            currVisitsHTML += data[i].lastName + '</a>';
            currVisitsHTML += '</p>';
          }
          currentVisitsElem.innerHTML = currVisitsHTML;
      });
  }

  getCurrentVisits();
  setInterval(getCurrentVisits, 10000);
});
</script>
<div class="page-header">
    <h3>Check Out Customer</h3>
</div>
<div id="hbox">
  <div id="currentVisits">
  </div>
</div>
</body>
</html>