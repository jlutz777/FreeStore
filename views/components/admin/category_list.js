/* global Ractive, categories */

var categoryReactiveList;

$(document).ready(function ()
{
    Ractive.load( '/components/admin/category_list.html' ).then( function ( CategoryReactiveList ) {
       categoryReactiveList = new CategoryReactiveList({
          el: '#category_list',
          data: { categories: categories }
       });
    });
});