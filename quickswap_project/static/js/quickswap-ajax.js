$(document).ready(function() {
	$('#save').click(function() {
		var userVar;
		var tradeNameVar;
		userVar = $(this).attr('data-user');
		tradeNameVar = $(this).attr('data-tradeName');
		
		$.get(	'/quickswap/save_trade/',
				{'trade_name': tradeNameVar, 
				'user': userVar
				},
				function(data) {
					//$('#like_count').html(data);
					if(data == 1){
						$('#save').css('color', 'red');
					}
					if(data == 0){
						$('#save').css('color', 'black');
					}
					alert("panic, it works!");
				}
			)
	});
});
