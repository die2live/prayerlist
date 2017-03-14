$(document).ready(function () {
    $('.btn-lang').click(function(event) {
        $('input[name=language]').val($(this).text());
        $('.form-lang').submit();
    });

	tinymce.init({selector:'textarea'});

	$('.datepicker').datepicker({
		dateFormat: 'yy-mm-dd',
	});

	$('.deletebtn').click(function(event) {
	    event.preventDefault();
		if(confirm('Are you sure?')) {
		    url = $(this).attr('href');
			$.post(
				url,
				{'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()},
				function(data) {
					window.location = '/all/';
				} );
		} 
	});

	$('#prs_table').DataTable({
		'order': [[2, 'desc']]
	});

	$('.togglereadbtn').click(function(event) {
	    event.preventDefault();
	    url = $(this).attr('href');
	    $.post(
            url,
            {'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()},
            function(data) {
                window.location = '/today/';
            }
        );
	});

});
