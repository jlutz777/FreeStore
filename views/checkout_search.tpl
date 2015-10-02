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
<style>
  a.customer
  {
      color: rgb(0, 78, 110);
      font-weight: bold;
  }
</style>
<script src='/js/ractive.min.js'></script>
<script id='template' type='text/ractive'>
    [[#visits]]
    <p>
      <a class="customer" href="/customer/[[familyId]]">[[lastName]], [[firstName]]</a>: [[timeInStore]]
    </p>
    <p style="margin-bottom:15px">
      <a href="/checkout/[[visitId]]" role="button" class="btn btn-default">Checkout [[lastName]]</a>
    </p>
    [[/visits]]
</script>
<script type="text/javascript">
$(window).load(function()
{
    Ractive.DEBUG = false;
    Ractive.defaults.delimiters = [ '[[', ']]' ];
    var ractive = new Ractive({
      el: '#currentVisits',
      template: '#template',
      data: { visits: [] }
    });

  function getCurrentVisits()
  {
     $.get('/currentVisits', function(data)
      {
          ractive.set('visits', data);
      });
  }

  getCurrentVisits();
  // Every 10 seconds, get the currently shopping customers
  setInterval(getCurrentVisits, 10000);
});
</script>
<div class="page-header">
    <h3>Current Shoppers</h3>
</div>
<div id="hbox">
  <div id="currentVisits">
  </div>
</div>
</body>
</html>