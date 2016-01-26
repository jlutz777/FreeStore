/* global Ractive, users, roles, userReactiveList */

var userReactive;

$(document).ready(function ()
{
    Ractive.load( '/components/admin/user.html' ).then( function ( UserReactive ) {
       userReactive = new UserReactive({
          el: '#user_modal_body',
          data: { roles: roles }
       });
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
		        type: 'DELETE',
		        url: 'delete_user/' + username,
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
});
