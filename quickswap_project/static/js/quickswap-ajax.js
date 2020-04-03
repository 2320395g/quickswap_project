$(document).on('click', 'button[data-tradeName][data-user]', function (e) {

	var buttonIDVar;
	var userVar;
	var tradeNameVar;
	buttonIDVar = $(this).attr('id');
	userVar = $(this).attr('data-user');
	tradeNameVar = $(this).attr('data-tradeName');
	
	$.get(	'/quickswap/save_trade/',
			{'trade_name': tradeNameVar, 
			'user': userVar
			},
			function(data) {
				// $('#like_count').html(data);
				if(data == 1){
					$('#'+buttonIDVar).css('color', 'red');
					alert(tradeNameVar + " has been added to your saved trades.");
				}
				if(data == 0){
					$('#'+buttonIDVar).css('color', 'black');
					alert(tradeNameVar + " has been removed from your saved trades.");
				}
			}
		)

});


/* $(document).ready(function() {
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
					// $('#like_count').html(data);
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
 */