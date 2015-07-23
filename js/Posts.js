$(document).ready(function(){
      console.log('Running Posts.js')
      $delete = $('#delete');
      $id = $('#id')
      $delete.click(function(){
            var req = $.ajax({
                type: 'DELETE',
                url: '/Posts/' + $id.html(),
            });
            req.done(function(){
                location.reload();
            })
      });
});