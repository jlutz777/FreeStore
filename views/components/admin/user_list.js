/* global Ractive, users */

var userReactiveList;

$(document).ready(function ()
{
    Ractive.load( '/components/admin/user_list.html' ).then( function ( UserReactiveList ) {
       userReactiveList = new UserReactiveList({
          el: '#user_list',
          data: { users: users }
       });
    });
});