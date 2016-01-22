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
<!-- Ractive practice -->
<script src='/js/ractive.min.js'></script>
<script src='/js/admin.js'></script>
<script id="user_li_template" type="text/ractive">
[[#users:name]]
    <li class="list-group-item" data-toggle="modal" data-user-id="[[name]]" data-target="#user_modal"><span>[[name]]</span></li>
[[/users]]
</script>
<script id="user_template" type="text/ractive">
    <form id="user_form" action="[[#if existing]]edit_user[[else]]create_user[[/if]]" data-target="#user_modal" method="post">
        <div class="form-horizontal">
        <div class="form-group">
            <label for="username" class="col-sm-4 control-label">User name</label>
            <div class="col-sm-8">
                <input class="form-control" [[#if existing]]readonly[[/if]] id="username" type="text" name="username" value="[[name]]" />
            </div>
        </div>
        <div class="form-group">
            <label for="description" class="col-sm-4 control-label">Description</label>
            <div class="col-sm-8">
                <input class="form-control" [[#if existing]]readonly[[/if]] id="description" type="text" name="description" value="[[description]]" />
            </div>
        </div>
        <div class="form-group">
            <label for="role" class="col-sm-4 control-label">Role</label>
            <div class="col-sm-8">
                <select id="role" name="role" class="form-control" value='[[role]]'>
                  [[#roles:name]]
                    <option value='[[name]]'>[[name]]</option>
                  [[/roles]]
                </select>
            </div>
        </div>
        <div class="form-group">
            <label for="email" class="col-sm-4 control-label">Email</label>
            <div class="col-sm-8">
                <input class="form-control" id="email" type="text" name="email" value="[[email]]" />
            </div>
        </div>
        <div class="form-group">
            <label for="password" class="col-sm-4 control-label">Password</label>
            <div class="col-sm-8">
                <input class="form-control" id="password" type="password" name="password" value="[[password]]" />
            </div>
        </div>
        </div>
      </form>
</script>
<script id="category_li_template" type="text/ractive">
[[#categories:id]]
    <li class="list-group-item" data-toggle="modal" data-category-id="[[id]]" data-target="#category_modal">
        <span>[[name]] ([[order]])</span>
        [[#if disabled]]
        <span> - DISABLED</span>
        [[/if]]
    </li>
[[/categories]]
</script>
<script id="category_template" type="text/ractive">
    <form id="category_form" action="[[#if existing]]edit_category[[else]]create_category[[/if]]" data-target="#category_modal" method="post">
        <input type="hidden" id="id" name="id" value="[[id]]" />
        <div class="form-horizontal">
        <div class="form-group">
            <label for="name" class="col-sm-4 control-label">Name</label>
            <div class="col-sm-8">
                <input class="form-control" id="name" type="text" name="name" value="[[name]]" />
            </div>
        </div>
        <div class="form-group">
            <label for="dailyLimit" class="col-sm-4 control-label">Daily Limit</label>
            <div class="col-sm-8">
                <input class="form-control" id="dailyLimit" type="text" name="dailyLimit" value="[[dailyLimit]]" />
            </div>
        </div>
        <div class="form-group">
            <label for="monthlyLimit" class="col-sm-4 control-label">Monthly Limit</label>
            <div class="col-sm-8">
                <input class="form-control" id="monthlyLimit" type="text" name="monthlyLimit" value="[[monthlyLimit]]" />
            </div>
        </div>
        <div class="form-group">
            <label for="familyWideLimit" class="col-sm-4 control-label">Family Wide Limit</label>
            <div class="col-sm-8">
                <input class="form-control" id="familyWideLimit" type="checkbox" name="familyWideLimit" value="familyWideLimit" checked="[[familyWideLimit]]" />
            </div>
        </div>
        <div class="form-group">
            <label for="order" class="col-sm-4 control-label">Order</label>
            <div class="col-sm-8">
                <input class="form-control" id="order" type="text" name="order" value="[[order]]" />
            </div>
        </div>
        <div class="form-group">
            <label for="minAge" class="col-sm-4 control-label">Minimum Age</label>
            <div class="col-sm-8">
                <input class="form-control" id="minAge" type="text" name="minAge" value="[[minAge]]" />
            </div>
        </div>
        <div class="form-group">
            <label for="maxAge" class="col-sm-4 control-label">Maximum Age</label>
            <div class="col-sm-8">
                <input class="form-control" id="maxAge" type="text" name="maxAge" value="[[maxAge]]" />
            </div>
        </div>
        <div class="form-group">
            <label for="catDisabled" class="col-sm-4 control-label">Disabled</label>
            <div class="col-sm-8">
                <input class="form-control" id="catDisabled" type="checkbox" value="catDisabled" name="catDisabled" checked="[[disabled]]" />
            </div>
        </div>
        </div>
    </form>        
</script>

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
    </div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div><!-- /.modal -->
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
    </div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div><!-- /.modal -->
<div class="container-fluid" style="width:90%">
    <div class="panel panel-default">
        <div class="panel-heading">Users</div>
        <div class="panel-body">
            <ul id="user_list" class="list-group">
            </ul>
        </div>
        <div class="panel-footer">
            <button id="add_user" type="button" class="btn btn-primary">Add</button>
        </div>
    </div>
    <div class="panel panel-default">
        <div class="panel-heading">Categories</div>
        <div class="panel-body">
            <ul id="category_list" class="list-group">
            </ul>
        </div>
        <div class="panel-footer">
            <button id="add_category" type="button" class="btn btn-primary">Add</button>
        </div>
    </div>
</div>
</body>
</html>