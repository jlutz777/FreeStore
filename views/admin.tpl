% include renders
% renders_namespace = _ 
% get_field_errors = renders_namespace['get_field_errors']
% get_menu = renders_namespace['get_menu']

<!DOCTYPE html>
<html lang="en">
<head>
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <meta content="text/html; charset=utf-8" http-equiv="content-type">
</head>
<body>
% get_menu()
<div class="container-fluid">
<div class="page-header">
    <h3>Administration</h3>
</div>

<script src='/js/ractive.min.js'></script>
<script src='/js/ractive-load.min.js'></script>
<script src='/js/admin.js?v=2'></script>
<script src='/components/admin/user_list.js'></script>
<script src='/components/admin/user.js'></script>
<script src='/components/admin/category_list.js'></script>
<script src='/components/admin/category.js'></script>

<script type="text/javascript">
    var users = {};
    var roles = {};
    var categories = {};
    var highestCategoryOrder = -1;
    
    %for u in users:
    users["{{u[0]}}"] = {
            name: "{{u[0]}}",
            role: "{{u[1]}}",
            email: "{{u[2]}}",
            description: "{{u[3]}}",
            password: "",
            existing: true
        };
    %end
    
    %for r in roles:
    roles["{{r[0]}}"] = {
            name: "{{r[0]}}",
            level: "{{r[1]}}"
        };
    %end
    
    categories = JSON.parse('{{!categories}}');
    for (cat in categories)
    {
        if (categories[cat].order > highestCategoryOrder)
        {
            highestCategoryOrder = categories[cat].order;
        }
    }
    
</script>

<!-- Modal structure for user component -->
<div id="user_modal" class="modal fade">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title">Edit User</h4>
      </div>
      <div id="user_modal_body" class="modal-body">
      </div>
      <div class="modal-footer">
        <button id="delete_user" type="button" class="btn btn-warning">Delete</button>
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        <button id="save_user" type="button" class="btn btn-primary">Save changes</button>
      </div>
    </div>
  </div>
</div>

<!-- Modal structure for category component -->
<div id="category_modal" class="modal fade">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title">Edit Category</h4>
      </div>
      <div id="category_modal_body" class="modal-body">
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        <button id="save_category" type="button" class="btn btn-primary">Save changes</button>
      </div>
    </div>
  </div>
</div>

<div class="container-fluid" style="width:90%">
    <div class="panel panel-default">
        <div class="panel-heading">Users</div>
        <div class="panel-body">
            <!-- Placeholder for user_list component -->
            <ul id="user_list" class="list-group"></ul>
        </div>
        <div class="panel-footer">
            <button id="add_user" type="button" class="btn btn-primary">Add</button>
        </div>
    </div>
    <div class="panel panel-default">
        <div class="panel-heading">Categories</div>
        <div class="panel-body">
            <!-- Placeholder for category_list component -->
            <ul id="category_list" class="list-group"></ul>
        </div>
        <div class="panel-footer">
            <button id="add_category" type="button" class="btn btn-primary">Add</button>
        </div>
    </div>
</div>
</body>
</html>