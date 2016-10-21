/* global Ractive, categories, categoryReactiveList, highestCategoryOrder:true */

var categoryReactive;

$(document).ready(function ()
{
    Ractive.load( '/components/admin/category.html' ).then( function ( CategoryReactive ) {
       categoryReactive = new CategoryReactive({
          el: '#category_modal_body',
          data: {}
       });
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
                name: "",
                dailyLimit: "1",
                monthlyLimit: "5",
                yearlyLimit: "60",
                familyWideLimit: false,
                minAge: "",
                maxAge: "",
                disabled: false,
                order: highestCategoryOrder+1,
                existing: false
            };
        }
        categoryReactive.set(category);
    });
    
    $('#add_category').click(function()
    {
        $('#category_modal').modal({show:true});
    });

    $('#save_category').click(function()
    {
        var $form = $('#category_form');
        var $target = $($form.attr('data-target'));
    
        $.ajax({
            type: $form.attr('method'),
            url: $form.attr('action'),
            data: $form.serialize(),
            success: function(data, status)
            {
                if (data.ok)
                {
                    var cat = data.category;
                    cat.existing = true;
                    categories[cat.id] = cat;
                    
                    if (cat.order > highestCategoryOrder)
                    {
                        highestCategoryOrder = cat.order;
                    }
                    
                    categoryReactiveList.set("categories", categories);

                    $target.modal('hide');
                }
                else
                {
                    alert("Error in saving");
                }
            }
        });
    });
    
    /*$('#delete_category').click(function()
    {
    	var keepGoing = confirm('Are you sure you want to delete?');
    	
    	if (keepGoing)
    	{
    		var $form = $('#category_form');
        	var $target = $($form.attr('data-target'));
        	var cat_id = $form.find('#id').val();
        
		    $.ajax({
		        type: 'DELETE',
		        url: 'delete_category/' + cat_id,
		        success: function(data, status)
		        {
		            if (data.ok)
		            {
		            	delete categories[cat_id];
		                
		                categoryReactiveList.set("categories", categories);
		
		                $target.modal('hide');
		            }
		            else
		            {
		                alert("Error in deleting");
		            }
		        }
		    });
    	}
    });*/
});