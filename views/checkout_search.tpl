% include renders
% renders_namespace = _ 
% get_menu = renders_namespace['get_menu']

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1">
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
<script src="/js/typeahead.jquery.min.js"></script>
<script type="text/javascript">
var customerSearch = function(q, cb) {
   return $.get('/currentVisits', { 'searchTerm': q}, function(data)
   {
      return cb(data);
   });
};

$(window).load(function()
{
  function onSelected(e,d)
  {
    window.location = '/checkout/' + d.visitId;
  }

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

  $('form input').keydown(function(evt){
    if(evt.keyCode == 13) {
      evt.preventDefault();
    }
  });

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
    <form action="customersearch" method="post" name="customersearch">
        <label>Find shopper:</label>
        <div id="the-basics">
          <input autofocus class="typeahead" type="text" id="customername" name="customername" />
        </div>
      </form>
</div>
<div id="hbox">
  <div id="currentVisits">
  </div>
</div>
</body>
</html>