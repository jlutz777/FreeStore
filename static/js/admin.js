/* =========================================================
 * admin.js
 * ========================================================= */

/* global Ractive, users */
Ractive.DEBUG = true;
Ractive.defaults.delimiters = [ '[[', ']]' ];

var userReactive, userReactiveList;
var categoryReactive, categoryReactiveList;

$(document).ready(function ()
{
    setupUserList();
    setupUserModal();
    //setupCategoryList();
    //setupCategoryModal();
});

function setupUserList()
{
    userReactiveList = new Ractive({
        el: '#user_list',
        template: '#user_li_template',
        data: { users: users }
    });
}

function setupUserModal()
{
    userReactive = new Ractive({
      el: '#user_modal_body',
      template: '#user_template',
      data: { roles: roles }
    });
    
    $('#user_modal').on('show.bs.modal', function(e)
    {
        var user = null;
        if (e.relatedTarget)
        {
            var userId = $(e.relatedTarget).data('user-id');
            user = users[userId];
        }
        else
        {
            user = {
                name: "",
                role: "",
                email: "",
                description: "",
                password: "",
                existing: false
            };
        }
        userReactive.set(user);
    });
    
    $('#add_user').click(function()
    {
        $('#user_modal').modal({show:true});
    });
    
    $('#save_user').click(function()
    {
        var $form = $('#user_form');
        var $target = $($form.attr('data-target'));
    
        $.ajax({
            type: $form.attr('method'),
            url: $form.attr('action'),
            data: $form.serialize(),
            success: function(data, status)
            {
                if (data.ok)
                {
                    var name = data.user.name;
                    users[name] = {
                        name: name,
                        role: data.user.role,
                        email: data.user.email,
                        description: data.user.description,
                        password: data.user.password,
                        existing: true
                    };
                    
                    userReactiveList.set("users", users);

                    $target.modal('hide');
                }
                else
                {
                    alert("Error in saving");
                }
            }
        });
    });
    
    $('#delete_user').click(function()
    {
    	var keepGoing = confirm('Are you sure you want to delete?');
    	
    	if (keepGoing)
    	{
    		var $form = $('#user_form');
        	var $target = $($form.attr('data-target'));
        	var username = $form.find('#username').val();
        
		    $.ajax({
		        type: 'POST',
		        url: 'delete_user',
		        data: 'username='+username,
		        success: function(data, status)
		        {
		            if (data.ok)
		            {
		            	delete users[username];
		                
		                userReactiveList.set("users", users);
		
		                $target.modal('hide');
		            }
		            else
		            {
		                alert("Error in deleting");
		            }
		        }
		    });
    	}
    });
}

function setupCategoryList()
{
    categoryReactiveList = new Ractive({
        el: '#category_list',
        template: '#category_li_template',
        data: { categories: categories }
    });
}

function setupCategoryModal()
{
    categoryReactive = new Ractive({
        el: '#category_modal_body',
        template: '#category_template',
        data: {}
    });
    
    $('#category_modal').on('show.bs.modal', function(e)
    {
        var category = null;
        if (e.relatedTarget)
        {
            var categoryId = $(e.relatedTarget).data('category-id');
            category = categories[categoryId];
        }
        else
        {
            category = {
                existing: false
            };
        }
        categoryReactive.set(category);
    });
}