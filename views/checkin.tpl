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
<script src="/js/typeahead.jquery.min.js"></script>
<script type="text/javascript">
var customerSearch = function(q, cb) {
   return $.post('/customersearch', { 'searchTerm': q}, function(data)
   {
      return cb(data);
   });
};

$(window).load(function()
{
  function onSelected(e,d)
  {
    window.location = '/customer/' + d.family_id;
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
});
</script>
<div class="page-header">
    <h3>Search for Customer</h3>
</div>
<div id="hbox">
  <div class="box">
      <form action="customersearch" method="post" name="customersearch">
        <label>Type part of name to search</label>
        <div id="the-basics">
          <input autofocus class="typeahead" type="text" id="customername" name="customername" />
        </div>
      </form>
      <br />
  </div>
  <br style="clear: left;" />
</div>
</body>
</html>