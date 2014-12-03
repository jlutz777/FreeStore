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
var currentVisitsElem;

var customerSearch = function(q, cb) {
   return $.post('/customersearch', { 'searchTerm': q}, function(data)
   {
      return cb(data);
   });
};

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
            currVisitsHTML += '<p>';
            currVisitsHTML += data[i].lastName + ": " + data[i].timeInStore;
            currVisitsHTML += '</p>';
          }
          currentVisitsElem.innerHTML = currVisitsHTML;
      });
  }

  getCurrentVisits();
  setInterval(getCurrentVisits, 10000);

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
  <div id="currentVisits">
  </div>
</div>
</body>
</html>