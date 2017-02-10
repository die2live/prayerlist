$(document).ready(function () {
	tinymce.init({selector:'textarea'});

	$('.datepicker').datepicker({
		dateFormat: 'yy-mm-dd',
	});

	$('.grid').masonry({    
		itemSelector: '.grid-item',
		columnWidth: 310,
		percentPosition: true        
	});

	$('.deletebtn').click(function() {
		if(confirm('Are you sure?')) {
			var id = $(this).data('id');
			$.post(
				'/delete/' + id + '/', 
				{'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()},
				function(data) {
					window.location = '/all/';
				} );
		} 
	});

	$('#prs_table').DataTable();      

});
