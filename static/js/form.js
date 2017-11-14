$("#login-button").click(function(event){
		event.preventDefault();
	 $('#title-text').html("Loading results. This might take a while.");
	 $('form').fadeOut(500);
	 $('p').fadeOut(500);
	 $('.wrapper').addClass('form-success');
});

