$(document).ready(function(){

	$("#q").keyup(function(){

q=$(this).val();
$.ajax({


	type:"GET",
	url: "/music/?q="+q,
	data:{

		csrfmiddlewaretoken: '{{ csrf_token }}',
	},
	success: function(data){
		$("#results").html(data)
	}
})


	})
})